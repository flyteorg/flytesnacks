


#. How do I call a workflow from within another workflow?

There are four possible ways of incorporating a workflow into another workflow - you have two choices each along two dimensions.

Workflow vs Launch Plan
  * The workflow can be referenced directly (by using its identifier). Think of this as pass-by-value. (Not yet implemented.)
  * The workflow can be referenced by a launch plan (by using the identifier for the launch plan instead). This of this as pass-by-reference.

Static vs Dynamic
  * The workflow can be declared statically inside another workflow. This is called a sub-workflow and the contents of the inner workflow will appear statically inside the definition of the parent workflow.
  * The workflow can be yielded dynamically from within a dynamic task. In this case, the workflow will not show up until execution time.


Example 1 - Statically including a Launch Plan in Workflow

Workflow name: ``StaticLaunchPlanCaller``

This is the node that gets included in the compiled workflow. Note that the version that's pulled in is assumed to be the version that the workflow registration itself ran with on

.. code-block::

        nodes {
          id: "identity-lp-execution"
          metadata {
            name: "DEADBEEF"
            timeout {
            }
            retries {
            }
          }
          inputs {
            var: "a"
            binding {
              promise {
                node_id: "start-node"
                var: "outer_a"
              }
            }
          }
          workflow_node {
            launchplan_ref {
              resource_type: LAUNCH_PLAN
              project: "flytetester"
              domain: "development"
              name: "cookbook.sample_workflows.formula_1.outer.id_lp"
              version: "7be6342b4d5d95f5e31e6ad89636ad48925643ab"
            }
          }
        }

To get the workflow
flyte-cli -h localhost:30081 -i -p flytetester -d development get-workflow -u wf:flytetester:development:cookbook.sample_workflows.formula_1.outer.StaticLaunchPlanCaller:7be6342b4d5d95f5e31e6ad89636ad48925643ab

Example 2 - Statically including a Workflow in Another Workflow



What about labels and annotations?


