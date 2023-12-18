(flyte-interactive)=

# FlyIn

```{eval-rst}
.. tags:: Advanced
```


FlyIn provides interactive task development in a remote environment. This allows developers to leverage remote environment capabilities while accessing features like debugging, code inspection, and Jupyter Notebook, traditionally available in local IDEs.


Flyte tasks, designed as one-off jobs, require users to wait until completion to view results. These tasks are developed locally in a virtual environment before being deployed remotely. However, differences in data access, GPU availability, and dependencies between local and remote environments often lead to discrepancies, making local success an unreliable indicator of remote success. This results in frequent, tedious debugging cycles.



## Installation

To use the Flyte interactive plugin, run the following command:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-flyin
```


## Acknowledgement

This feature was created at LinkedIn and later donated to Flyte.

```{auto-examples-toc}
vscode
```
