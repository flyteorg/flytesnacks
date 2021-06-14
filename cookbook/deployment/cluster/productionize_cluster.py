"""
Productionize Your Flyte Cluster
--------------------------------
########################
Handling Production Load
########################

In order to handle production load robustly, securely and with high availability, there's a number of important tasks that need to
be done distinctly from the sandbox deployment:

* The kubernetes cluster needs to run securely and robustly
* The sandbox's object store must be replaced with a production grade storage system
* The sandbox's PostgreSQL database with a production grade deployment of postgres
* A production grade task queueing system must be provisioned and configured
* A production grade notification system must be provisioned and configured
* All the above must be done in a secure fashion
* (Optionally) An official dns  domain
* (Optionally) A production grade email sending system must be provisioned and configured

A Flyte user may provision and orchestrate this setup by themselves, but the Flyte team has partnered with the
`Opta <https://github.com/run-x/opta>`_ team to create a streamlined production deployment strategy for AWS with
ready-to-use templates provided in the `Flyte repo <https://github.com/flyteorg/flyte/tree/master/opta>`_. The following
documentation specifies how to use and further configure them.

Deploying Opta Environment and Service for Flyte
************************************************
**The Environment**

To begin using Opta, please first `download the latest version <https://docs.opta.dev/installation/>`_ and all the listed
prerequisites and make sure that you have
`admin/fullwrite AWS credentials setup on your terminal <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.
With that prepared, go to the opta subdirectory in the Flyte repo, and open up env.yaml in your editor. Please find and
replace the following values with your desired ones:

* <account_id>: your aws account id
* <region>: your aws region (e.g. us-east-1)
* <domain>: your desired domain for your flyte deployment (should be a domain which you own or a subdomain thereof-- this environment will promptyly take ownership of the domain/subdomain so make sure you do not wish it for other usages)
* <env_name>: a name to give to the new isolated cloud environment which is going to be created (e.g. flyte-prod)
* <your_company>: your company's/org's name

Once complete please run `opta apply -c env.yaml` and follow the prompts.

**DNS Delegation**
Once the opta apply for the environment is completed you will need to complete dns delegation to fully setup public
traffic access. You may find instructions on `how to do so here <https://docs.opta.dev/miscellaneous/ingress/>`_.

**The Flyte deployment**
Once dns deployment delegation is complete we may deploy the flyte service and affiliated resources. Go to the Opta
subdirectory in the Flyte repo, and open up flyte.yaml in your editor. Please find and replace the following values with
your desired ones:

* <account_id>: your aws account id
* <region>: your aws region

Once complete please run `opta apply -c flyte.yaml` and follow the prompts.

Understanding the Opta Yamls
****************************
The Opta yaml files

**Production Grade Environment**
The Opta env.yaml is responsible for setting up the base infrastructure necessary for most cloud resources. The base
module sets up the VPC and subnets (both public and private) used by thr environment as well as the shared KMS keys.
The dns one sets up the hosted zone for domain and ssl certificates once completed. The k8s-cluster creates the
Kubernetes cluster and node pool (with encrypted disk storage). And lastly the k8s-base module sets up the resources
within Kubernetes like the autoscaler, metrics server, and ingress.

**Production Grade Database**
The aws-postgres module in flyte.yaml creates an Aurora Postgresql database with disk encryption and regular snapshot
backups. You can read more about it `here <https://docs.opta.dev/modules-reference/service-modules/aws/#postgres>`_

**Production Grade Object Store**
The aws-s3 module in flyte.yaml creates a new S3 bucket for flyte, including disk encryption. You can read more about it
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-s3>`_

**Production Grade Notification System**
Flyte uses a combination of the AWS Simple Notification Service (SNS) and Simple Queueing service for a notification
system. flyte.yaml creates both the SNS topic and SQS queue (via the notifcationsQueue and topic modules), which are
encrypted with unique KMS keys and only the  flyte roles can access them. You can read more about the queues
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-sqs>`_ and the topics
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-sns>`_.

**Production Grade Queueing System**
Flyte uses SQS to power its task scheduling system, and flyte.yaml creates said queue (via the schedulesQueue
module) with encryption and principle of least privilege rbac access like the other SQS queue above.

**Secure IAM Roles for Data and Control Planes**


**Flyte Deployment via Helm**
A Flyte deployment contains around 50 kubernetes resources.

Additional Setup
****************
By now you should have all necessary for most production deployments but there are some extra steps which we recommend
most users to consider.

**Email Setup**
Flyte has the power of sending email notifications and this can be enabled in Opta via
`AWS' Simple Email Service <https://aws.amazon.com/ses/>`_ with a few extra steps (NOTE: make sure to have completed dns
delegation first). Simply go to env.yaml and uncomment out the last line ( `- type: aws-ses` ) And run
`opta apply -c env.yaml` again. This will enable SES on your account and environment domain -- you may be prompted to
fill in some user-specific input to take your account out of SES sandbox if not done already. It may take a day for
AWS to enable production SES on your account (you will be kept notified via the email addresses inputted on the user
prompt) but that should not prevent you from moving forward. Lastly, go ahead and uncomment out the 'Uncomment out for SES'
line in the flyte.yaml and rerun `opta apply -c flyte.yaml`.

You will now be able to receive emails sent by flyte as soon as AWS approves your account. You may also specify other
non-default email senders via the helm chart values.

**Flyte Rbac**
All flyte deployments are currently insecure on the application level by default (e.g. open/accessible to everyone) so it
is strongly encouraged for users `to add authentication <https://docs.flyte.org/projects/cookbook/en/latest/auto/deployment/cluster/auth_setup.html>`_.

**Extra configuration**
It is possible to add extra configuration to your flyte deployment by modifying the values passed in the helm chart
used by opta. Please refer to the module

Productionize Your Flyte Cluster
--------------------------------
########################
Handling Production Load
########################

In order to handle production load robustly, securely and with high availability, there's a number of important tasks that need to
be done distinctly from the sandbox deployment:

* The kubernetes cluster needs to run securely and robustly
* The sandbox's object store must be replaced with a production grade storage system
* The sandbox's PostgreSQL database with a production grade deployment of postgres
* A production grade task queueing system must be provisioned and configured
* A production grade notification system must be provisioned and configured
* All the above must be done in a secure fashion
* (Optionally) An official dns  domain
* (Optionally) A production grade email sending system must be provisioned and configured

A Flyte user may provision and orchestrate this setup by themselves, but the Flyte team has partnered with the
`Opta <https://github.com/run-x/opta>`_ team to create a streamlined production deployment strategy for AWS with
ready-to-use templates provided in the `Flyte repo <https://github.com/flyteorg/flyte/tree/master/opta>`_. The following
documentation specifies how to use and further configure them.

Deploying Opta Environment and Service for Flyte
************************************************
**The Environment**
To begin using Opta, please first `download the latest version <https://docs.opta.dev/installation/>`_ and all the listed
prerequisites and make sure that you have
`admin/fullwrite AWS credentials setup on your terminal <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.
With that prepared, go to the opta subdirectory in the Flyte repo, and open up env.yaml in your editor. Please find and
replace the following values with your desired ones:

* {account_id}: your aws account id
* {region}: your aws region
* {domain}: your desired domain for your flyte deployment (should be a domain which you own or a subdomain thereof-- this environment will promptyly take ownership of the domain/subdomain so make sure you do not wish it for other usages)
* {env_name}: a name to give to the new isolated cloud environment which is going to be created (e.g. flyte-prod)
* {your_company}: your company's/org's name

Once complete please run `opta apply -c env.yaml` and follow the prompts.

**DNS Delegation**
Once the opta apply for the environment is completed you will need to complete dns delegation to fully setup public
traffic access. You may find instructions on `how to do so here <https://docs.opta.dev/miscellaneous/ingress/>`_.

**The Flyte deployment**
Once dns deployment delegation is complete we may deploy the flyte service and affiliated resources. Go to the Opta
subdirectory in the Flyte repo, and open up flyte.yaml in your editor. Please find and replace the following values with
your desired ones:

* {account_id}: your aws account id
* {region}: your aws region

Once complete please run `opta apply -c flyte.yaml` and follow the prompts.

Understanding the Opta Yamls
****************************
The Opta yaml files

**Production Grade Environment**
The Opta env.yaml is responsible for setting up the base infrastructure necessary for most cloud resources. The base
module sets up the VPC and subnets (both public and private) used by thr environment as well as the shared KMS keys.
The dns one sets up the hosted zone for domain and ssl certificates once completed. The k8s-cluster creates the
Kubernetes cluster and node pool (with encrypted disk storage). And lastly the k8s-base module sets up the resources
within Kubernetes like the autoscaler, metrics server, and ingress.

**Production Grade Database**
The aws-postgres module in flyte.yaml creates an Aurora Postgresql database with disk encryption and regular snapshot
backups. You can read more about it `here <https://docs.opta.dev/modules-reference/service-modules/aws/#postgres>`_

**Production Grade Object Store**
The aws-s3 module in flyte.yaml creates a new S3 bucket for flyte, including disk encryption and restrictive rbac only
allowing the flyte roles to access it. You can read more about it
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-s3>`_

**Production Grade Notification System**
Flyte uses a combination of the AWS Simple Notification Service (SNS) and Simple Queueing service for a notification
system. flyte.yaml creates both the SNS topic and SQS queue (via the notifcationsQueue and topic modules), which are
encrypted with unique KMS keys and only the  flyte roles can access them. You can read more about the queues
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-sqs>`_ and the topics
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-sns>`_.

**Production Grade Queueing System**
Flyte uses SQS to power its task scheduling system, and flyte.yaml creates said queue (via the schedulesQueue
module) with encryption and principle of least privilege rbac access like the other SQS queue above.

**Secure IAM Roles for Data and Control Planes**
In order to use several of the AWS services above, flyte requires IAM roles for both the control plane and the workers,
which is given via the adminflyterole and userflyterole modules in the flyte.yaml. You can read more about it
`here <https://docs.opta.dev/modules-reference/service-modules/aws/#aws-iam-role>`_

**Flyte Deployment via Helm**
A Flyte deployment contains around 50 kubernetes resources, making it rather unwieldy. To address this issue the flyte
team has created a `helm chart <https://helm.sh/>`_ to manage flyte deplyoments (you can find it `here <https://github.com/flyteorg/flyte/tree/master/helm>`_).
Opta uses said helm chart in its deployment as the helm-chart module in flyte.yaml, but has added all the necessary
values to integrate with the resources listed above, delivering the production-grade deployment. You can read more about
it `here <https://docs.opta.dev/modules-reference/service-modules/cloud-agnostic/#helm-chart>`_

Additional Setup
****************
By now you should have all necessary for most production deployments but there are some extra steps which we recommend
most users to consider.

**Email Setup**
Flyte has the power of sending email notifications and this can be enabled in Opta via
`AWS' Simple Email Service <https://aws.amazon.com/ses/>`_ with a few extra steps (NOTE: make sure to have completed dns
delegation first). Simply go to env.yaml and uncomment out the last line ( `- type: aws-ses` ) And run
`opta apply -c env.yaml` again. This will enable SES on your account and environment domain -- you may be prompted to
fill in some user-specific input to take your account out of SES sandbox if not done already. It may take a day for
AWS to enable production SES on your account (you will be kept notified via the email addresses inputted on the user
prompt) but that should not prevent you from moving forward. Lastly, go ahead and uncomment out the 'Uncomment out for SES'
line in the flyte.yaml and rerun `opta apply -c flyte.yaml`.

You will now be able to receive emails sent by flyte as soon as AWS approves your account. You may also specify other
non-default email senders via the helm chart values.

**Flyte Rbac**
All flyte deployments are currently insecure on the application level by default (e.g. open/accessible to everyone) so it
is strongly encouraged for users `to add authentication <https://docs.flyte.org/projects/cookbook/en/latest/auto/deployment/cluster/auth_setup.html>`_.

**Extra configuration**
It is possible to add extra configuration to your flyte deployment by modifying the values passed in the helm chart
used by opta. Please refer to the possible values allowed from the `Flyte helm chart <https://github.com/flyteorg/flyte/tree/master/helm>`_
and update the values field of the flyte module in the flyte.yaml file accordingly.


Raw Helm Deployment
*******************
It is certainly possible to deploy a production Flyte cluster directly using the helm chart if a user does not wish to
use opta. To do so properly, one will need to ensure they have completed the initial security/ha/robustness checklist
from above, and then use `helm <https://helm.sh/>`_ to deploy the `Flyte helm chart <https://github.com/flyteorg/flyte/tree/master/helm>`_.
s


Raw Helm Deployment
*******************
It is certainly possible to deploy a production Flyte cluster directly using the helm chart if a user does not wish to
use opta. To do so properly, one will need to ensure they have completed the initial security/ha/robustness checklist
from above, and then use `helm <https://helm.sh/>`_ to deploy the `Flyte helm chart <https://github.com/flyteorg/flyte/tree/master/helm>`_.
"""
