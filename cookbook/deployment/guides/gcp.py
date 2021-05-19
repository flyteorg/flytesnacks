"""
GCP
---
******************************************
Using Flyte with the Google Cloud Platform
******************************************

(insert intro paragraph)

**********************************************************
Troubleshooting Using Flyte with the Google Cloud Platform
**********************************************************

When running examples, the task fails with 401 error
----------------------------------------------------
Steps:

 #. If you are using Workload Identity, then you have to pass in the ServiceAccount when you create the launchplan.
     - Refer to docs :ref:`howto-serviceaccounts`
     - More information about Workload Identity at https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
 #. If you are just using a simple Nodepool wide permissions then check the cluster's ServiceAccount for Storage permissions. Do they look fine?

 #. If not, then start a dummy pod in the intended namespace and check for:

::

    gcloud auth list


.. note::

    FlytePropeller uses Google Application credentials, but gsutil does not use these credentials.
    
"""
