"""
Checkpoints
------------

Checkpoints refer to a recorded waypost, that allow programs to recover from a previous failure by skipping all the
previously visited wayposts.

Flyte at its core is a workflow engine. Workflows are ways to logically break up an operation / program / idea into smaller
sized chunks, where each chunk (called task in flyte) can be run in an isolated failure domain, i.e., if a task fails
the workflow does not need to run the previously completed tasks, but can simply retry this one task and eventually
when this task succeeds, it will never be run again. Thus, task boundaries naturally serve as checkpoints.

There are cases where it is not easy or desirable to break a task into further smaller tasks, as running a task
adds overhead. This is especially true, when running a large computation in a tight-loop. It is desirable that
once running the task proceeds to completion as the overhead of relaunching or recreating the running state is expensive.
One might argue, that in such a case users could split each loop iteration (or some number of iterations) into a task
and thus use workflows natural checkpointing mechanism to recover. This is completely possible and Flyte's dynamic workflows
provide exactly this capability. But, this is still less then ideal, as in the best case scenario, where failure is not
common, the overhead of spawning new tasks, recording intermediates and re-bootstrapping the state can be extremely
expensive. An example of this case is model-training. Running multiple epochs or different iterations with the same
dataset can take a long time, but the bootstrap time may be high and creating task boundaries can be expensive.

To tackle this, Flyte offers a way to checkpoint progress within a task execution as a file or a set of files. These
checkpoints can be written synchronously or async and in case of failure, the checkpoint file can be re-read to resume
most of the state without re-running the entire task. This opens up the opportunity to use alternate compute systems with
lower guarantees like - `AWS Spot Instances <https://aws.amazon.com/ec2/spot/>`__, `GCP Pre-emptible Instances <https://cloud.google.com/compute/docs/instances/preemptible>`__ etc.

These instances offer great performance at much lower price-points as compared to their OnDemand or Reserved alternatives.
This is possible if you construct your tasks in a fault-tolerant way. For most cases, when the task runs for a short duration,
less than 10 minutes, the potential of failure is not significant and Task-boundary based recovery offers great fault-tolerance
to ensure successful completion.

But, as the time for a task increases, the cost of re-running the task increases and the chance of it successfully completing reduces.
This is where Flyte's intra-task checkpointing truly shines. This document provides an example of how to develop tasks which
utilize intra-task checkpoining. This only provides the low-level API. We intend to integrate higher level api;s with popular
training frameworks like Keras (ModelCheckpoint), Pytorch, Scikit learn, Spark (checkpoints), flink (checkpoints) to super charge
their fault-tolerance.
"""

from flytekit import task, workflow, current_context


# %%
# This task shows how in case of failure checkpoints can help resume. This is only an example task and shows the api for
# the checkpointer. The checkpoint system exposes other api's and for a more detailed understanding refer to
# :ref:pyclass:`flytekit.Checkpoint`
#
# The goal of this method is to actually return `a+4` It does this in 3 retries of the task, by recovering from previous
# failures. For each failure it increments the value by 1
@task(retries=4)
def t1(a: int) -> int:
    cp = current_context().checkpoint
    if not cp:
        raise NotImplementedError(f"Checkpoint is not available! {current_context()}")
    prev = cp.read()
    v = a
    if prev:
        v = int(prev)
        if a - v > 3:
            return v + 1
    cp.write(bytes(v + 1))
    raise RuntimeError(f"V value {v + 1}")


# %%
# The workflow in this case simply calls the task. The task itself will be retried for the failure (runtime error)
@workflow
def my_wf(a: int) -> int:
    return t1(a=a)


if __name__ == "__main__":
    try:
        my_wf(a=10)
    except RuntimeError as e:
        # Locally an exception is expected as retries are not performed.
        pass
