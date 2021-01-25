AWS Sagemaker Training
======================
This section provides examples of Flyte Plugins that are designed to work with
AWS Hosted services like Sagemaker, EMR, Athena, Redshift etc

Builtin Algorithms
------------------

Training a custom model
-----------------------

Creating a dockerfile for Sagemaker custom training [Required]
--------------------------------------------------------------

TODO make this the right dockerfile

.. literalinclude:: ../../sagemaker.Dockerfile
    :language: dockerfile
    :emphasize-lines: 22-24
    :linenos:
    :caption: Dockerfile for Sagemaker, similar to base dockerfile, but installs sagemaker-training and set training script
