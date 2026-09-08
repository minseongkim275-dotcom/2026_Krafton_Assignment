#!/usr/bin/env bash
set -euo pipefail

: "${JIRA_BASE_URL:?}"
: "${JIRA_EMAIL:?}"
: "${JIRA_API_TOKEN:?}"
: "${JIRA_PROJECT_KEY:?}"
ISSUE_TYPE="${JIRA_ISSUE_TYPE:-Task}"

JIRA_AUTH=$(printf '%s:%s' "$JIRA_EMAIL" "$JIRA_API_TOKEN" | base64 -w0)

adf_body() {
  local text="$1"
  jq -n --arg t "$text" '{type:"doc", version:1, content:[{type:"paragraph", content:[{type:"text", text:$t}]}]}'
}

# 라벨 중 "jira-XXX-123" 형태를 찾아서 이미 연결된 Jira 키가 있는지 확인
existing_key=$(gh issue view "$ISSUE_NUMBER" --repo "$REPO" --json labels -q '.labels[].name' \
  | grep '^jira-' | sed 's/^jira-//' | head -n1 || true)

# 연결된 Jira 이슈를 지정한 상태(status 이름)로 전환. 실패해도 워크플로우 전체를 죽이지 않음
transition_to() {
  local key="$1" target_status="$2"

  local transitions
  transitions=$(curl -sf -H "Authorization: Basic $JIRA_AUTH" \
    "$JIRA_BASE_URL/rest/api/3/issue/$key/transitions")

  local transition_id
  transition_id=$(echo "$transitions" \
    | jq -r --arg name "$target_status" '.transitions[] | select(.name==$name) | .id' | head -n1)

  if [ -z "$transition_id" ] || [ "$transition_id" = "null" ]; then
    echo "'$target_status' 상태로 가는 transition을 찾지 못했습니다. Jira 워크플로우 상태명을 확인하세요."
    return 0
  fi

  curl -sf -X POST \
    -H "Authorization: Basic $JIRA_AUTH" \
    -H "Content-Type: application/json" \
    --data "$(jq -n --arg id "$transition_id" '{transition: {id: $id}}')" \
    "$JIRA_BASE_URL/rest/api/3/issue/$key/transitions"
  echo "$key 상태를 $target_status 로 전환했습니다."
}

case "$EVENT_ACTION" in
  opened)
    if [ -n "$existing_key" ]; then
      echo "이미 $existing_key 에 연결되어 있어 생성을 건너뜁니다."
      exit 0
    fi

    description=$(adf_body "$(printf '%s\n\nGitHub Issue: %s' "${ISSUE_BODY:-（내용 없음）}" "$ISSUE_URL")")

    payload=$(jq -n \
      --arg project "$JIRA_PROJECT_KEY" \
      --arg summary "$ISSUE_TITLE" \
      --argjson description "$description" \
      --arg issuetype "$ISSUE_TYPE" \
      '{fields: {project: {key: $project}, summary: $summary, description: $description, issuetype: {name: $issuetype}}}')

    response=$(curl -sf -X POST \
      -H "Authorization: Basic $JIRA_AUTH" \
      -H "Content-Type: application/json" \
      --data "$payload" \
      "$JIRA_BASE_URL/rest/api/3/issue")

    key=$(echo "$response" | jq -r '.key')
    echo "Jira 이슈 생성됨: $key"

    gh label create "jira-$key" --repo "$REPO" --color "0052CC" \
      --description "Linked Jira issue $key" --force
    gh issue edit "$ISSUE_NUMBER" --repo "$REPO" --add-label "jira-$key"
    gh issue comment "$ISSUE_NUMBER" --repo "$REPO" \
      --body "🔗 연결된 Jira 이슈: $JIRA_BASE_URL/browse/$key"
    ;;

  edited)
    if [ -z "$existing_key" ]; then
      echo "연결된 Jira 이슈가 없어 업데이트를 건너뜁니다."
      exit 0
    fi

    description=$(adf_body "$(printf '%s\n\nGitHub Issue: %s' "${ISSUE_BODY:-（내용 없음）}" "$ISSUE_URL")")

    payload=$(jq -n \
      --arg summary "$ISSUE_TITLE" \
      --argjson description "$description" \
      '{fields: {summary: $summary, description: $description}}')

    curl -sf -X PUT \
      -H "Authorization: Basic $JIRA_AUTH" \
      -H "Content-Type: application/json" \
      --data "$payload" \
      "$JIRA_BASE_URL/rest/api/3/issue/$existing_key"
    echo "$existing_key 업데이트 완료"
    ;;

  closed | reopened)
    if [ -z "$existing_key" ]; then
      echo "연결된 Jira 이슈가 없어 상태 전환을 건너뜁니다."
      exit 0
    fi

    target_status="Done"
    [ "$EVENT_ACTION" = "reopened" ] && target_status="To Do"

    transition_to "$existing_key" "$target_status"
    ;;

  labeled)
    # 라벨 이름을 Jira 상태 이름으로 그대로 사용합니다. "To Do" / "In Progress" / "Done"
    # 라벨을 붙이면 그 이름 그대로 Jira 상태 전환을 시도합니다. (우리가 붙이는 "jira-XXX-123"
    # 라벨이나 그 외 라벨(bug, enhancement 등)은 무시)
    case "$LABEL_NAME" in
      "To Do" | "In Progress" | "Done")
        if [ -z "$existing_key" ]; then
          echo "연결된 Jira 이슈가 없어 상태 전환을 건너뜁니다."
          exit 0
        fi
        transition_to "$existing_key" "$LABEL_NAME"
        ;;
      *)
        echo "상태 라벨이 아니라서 건너뜁니다: $LABEL_NAME"
        ;;
    esac
    ;;

  unlabeled)
    echo "라벨 제거는 별도 처리하지 않습니다 (다른 상태 라벨을 붙이면 그걸로 전환됩니다)."
    ;;

  *)
    echo "처리하지 않는 이벤트: $EVENT_ACTION"
    ;;
esac
