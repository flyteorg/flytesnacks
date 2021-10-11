########################
External Service Plugins
########################

As the term suggests, external service backend plugins relies on external services like
`AWS Sagemaker <https://aws.amazon.com/sagemaker/>`__,
`Hive <https://docs.qubole.com/en/latest/user-guide/engines/hive/index.html>`__ or `Snowflake <https://www.snowflake.com/>`__ for handling the workload defined in
the Flyte task that use the respective plugin.


.. TODO: add the following items to the TOC when the content is written.
.. - gcp

.. panels::
    :header: text-center

    .. link-button:: aws
       :type: ref
       :text: AWS
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Define tasks that use AWS services in your workflows.

    ---

    .. link-button:: auto/integrations/external_services/hive/index
       :type: ref
       :text: Hive
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Run Hive jobs in your workflows.

    ---

    .. link-button:: auto/integrations/external_services/snowflake/index
       :type: ref
       :text: Snowflake
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Run Snowflake jobs in your workflows.


.. toctree::
    :maxdepth: -1
    :caption: Contents
    :hidden:

    aws
    auto/integrations/external_services/hive/index
    auto/integrations/external_services/snowflake/index
