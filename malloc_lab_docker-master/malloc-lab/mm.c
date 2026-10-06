/*
 * mm-naive.c - The fastest, least memory-efficient malloc package.
 *
 * In this naive approach, a block is allocated by simply incrementing
 * the brk pointer.  A block is pure payload. There are no headers or
 * footers.  Blocks are never coalesced or reused. Realloc is
 * implemented directly using mm_malloc and mm_free.
 *
 * NOTE TO STUDENTS: Replace this header comment with your own header
 * comment that gives a high level description of your solution.
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*==============================================*/
#define WSIZE 4
#define DSIZE 8
#define CHUNKSIZE (1<<12)

#define MAX(x,y) ((x) > (y) ? (x) : (y))
#define PACK(size,alloc) ((size) | (alloc))

#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (val))

#define GET_SIZE(p) (GET(p) & ~0x7)
#define GET_ALLOC(p) (GET(p) & 0x1)

#define HDRP(bp) ((char *)(bp) - WSIZE)
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp))- DSIZE)

#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE(((char *)(bp) - WSIZE)))
#define PREV_BLKP(bp) ((char *)(bp) - GET_SIZE(((char *)(bp) - DSIZE)))

#define PRED(bp) *(char**)(bp)
#define SUCC(bp) *(char**)((char*)(bp) + DSIZE)

static char *heap_listp;
static char *free_listp;

static void insert_free(void *bp);
static void remove_free(void *bp);
static void *extend_heap(size_t words);
static void *coalesce(void *bp);
static void *find_fit(size_t asize);
static void place(void *bp, size_t asize);
/*==============================================*/
/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "ateam",
    /* First member's full name */
    "Harry Bovik",
    /* First member's email address */
    "bovik@cs.cmu.edu",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""};

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~0x7)

#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))

/*
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    if((heap_listp = mem_sbrk(4*WSIZE)) == (void *)-1)
        return -1;
    PUT(heap_listp, 0);
    PUT(heap_listp + (1*WSIZE), PACK(DSIZE,1));
    PUT(heap_listp + (2*WSIZE), PACK(DSIZE,1));
    PUT(heap_listp + (3*WSIZE), PACK(0,1));
    heap_listp += (2*WSIZE);
    free_listp = NULL;

    if(extend_heap(CHUNKSIZE/WSIZE) == NULL)
        return -1;
    return 0;

}

static void *extend_heap(size_t words)
{
    char *bp;
    size_t size;

    size = (words % 2) ? (words+1)*WSIZE : words * WSIZE;
    /* 왜 나머지 연산을 진행하냐 짝수가 아니면 더했을때 8배수로 안맞춰지기 때문에
    패딩을 넣어주는 작업입니다. */
    if ((long)(bp = mem_sbrk(size)) == -1)
        return NULL;
    PUT(HDRP(bp),PACK(size,0));
    PUT(FTRP(bp),PACK(size,0));
    PUT(HDRP(NEXT_BLKP(bp)),PACK(0,1));

    return coalesce(bp);
}

/*
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    size_t asize;
    size_t extendsize;
    char *bp;

    if (size == 0)
        return NULL;
    
    if (size <= DSIZE)
        asize = 3*DSIZE; /*기본이 24이지만 애초에 주소를 덮어서 데이터가 들어갈수있기때문에 상관없음*/
    else
        asize = DSIZE * ((size + (DSIZE)+(DSIZE-1)) / DSIZE ); /*if 9라고 가정하면 패딩때문에 16을 줘야하며 헤더와 풋터가 4바이트인 8바이트 즉 24가 되야한다. 애초에 넘기면 24부터여서 바꿀필요가 업음*/

    if ((bp = find_fit(asize)) != NULL){
        place(bp,asize);
        return bp;
    }

    extendsize = MAX(asize,CHUNKSIZE);
    if((bp = extend_heap(extendsize/WSIZE)) == NULL)
        return NULL;
    place(bp,asize);
    return bp;

}

static void *find_fit(size_t asize){
    char *bp;
    bp = free_listp;
    while (!(bp == NULL)) 
            if (asize <= GET_SIZE(HDRP(bp)))
                    return bp;
                else
                    bp = SUCC(bp);
    return NULL;
}

static void place(void *bp, size_t asize){
    int num = GET_SIZE(HDRP(bp)) - asize;
    char *new_bp;
    PUT(HDRP(bp),PACK(GET_SIZE(HDRP(bp)),1));
    PUT(FTRP(bp),PACK(GET_SIZE(HDRP(bp)),1));
    remove_free(bp);
    if (num >= 3*DSIZE){
        PUT(FTRP(bp),PACK(num ,0));
        PUT(FTRP(bp) - num + WSIZE, PACK(num,0));
        new_bp = FTRP(bp) - num;
        PUT(new_bp,PACK(asize,1));
        PUT(HDRP(bp),PACK(asize,1));
        coalesce(new_bp + DSIZE);
    }
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *bp)
{
    size_t size = GET_SIZE(HDRP(bp));

    PUT(HDRP(bp), PACK(size,0));
    PUT(FTRP(bp), PACK(size,0));
    coalesce(bp);
}

static void *coalesce(void *bp){
    size_t prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp)));
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));

    if (prev_alloc && next_alloc){
        // return bp;
    }

    else if (prev_alloc && !next_alloc){
        size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
        remove_free(NEXT_BLKP(bp));
        PUT(HDRP(bp), PACK(size,0));
        PUT(FTRP(bp), PACK(size,0));
    }

    else if (!prev_alloc && next_alloc){
        size += GET_SIZE(HDRP(PREV_BLKP(bp)));
        PUT(FTRP(bp), PACK(size,0));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size,0));
        remove_free(PREV_BLKP(bp));
        bp = PREV_BLKP(bp);
    }
    
    else if (!prev_alloc && !next_alloc){
        size += GET_SIZE(HDRP(PREV_BLKP(bp))) + GET_SIZE(HDRP(NEXT_BLKP(bp)));
        PUT(HDRP(PREV_BLKP(bp)),PACK(size,0));
        PUT(FTRP(NEXT_BLKP(bp)),PACK(size,0));
        remove_free(NEXT_BLKP(bp));
        remove_free(PREV_BLKP(bp));
        bp = PREV_BLKP(bp);
    
    }
    insert_free(bp);
    return bp;
}

static void insert_free(void *bp){
    if(free_listp == NULL){
        PRED(bp) = NULL;
        SUCC(bp) = NULL;
        free_listp = bp;
    }
    else{
        PRED(bp) = NULL;
        SUCC(bp) = free_listp;   
        PRED(free_listp) = bp;
        free_listp = bp;              
    }
}

static void remove_free(void *bp){
    if(PRED(bp) == NULL && SUCC(bp) == NULL){
        free_listp = NULL;
    }else if (PRED(bp) == NULL){
        PRED(SUCC(bp)) = NULL;              
        free_listp = SUCC(bp);         
    }else if (SUCC(bp) == NULL){
        SUCC(PRED(bp)) = NULL;
    }else{
        PRED(SUCC(bp)) = PRED(bp);          
        SUCC(PRED(bp)) = SUCC(bp);          
    }

}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    void *oldptr = ptr;
    void *newptr;
    size_t copySize;

    newptr = mm_malloc(size);
    if (newptr == NULL)
        return NULL;
    copySize = GET_SIZE(HDRP(oldptr)) - DSIZE;   /* 블록 크기 - 헤더·풋터 = 페이로드 크기 */
    if (size < copySize)
        copySize = size;
    memcpy(newptr, oldptr, copySize);
    mm_free(oldptr);
    return newptr;
}