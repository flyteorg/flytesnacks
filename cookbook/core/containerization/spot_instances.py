"""
Using Spot Instances
--------------------

What Are Spot Instances?
========================

Spot Instances are unused EC2 capacity in AWS. `Spot instances <https://aws.amazon.com/ec2/spot/?cards.sort-by=item.additionalFields.startDateTime&cards.sort-order=asc>`_ can result in up to 90% savings on on-demand prices. The caveat is that at any point these instances can be preempted and no longer be available for use. This can happen due to:

* Price – The Spot price is greater than your maximum price.
* Capacity – If there are not enough unused EC2 instances to meet the demand for Spot Instances, Amazon EC2 interrupts Spot Instances. The order in which the instances are interrupted is determined by Amazon EC2.
* Constraints – If your request includes a constraint such as a launch group or an Availability Zone group, these Spot Instances are terminated as a group when the constraint can no longer be met.

Generally, most spot instances are obtained for around 2 hours (median), with the floor being around 20 minutes, and the ceiling of unbounded duration.

What Is Interruptible?
======================

Anyone looking to realize cost savings should look into interruptible.
Interruptible allows users to specify that their tasks are ok to be scheduled on machines that may get preempted such as AWS spot instances. 

Setting Interruptible
=====================

In order to run your workload on spot, you can set interruptible to True. For example:

.. code-block:: python

    @task(cache_version='1', interruptible=True)
    def add_one_and_print(value_to_print: int) -> int:
        return value_to_print + 1


By setting this value, Flyte will schedule your task on an ASG with only spot instances. In the case your task gets preempted, Flyte will retry your task on a non-spot instance. This retry will not count towards a retry that a user sets.

Which Tasks Should Be Set To Interruptible?
===========================================

Most Flyte workloads should be good candidates for spot instances. If your task does NOT exhibit the following properties, then the recommendation would be to set interruptible to true.

* Time sensitive: It needs to run now and can not have any unexpected delays.
* Side Effects: The task is not idempotent and retrying will cause issues.
* Long Running Tasks: The task takes > 2 hours. Having an interruption during this time frame could potentially waste a lot of computation.

How to Recover From Interruptions?
==================================

.. NOTE::

    Coming soon 🛠


"""
