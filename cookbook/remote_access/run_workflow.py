"""
Running a Workflow
------------------

Workflows on their own are not runnable directly. A launchplan is always bound to a workflow and you can use launchplans to **launch** a workflow. For cases in which you want the launchplan to have the same arguments as a workflow, if you are using one of the SDK's to author your workflows - like flytekit, flytekit-java etc, then they should automatically create a ``default launchplan`` for the workflow. A ``default launchplan`` has identical name as the workflow and all argument defaults are similar. Thus you can use the default launchplan to trigger the workflow.
Tasks can be run using the launch command. One difference is that, launchplans cannot be associated with a task, this is to avoid triggers and scheduling.

"""
