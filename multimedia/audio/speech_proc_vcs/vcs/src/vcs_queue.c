/*****************************************************************************/
/*
 * Copyright (C) ST-Ericsson SA 2009,2010. All rights reserved.
 * This code is ST-Ericsson proprietary and confidential.
 * Any use of the code for whatever purpose is subject to
 * specific written permission of ST-Ericsson SA.
 *
 */

/**
 * \file     vcs_queue.c
 * \brief    Standard queue
 * \author   ST-Ericsson
 */
/*****************************************************************************/
#include "vcs_queue.h"
#include <stdlib.h>

struct vcs_queue_s 
{
  unsigned int front;
  unsigned int rear;
  unsigned int size;
  void *q[1];
};

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
vcs_queue_t* vcs_queue_alloc(unsigned int size)
{
  struct vcs_queue_s* q = ( struct vcs_queue_s*) malloc(sizeof(struct vcs_queue_s) + sizeof(void*)*size);
  
  if (q)
  {
    q->front = q->rear = 0;
    q->size = size + 1;
  }

  return q;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
void vcs_queue_destroy(vcs_queue_t*q, vcs_queue_proc_fn foreach)
{
  if (q)
  {
    vcs_queue_empty(q, foreach);
    free(q);
  }
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
int vcs_queue_add(vcs_queue_t*q, void*elem)
{
  unsigned int next = (q->rear + 1) % q->size;
  
  if (next == q->front) 
  {
    return 0;
  }
  q->q[q->rear] = elem;
  q->rear       = next;

  return 1;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
void* vcs_queue_front(vcs_queue_t*q)
{
  if (q->rear != q->front)
  {
    return  q->q[q->front];
  } 
  else 
    return 0;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
void* vcs_queue_dequeue(vcs_queue_t*q)
{
  void* ret;
  if (q->rear != q->front)
  {
    ret = q->q[q->front];
    q->front =( q->front+1) % q->size;
  } 
  else 
    ret = 0;

  return ret;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
int vcs_queue_isempty(vcs_queue_t*q)
{
  return q->rear == q->front;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
int vcs_queue_isfull(vcs_queue_t*q)
{
  return ((q->rear + 1) % q->size)  == q->front;
}

/**********************************************************************************/
/**********************************************************************************/
/**********************************************************************************/
void vcs_queue_empty(vcs_queue_t *q, vcs_queue_proc_fn foreach)
{
  while (!vcs_queue_isempty(q))
  {
    void * d =  vcs_queue_dequeue(q);
    if (foreach && d)
      foreach(d);
  }
}

unsigned int vcs_queue_size(vcs_queue_t*q)
{
	if (q->rear == q->front) return 0;
	else {
		int d = q->rear - q->front;
		if (d < 0) d += q->size;
		return d;
	}
}

