#include "computation.h"
#include <stdlib.h>
#include <stdio.h>
void thpool_submit_computation(
    struct ThreadPool *pool,
    struct Computation *computation,
    OnComputationComplete on_complete,
    void* on_complete_arg
){
	computation -> task.f = computation->f;
	computation -> task.arg = computation->arg;
	pthread_mutex_lock(&computation->mtx);
	computation -> is_completed = false;
	pthread_mutex_unlock(&computation->mtx);
	computation -> on_complete = on_complete;
	computation -> on_complete_arg = on_complete_arg;
	computation -> pool = pool;
	thpool_submit(pool, &computation -> task);
}
void thpool_complete_computation(
	struct Computation *computation
){
	pthread_mutex_lock(&computation->mtx);
	computation->is_completed = true;
	pthread_cond_signal(&computation->cond_var);
	pthread_mutex_unlock(&computation->mtx);
	if (computation->on_complete!=NULL)
		computation->on_complete(computation->on_complete_arg);
}
void thpool_wait_computation(struct Computation *computation){
	while (!computation->is_completed){
		pthread_cond_wait(&computation->cond_var, &computation->mtx);
	}
	pthread_cond_destroy(&computation->cond_var);
	pthread_mutex_destroy(&computation->mtx);
}
