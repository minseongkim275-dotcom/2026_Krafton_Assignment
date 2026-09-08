# GitHub Issues ↔ Jira 연동

GitHub Issue를 생성/수정/닫으면 자동으로 Jira 이슈를 생성·갱신·상태전환 해주는 워크플로우입니다.

## 왜 필요한가

Jira Cloud용 **GitHub for Jira** 앱은 커밋/브랜치/PR을 Jira 이슈의 "Development" 패널에
연결해줄 뿐, **GitHub Issues 자체를 Jira 이슈로 옮기거나 동기화하는 기능은 없습니다.**
GitHub Issues와 Jira Issues는 완전히 별개 트래커이기 때문에, 이 저장소에서는 GitHub Actions로
직접 두 시스템을 연결합니다.

## 구성 파일

| 파일 | 역할 |
|---|---|
| `workflows/sync-jira.yml` | `issues` 이벤트(opened/edited/closed/reopened) 트리거 정의 |
| `scripts/sync-jira.sh` | Jira REST API 호출 로직 (이슈 생성/수정/상태전환) |

## 동작 방식

| GitHub 이벤트 | 동작 |
|---|---|
| `opened` | Jira 프로젝트에 새 이슈 생성 → GitHub 이슈에 `jira-<KEY>` 라벨 부착 → Jira 링크 댓글 등록 |
| `edited` | 라벨에서 연결된 Jira 키를 찾아 제목/본문(summary/description) 업데이트 |
| `closed` | 연결된 Jira 이슈를 **"Done"** 상태로 전환 |
| `reopened` | 연결된 Jira 이슈를 **"To Do"** 상태로 전환 |

이미 생성된 이슈인지는 GitHub 이슈에 붙은 `jira-<KEY>` 라벨로 판별합니다
(같은 이슈에 대해 Jira 이슈가 중복 생성되지 않도록 하기 위함).

## 사전 준비: GitHub Secrets 등록

저장소 **Settings → Secrets and variables → Actions → New repository secret** 에서 아래 값을 등록합니다.

| Secret | 값 | 비고 |
|---|---|---|
| `JIRA_BASE_URL` | `https://<도메인>.atlassian.net` | 마지막 슬래시(`/`) 없이 |
| `JIRA_EMAIL` | Jira 로그인 이메일 | |
| `JIRA_API_TOKEN` | [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens) 에서 발급 | 비밀번호 아님, API 토큰 |
| `JIRA_PROJECT_KEY` | 예: `ECM` | Jira 프로젝트 키 |
| `JIRA_ISSUE_TYPE` | (선택) 기본값 `Task` | 프로젝트에 없는 타입이면 반드시 지정 |

`GITHUB_TOKEN`은 GitHub Actions가 자동으로 주입하므로 별도 등록이 필요 없습니다.

## 주의사항

- `closed`/`reopened` 처리에서 사용하는 `"Done"`, `"To Do"` 문자열은 **Jira 프로젝트의 실제 워크플로우
  상태 이름과 정확히 일치**해야 합니다. 다르면 `scripts/sync-jira.sh`의 `target_status` 값을 프로젝트에
  맞게 수정하세요.
- Jira Cloud API v3는 이슈 본문(description)에 일반 텍스트 대신 **ADF(Atlassian Document Format)**를
  요구합니다. 스크립트에서 `adf_body()` 함수로 최소 형태(단일 문단)로 변환해서 전송합니다.
- 일회성으로 기존 GitHub Issues를 전부 옮기고 싶다면 이 워크플로우 대신 CSV export/import
  (Jira Settings → System → External System Import) 방식을 사용하는 것이 더 간단합니다. 이 워크플로우는
  **앞으로 새로 생기는 이슈를 지속적으로 동기화**하는 용도입니다.
