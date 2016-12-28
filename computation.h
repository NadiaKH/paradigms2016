#ifndef __COMPUTATION_H__
#define __COMPUTATION_H__
#include <pthread.h>
#include "thread_pool.h"

typedef void (*OnComputationComplete)(void*);
struct Computation{
	pthread_cond_t cond_var;
	pthread_mutex_t mtx;
	
	void (*f)(void*);
	void * arg;
	struct Task task;
	bool is_completed;
	
	OnComputationComplete on_complete;
	void* on_complete_arg;	
};

void thpool_submit_computation(
    struct ThreadPool *pool,
    struct Computation *computation,
    OnComputationComplete on_complete,
    void* on_complete_arg
);

void thpool_complete_computation(
	struct Computation *computation
);

void thpool_wait_computation(struct Computation *computation);

#endif
