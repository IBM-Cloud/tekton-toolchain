# Tekton in the IBM Cloud
IBM has been providing tools for devops and CI/CD for decades.  One component of the IBM Cloud [DevOps](https://cloud.ibm.com/devops/getting-started) is the Toolchain.  The Pipeline tool has recently been expanded to include open source [Tekton](https://tekton.dev/) resources including Tekton Pipelines and Tasks.

This multi part tutorial will guide you through this interesting technology.

## Before you begin
Navigate to the [tekton-toolchain](https://github.com/IBM-Cloud/tekton-toolchain) GitHub repository and make a fork.  I will call out mine, https://github.com/powellquiring/tekton-toolchain, during the tutorial but use yours instead.

If warnings or errors `Continuous Delivery service required...` are displayed you can live with the warnings or create a [Continuous Delivery](https://cloud.ibm.com/catalog/services/continuous-delivery) service (Lite plan) for the region.

## Labs
The following labs will introduce you to the ibm Tekton framework:
- [Lab 1 Simple getting Started](lab1-simple/README.md)
- [Lab 2 Parameters](lab2-parameters/README.md)
- [Lab 3 Workspaces](lab3-workspaces/README.md)
- [Lab 4 Git scripts](lab4-shared-git/README.md)
- [Lab 5 Example Upgrade](lab5-classic2tekton/README.md)
