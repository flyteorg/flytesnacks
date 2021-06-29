"""
Productionize Your Flyte Cluster
--------------------------------

In order to handle production load robustly, securely and with high availability, there are a number of important tasks that need to
be done independently from the sandbox deployment:

* The kubernetes cluster needs to run securely and robustly
* The sandbox's object store must be replaced by a production grade storage system
* The sandbox's PostgreSQL database must be replaced by a production grade deployment of postgres
* A production grade task queueing system must be provisioned and configured
* A production grade notification system must be provisioned and configured
* All the above must be done in a secure fashion
* (Optionally) An official dns domain must be created
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
With that prepared, go to the Opta subdirectory in the Flyte repo, and open up env.yaml in your editor. Please find and
replace the following values with your desired ones:

* <account_id>: your AWS account ID
* <region>: your AWS region
* <domain>: your desired domain for your Flyte deployment (should be a domain which you own or a subdomain thereof - this environment will promptyly take ownership of the domain/subdomain so make sure it will only be used for this purpose)
* <env_name>: a name for the new isolated cloud environment which is going to be created (e.g. flyte-prod)
* <your_company>: your company or organization's name

Once complete please run ``opta apply -c env.yaml`` and follow the prompts.

**DNS Delegation**
Once Opta's apply for the environment is completed, you will need to complete dns delegation to fully setup public
traffic access. You may find instructions on `how to do so here <https://docs.opta.dev/miscellaneous/ingress/>`_.

**The Flyte Deployment**
Once dns deployment delegation is complete, you may deploy the Flyte service and affiliated resources. Go to the Opta
subdirectory in the Flyte repo, and open up flyte.yaml in your editor. Please find and replace the following values with
your desired ones:

* <account_id>: your AWS account ID
* <region>: your AWS region

Once complete please run ``opta apply -c flyte.yaml`` and follow the prompts.

Understanding the Opta Yamls
****************************
The Opta yaml files

**Production Grade Environment**
The Opta env.yaml is responsible for setting up the base infrastructure necessary for most cloud resources. The base
module sets up the VPC and subnets (both public and private) used by the environment as well as the shared KMS keys.
The dns sets up the hosted zone for domain and ssl certificates once completed. The k8s-cluster creates the
Kubernetes cluster and node pool (with encrypted disk storage). And lastly the k8s-base module sets up the resources
within Kubernetes like the autoscaler, metrics server, and ingress.

**Production Grade Database**
The aws-postgres module in flyte.yaml creates an Aurora Postgresql database with disk encryption and regular snapshot
backups. You can read more about it `here <https://docs.opta.dev/modules-reference/service-modules/aws/#postgres>`_

**Production Grade Object Store**
The aws-s3 module in flyte.yaml creates a new S3 bucket for Flyte, including disk encryption. You can read more about it
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
By now you should be set up for most production deployments, but there are some extra steps which we recommend that
most users consider.

**Email Setup**
Flyte has the power to send email notifications, which can be enabled in Opta via
`AWS' Simple Email Service <https://aws.amazon.com/ses/>`_ with a few extra steps (NOTE: make sure to have completed dns
delegation first):
1. Simply go to env.yaml and uncomment out the last line ( `- type: aws-ses` )

2. Run ``opta apply -c env.yaml`` again

This will enable SES on your account and environment domain -- you may be prompted to fill in some user-specific input to take your account out of SES sandbox if not done already.
It may take a day for AWS to enable production SES on your account (you will be kept notified via the email addresses inputted on the user
prompt) but that should not prevent you from moving forward.

3. Lastly, go ahead and uncomment out the 'Uncomment out for SES' line in the flyte.yaml and rerun ``opta apply -c flyte.yaml``.

You will now be able to receive emails sent by Flyte as soon as AWS approves your account. You may also specify other
non-default email senders via the helm chart values.

**Flyte Rbac**
All Flyte deployments are currently insecure on the application level by default (e.g. open/accessible to everyone) so it
is strongly recommended that users `add authentication <https://docs.flyte.org/projects/cookbook/en/latest/auto/deployment/cluster/auth_setup.html#authentication-setup>`_.

**Extra configuration**
It is possible to add extra configuration to your Flyte deployment by modifying the values passed in the helm chart
used by Opta. Please refer to the possible values allowed from the `Flyte helm chart <https://github.com/flyteorg/flyte/tree/master/helm>`_
and update the values field of the Flyte module in the flyte.yaml file accordingly.


Raw Helm Deployment
*******************
It is certainly possible to deploy a production Flyte cluster directly using the helm chart if a user does not wish to
use Opta. To do so properly, one will need to ensure they have completed the initial security/ha/robustness checklist
from above, and then use `helm <https://helm.sh/>`_ to deploy the `Flyte helm chart <https://github.com/flyteorg/flyte/tree/master/helm>`_.

.. role:: raw-html-m2r(raw)
   :format: html

************************************************
Flyte Deployment - Manual AWS/EKS Deployment
************************************************
This guide helps you set up Flyte from scratch, on AWS, without using an automated approach. It details step-by-step how to go from a bare AWS account, to a fully functioning Flyte deployment that members of your company can use.

Prerequisites
=============
Before you begin, please ensure that you have the following tools installed.

* AWS CLI
* ``eksctl``
* Access to AWS console
* Helm
* ``kubectl``
* Openssl

AWS Permissioning
=================
Start off by creating a series of roles. These roles control Flyte's access to the AWS account. Since this is a setup guide, we'll be making liberal use of the default policies that AWS IAM comes with, which may be too broad - please consult with your infrastructure team if necessary.

EKS cluster role
^^^^^^^^^^^^^^^^
First create a role for the EKS cluster. This is the role that the Kubernetes platform itself will use to monitor, scale, and create ASGs, run the etcd store, and the K8s API server, etc.

* Navigate to your AWS console and choose the IAM Roles page
* Under the EKS service, select EKS-Cluster.
* Ensure that the ``AmazonEKSClusterPolicy`` is selected.
* Create this role without any permission boundary. Advanced users can try to restrict the permissions for there usecases.
* Choose any tags that would help in you tracking this role based on your devops rules
* Choose a good name for your cluster role which is easier to search eg ClusterName-EKS-Cluster-Role_

Refer the following AWS docs for the details
https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html#create-service-role

EKS node IAM role
^^^^^^^^^^^^^^^^^^^^^^^^^
Next create a role for your compute nodes to use. This is the role that will be given to the nodes that actually run user pods (including Flyte pods).

* Navigate to your AWS console and choose IAM role service
* Choose EC2 as service while choosing the use case
* Choose the following policies as mentioned in the linked AWS doc

  * AmazonEKSWorkerNodePolicy allows EKS nodes to connect to EKS clusters.
  * AmazonEC2ContainerRegistryReadOnly if using Amazon ECR for container registry.
  * AmazonEKS_CNI_Policy which allows pod and node networking within your VPC. You need this even though it's marked
    as optional in the AWS guide linked below.

* Create this role without any permission boundary. Advanced users can try to restrict the permissions for there usecases.
* Choose any tags that would help in you tracking this role based on your devops rules
* Choose a good name for your cluster role which is easier to search eg ClusterName-EKS-Node-Role_

Refer the following AWS docs for the details
https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html

Flyte System Role
^^^^^^^^^^^^^^^^^^^^^^^^^
Next create a role for the Flyte platform. When pods run, they shouldn't run with the node role created above, they should assume a separate role with permissions suitable for that pod's containers. This role will be used for Flyte's own API servers and associated agents.

Create a role ``iam-role-flyte`` from the IAM console. Select "AWS service" again for the type, and EC2 for the use case.
Attach the ``AmazonS3FullAccess`` policy for now. S3 access can be tweaked later to narrow down the scope.

Flyte User Role
^^^^^^^^^^^^^^^
Finally create a role for Flyte users.  This is the role that user pods will end up assuming when Flyte kicks them off.

Create a role ``flyte-user-role`` from the IAM console. Select "AWS service" again for the type, and EC2 for the use case. Also add the ``AmazonS3FullAccess`` policy for now.

Create EKS cluster
==================
Create an EKS cluster from AWS console.

* Pick a good name for your cluster eg : :raw-html-m2r:`<Name-EKS-Cluster>`
* Pick Kubernetes version >= 1.19
* Choose the EKS cluster role ClusterName-EKS-Cluster-Role_ and not the node role, created in previous steps
* Keep secrets encryption off
* Use the same VPC where you intend to deploy your RDS instance. Keep the default VPC if none created and choose RDS to use the default aswell
* Use the subnets for all the supported AZ's in that VPC
* Choose the security group that you which to use for this cluster and the RDS instance(use default if using default VPC)
* Provide public access to your cluster or depending on your devops settings
* Choose default version of the network addons
* You can choose to enable the control plane logging to CloudWatch.

Connect to EKS cluster
======================
* Use you AWS account access keys to run the following command to update your kube config and switch to the new EKS cluster context
  .. code-block::

       export AWS_ACCESS_KEY_ID=<YOUR-AWS-ACCOUNT-ACCESS-KEY-ID>
       export AWS_SECRET_ACCESS_KEY=<YOUR-AWS-SECRET-ACCESS-KEY>
       exportAWS_SESSION_TOKEN=<YOUR-AWS-SESSION-TOKEN>

*
  Switch to EKS cluster context :raw-html-m2r:`<Name-EKS-Cluster>`

  .. code-block::

     aws eks update-kubeconfig --name <Name-EKS-Cluster> --region <region>

*
  Verify the context is switched

.. code-block::

   kubectl config current-context
   arn:aws:eks:<region>:<AWS_ACCOUNT_ID>:cluster/<Name-EKS-Cluster>

* Test it with ``kubectl``. It should tell you there aren't any resources.

.. code-block::

   kubectl get pods
   No resources found in default namespace.

OIDC Provider for EKS cluster
=============================
Create the OIDC provider to be used for the EKS cluster and associate a trust relationship with the EKS cluster role ClusterName-EKS-Cluster-Role_

* EKS cluster created should have a URL created and hence the following command would return the provider

.. code-block::

  aws eks describe-cluster --region <region> --name <Name-EKS-Cluster> --query "cluster.identity.oidc.issuer" --output text

Example output:

.. code-block::

  https://oidc.eks.us-west-2.amazonaws.com/id/<UUID-OIDC>

* The following command creates the oidc provider using the address provided by the cluster

.. code-block::

  eksctl utils associate-iam-oidc-provider --cluster <Name-EKS-Cluster> --approve

Follow this [AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) for additional reference

* Verify the OIDC provider is created by navigating to https://console.aws.amazon.com/iamv2/home?#/identity_providers and confirming that a new provider entry has been created with the same <UUID-OIDC> issuer as the cluster's.

* Next we need to add a trust relationship between this OIDC provider and the two Flyte roles.
   * Navigate to the newly created OIDC provider with <UUID-OIDC> on https://console.aws.amazon.com/iamv2/home?#/identity_providers and copy the ARN.
   * Navigate to `IAM Roles <https://console.aws.amazon.com/iam/home#/roles>`__ and select your cluster role.
   * Under the Trust relationships tab, hit the Edit button.
   * Replace the ``Principal:Federated`` value in the policy JSON below with the copied ARN.
   * Replace the ``<UUID-OIDC>`` placeholder in the ``Condition:StringEquals`` with the last part of the copied ARN. It'll look something like ``8DCF90D22E386AA3975FC4DCD2ECD23BC`` and should match the tail end of the issuer ID from the first step.
     Ensure you don't accidentally remove the ``:aud`` suffix. You need that.

.. code-block::

   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "eks.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       },
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/oidc.eks.us-east-2.amazonaws.com/id/<UUID-OIDC>"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "oidc.eks.us-east-2.amazonaws.com/id/<UUID-OIDC>:aud": "sts.amazonaws.com"
           }
         }
       }
     ]
   }

Create EKS node group
=====================

The intial EKS cluster wont have any instances configured to operate the cluster. Create a node group which provides resources for the kubernetes cluster.

* Go to your EKS cluster and under compute tab.
* Provide a good enough name :raw-html-m2r:`<Name>`\ -EKS-Node-Group
* Use the EKS node IAM role (ClusterName-EKS-Node-Role_) created in the above steps
* Use without any launch template, kuebernetes labels,taints or tags.
* Choose the default Amazon EC2 AMI (AL2_x86_64)
* Capacity type on demand, Instance type and size can be chosen based on your devops requirements. Keep default if in doubt
* Create a node group with 5/10/5 instance min, max, desired
* Use the default subnets selected which would be chosen based on your EKS cluster accessible subnets.
* Disallow remote access to the nodes(If needed provide the ssh access key pair to use from your account)

Create RDS database
===================
Next create a relational database. This database will be used by both the primary control plane service (Flyte Admin) and the Flyte memoization service (Data Catalog).

* Navigate to `RDS <https://us-east-2.console.aws.amazon.com/rds/home>`__ and create an Aurora engine with Postgres compatibility database
* Leave the Template as Production.
* Change the default cluster identifier to ``flyteadmin``.
* Set the master username to ``flyteadmin``.
* Choose a master password which you'll later use in your Helm template.

  * `Username <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L218>`_
  * `Password <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L196>`_

* Leave Public access off.
* Choose the same VPC that your EKS cluster is in and also add the security group associated with your EKS cluster.
  Provide inbound and outbound rule to allow too and fro traffic from the two. Refer to next section to verify the connectivity before installing flyte on the cluster

  * On the security group where EKS cluster is deployed , allow inbound from RDS cluster besides the existing default

    * All traffic   All All sg-c409c78d / default   – (eg : The rule would look similar to this where sg-c409c78d is default group where RDS is deployed)

  * On the default security group where the RDS cluster is deployed (named as default), add inbound rule to allow traffic from EKS cluster.

    * All traffic   All All sg-06948dc5a63c41453 / eks-cluster-sg-\ :raw-html-m2r:`<cluster-name>`\ -\ :raw-html-m2r:`<some-id>`\ (You will get this name in search as soon as you type name of the cluster)
* Under the top level Additional configuration (there's a sub menu by the same name) under "Initial database name" enter ``flyteadmin`` as well.

Leave all the other settings as is and hit Create.

Check connectivity to RDS database from EKS cluster
===================================================
* Get the :raw-html-m2r:`<RDS-HOST-NAME>` by clicking on the db instance and find the endpoint

We will use pgsql-postgres-client to verify DB connectivity

* Create a testdb namespace for trial

  .. code-block:: bash

     kubectl create ns testdb

* Run the following command with the username and password you used, and the host returned by AWS.

  .. code-block:: bash

     kubectl run pgsql-postgresql-client --rm --tty -i --restart='Never' --namespace testdb --image docker.io/bitnami/postgresql:11.7.0-debian-10-r9 --env="PGPASSWORD=<Password>" --command -- psql testdb --host <RDS-HOST-NAME> -U <Username> -d flyteadmin -p 5432

* If things are working fine then you should drop into a psql command prompt. Type ``\q`` to quit. If you make a mistake in the above command you may need to delete the pod created with ``kubectl -n testdb delete pod pgsql-postgresql-client``

* In case there are connectivity issues then you would see the following error. Please check the security groups on the Database and the EKS cluster.

.. code-block:: bash

   psql: warning: extra command-line argument "testdb" ignored
   psql: could not translate host name "database-2-instance-1.ce40o2y3b4os.us-east-2.rds.amazonaws.co" to address: Name or service not known
   pod "pgsql-postgresql-client" deleted
   pod flyte/pgsql-postgresql-client terminated (Error)

Install Amazon Loadbalancer Ingress Controller
==============================================

The cluster doesn't come with any ingress controllers so we have to install one separately. This one will create an AWS load balancer for K8s Ingress objects.

Before we begin, make sure all the subnets are tagged correctly for subnet discovery. The controller uses this for creating the ALB's.

* Go to your default VPC subnets. There would be 3 subnets for the 3 AZ's.
* Add 2 tags on all the three subnets
  Key kubernetes.io/role/elb Value 1
  Key kubernetes.io/cluster/\ :raw-html-m2r:`<Name-EKS-Cluster>` Value shared
* Refer this doc for additional details https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.1/deploy/subnet_discovery/

* Download IAM policy for the AWS Load Balancer Controller
  .. code-block::

     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.0/docs/install/iam_policy.json

* Create an IAM policy called AWSLoadBalancerControllerIAMPolicy(delete it if it already exists from IAM service)
  .. code-block::

     aws iam create-policy \
       --policy-name AWSLoadBalancerControllerIAMPolicy \
       --policy-document file://iam-policy.json

* Create a IAM role and ServiceAccount for the AWS Load Balancer controller, using the ARN from the step above.
  .. code-block::

     eksctl create iamserviceaccount \
     --cluster=<cluster-name> \
     --region=<region> \
     --namespace=kube-system \
     --name=aws-load-balancer-controller \
     --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
     --override-existing-serviceaccounts \
     --approve

* Add the EKS chart repo to helm

  .. code-block::

     helm repo add eks https://aws.github.io/eks-charts

*
  Install the TargetGroupBinding CRDs

  .. code-block::

     kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

*
  Install the load balancer controller using helm

.. code-block::

   helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<Name-EKS-Cluster> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller


* Verify load balancer webhook service is running in kube-system ns

.. code-block::

   kubectl get service -n kube-system

Sample o/p

.. code-block::

   NAME                                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
   aws-load-balancer-webhook-service   ClusterIP   10.100.255.5   <none>        443/TCP         95s
   kube-dns                            ClusterIP   10.100.0.10    <none>        53/UDP,53/TCP   75m

.. code-block::

   ✗ kubectl get pods -n kube-system
   NAME                                            READY   STATUS    RESTARTS   AGE
   aws-load-balancer-controller-674869f987-brfkj   1/1     Running   0          11s
   aws-load-balancer-controller-674869f987-tpwvn   1/1     Running   0          11s


* Use this doc for any additional installation instructions
  https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/deploy/installation/


SSL Certificate
===============
In order to use SSL (which we need to use gRPC clients), we next need to create an SSL certificate. We realize that
you may need to work with your infrastructure team to acquire a legitmate certificate, so the first set of instructions
help you get going with a self-signed certificate. These are of course not secure and will show up as a security warning
to any users, so we recommend deploying a legitimate certificate as soon as possible.

Self-Signed Method (Insecure)
-----------------------------

Generate a self signed cert using open ssl and get the :raw-html-m2r:`<KEY>` and :raw-html-m2r:`<CRT>` file.

#. Define req.conf file with the following contents.
  .. code-block::

       [req]
       distinguished_name = req_distinguished_name
       x509_extensions = v3_req
       prompt = no
       [req_distinguished_name]
       C = US
       ST = WA
       L = Seattle
       O = Flyte
       OU = IT
       CN = flyte.example.org
       emailAddress = dummyuser@flyte.org
       [v3_req]
       keyUsage = keyEncipherment, dataEncipherment
       extendedKeyUsage = serverAuth
       subjectAltName = @alt_names
       [alt_names]
       DNS.1 = flyte.example.org

#. Use openssl to generate the KEY and CRT files.

.. code-block::

   openssl req -x509 -nodes -days 3649 -newkey rsa:2048 -keyout key.out -out crt.out -config req.conf -extensions 'v3_req'

#. Create ARN for the cert.

.. code-block::

     aws acm import-certificate --certificate fileb://crt.out --private-key fileb://key.out --region us-east-2

Production
----------

Generate a cert from the CA used by your org and get the :raw-html-m2r:`<KEY>` and :raw-html-m2r:`<CRT>`
Flyte doesn't manage the lifecycle of certificates so this will need to be managed by your security or infrastructure team.

AWS docs for importing the cert https://docs.aws.amazon.com/acm/latest/userguide/import-certificate-prerequisites.html
Requesting a public cert issued by ACM Private CA https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html#request-public-console

Note the generated ARN. Let's calls it :raw-html-m2r:`<CERT-ARN>` in this doc which we will use to replace in our values-eks.yaml

Use AWS Certificate manager for generating the SSL certificate to host your hosted flyte installation


Create S3 Bucket
================
* Create an S3 bucket without public access.
* Choose a good name for it  :raw-html-m2r:`<ClusterName-Bucket>`
* Use the same region as the EKS cluster


Create a Log Group
==================
Navigate to the `AWS Cloudwatch <https://us-east-2.console.aws.amazon.com/cloudwatch/home>`__ page and create a Log Group.
Give it a reasonable name like ``flyteplatform``.

Installing Flyte
================

#. Clone flyte repo

.. code-block:: bash

   git clone https://github.com/flyteorg/flyte

#. Update values

Search and replace the following

.. list-table:: Helm EKS Values
   :widths: 25 25 75
   :header-rows: 1

   * - Placeholder
     - Description
     - Sample Value
   * - ``<ACCOUNT_NUMBER>``
     - The AWS Account ID
     - ``173113148371``
   * - ``<AWS_REGION>``
     - The region your EKS cluster is in
     - ``us-east-2``
   * - ``<RDS_HOST_DNS>``
     - DNS entry for your Aurora instance
     - ``flyteadmin.cluster-cuvm8rpzqloo.us-east-2.rds.amazonaws.com``
   * - ``<BUCKET_NAME>``
     - Bucket used by Flyte
     - ``my-sample-s3-bucket``
   * - ``<DB_PASSWORD>``
     - The password in plaintext for your RDS instance
     - awesomesauce
   * - ``<LOG_GROUP_NAME>``
     - CloudWatch Log Group
     - ``flyteplatform``
   * - ``<CERTIFICATE_ARN>``
     - ARN of the self-signed (or official) certificate
     - ``arn:aws:acm:us-east-2:173113148371:certificate/763d12d5-490d-4e1e-a4cc-4b28d143c2b4``

   Use the arn value from ClusterName-EKS-Cluster-Role_ page\ ``arn:aws:iam::<AWS_ACCOUNT_ID>:role/ClusterName-EKS-Cluster-Role`` and replace them in following places and also turn on ServiceAccount creation (``create: true``)

  * `Flyteadmin Service Account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L13>`_
  * `Datacatlog service Account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L51>`_
  * `Flytepropeller service Account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L85>`_
  * `Flytepropeller service Account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L85>`_
  * `aab_default_service_account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L389>`_
  * `ae_spark_service_account <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L440>`_

*
  Update the RDS host name
  * Get the :raw-html-m2r:`<RDS-HOST-NAME>` by clicking on the db instance and find the endpoint
  * Update it `RDS-HOST-NAME <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L219>`_

* Update Bucket name with :raw-html-m2r:`<ClusterName-Bucket>`

  * `Bucket Name <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L210>`_ for flyte to use

* Update Region name

  * `Region <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L212>`_ for the flyte bucket

*
  Update certificate ARN with :raw-html-m2r:`<CERT-ARN>`


  * `ARN Certificate <https://github.com/flyteorg/flyte/blob/3600badd2ad49ec2cd1f62752780f201212de3f3/helm/values-eks.yaml#L176>`_ copy this from the generated SSL cert using AWS certificate manager

*
  Update the helm deps

.. code-block:: bash

   helm dep update


* Installing flyte

.. code-block:: bash

   cd helm
   helm install -n flyte -f values-eks.yaml --create-namespace flyte .


* Verify all the pods have come up correctly

.. code-block:: bash

   kubectl get pods -n flyte

Uninstalling flyte
==================

.. code-block:: bash

   helm uninstall -n flyte flyte

Upgrading flyte
===============

.. code-block:: bash

   helm upgrade -n flyte -f values-eks.yaml --create-namespace flyte .

Connecting to flyte
===================

Flyte can be accessed using the UI console or CLI


* Before that find the endpoint to connect to flyte

.. code-block:: bash

   kubectl get service -n flyte

Without using DNS use the ADDRESS column to get the ingress endpoint which will be used for accessing flyte

.. code-block::

   NAME         CLASS    HOSTS   ADDRESS                                                       PORTS   AGE
   flyte        <none>   *       k8s-flyte-8699360f2e-1590325550.us-east-2.elb.amazonaws.com   80      3m50s
   flyte-grpc   <none>   *       k8s-flyte-8699360f2e-1590325550.us-east-2.elb.amazonaws.com   80      3m49s

<FLYTE-ENDPOINT> = Value in ADDRESS column and both will be the same as the same port is used for both GRPC and HTTP


* Connecting to flytectl CLI

Add :<FLYTE-ENDPOINT>  to ~/.flyte/config.yaml eg ;

.. code-block::

   admin:
     # For GRPC endpoints you might want to use dns:///flyte.myexample.com
     endpoint: dns:///<FLYTE-ENDPOINT>
     insecureSkipVerify: true # only required if using a self-signed cert. Caution: not to be used in production
     insecure: true
     authType: Pkce
   logger:
     show-source: true
     level: 0

Accessing flyte console
=======================


* Use the https://<FLYTE-ENDPOINT>/console to get access to flyteconsole UI
* Ignore the certificate error if using a self signed cert

Troubleshooting
===============


* If flyteadmin pod is not coming up, then describe the pod and check which of the container or init-containers had an error.

.. code-block:: bash

   kubectl describe pod/<flyteadmin-pod-instance> -n flyte

Then check the logs for the container which failed.
eg: to check for run-migrations init container do this. If you see connectivity issue then check your security group rules on the DB and eks cluster. Authentication issues then check you have used the same password in helm and RDS DB creation. (Note : Using Cloud formation template make sure passwords are not double/single quoted)

.. code-block:: bash

   kubectl logs -f <flyteadmin-pod-instance> run-migrations -n flyte


* Increasing log level for flytectl
  Change your logger config to this
  .. code-block::

     logger:
     show-source: true
     level: 6

"""
