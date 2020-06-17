# Tekton in the IBM Cloud - part 1 getting started

## Goal
You will create a **Toolchain Service** that contains a **Delivery Pipeline**.  The Delivery Pipeline will contain the Tekton resources required to execute automated build and deploy steps when a trigger is clicked.

## Before you begin
Navigate to the [tekton-toolchain](https://github.com/IBM-Cloud/tekton-toolchain) GitHub repository and make a fork.  I will refer to this fork as https://github.com/powellquiring/tekton-toolchain in this tutorial, when you see this replace it with your fork.

If warnings or errors `Continuous Delivery service required...` are displayed you can live with the warnings or create a [Continuous Delivery](https://cloud.ibm.com/catalog/services/continuous-delivery) service (Lite plan) for the region.

## Lets do it
This first part is about the simplest pipeline that can be configured and added to a **pipeline service** of a **toolchain**.

Visit the [IBM Cloud](https://cloud.ibm.com/) in your browser.  In the hamburger menu in the upper left choose `DevOps`.
- Create a toolchain, **Build your own toolchain**, in the context of this toolchain:
- Add tool **GitHub**
  - GitHubServer: GitHub (https://github.com)
  - repository type: existing
  - Repository URL: this repo or your fork: https://github.com/powellquiring/tekton-toolchain
- Add tool **Delivery Pipeline**, name: whatever, Pipeline type: **Tekton**

As you can see a toolchain is a landing page that holds integrated tools.  You have integrated two tools: GitHub and a Delivery Pipeline.

Click the **Delivery Pipeline** to open.  Notice the context is in the Delivery Pipeline service just created.
The Configuration page is likely displayed, if not click **Configure Pipeline** (if you do not see a Configure Pipeline button maybe you did not select Tekton when you created it)

- Select the **Definitions** panel.  Definitions are going to define the set of tekton files that will contribute to this Delivery Pipeline Service.  Contribute all of the files in the **lab1-simple** path in your clone (I show my clone below):

| Repository                              | Branch | Path        |
| --------------------------------------- | ------ | ----------- |
| https://github.com/powellquiring/tekton-toolchain | master | lab1-simple |

- **Worker**: The default works great and for me it was: **(Beta)IBM Managed workers in DALLAS**
- **Triggers**:
  - Add trigger
  - Manual Trigger
  - EventListener: the-listener

**Save** and then **Close** and you are back to the delivery pipeline: click **Run Pipeline** > Manual Trigger.  The **View the PipelineRun** link will take you to the results.

This demonstrates some cool stuff.  All of the tekton files in the github [lab1-simple](https://github.com/IBM-Cloud/tekton-toolchain/tree/master/lab1-simple).  In this case it was just the [tekton.yaml](https://github.com/IBM-Cloud/tekton-toolchain/blob/master/lab1-simple/tekton.yaml) file but all files with a `.yaml` or `.yml` extension would have been read by the Delivery Pipeline service.

- The name of the trigger in the drop down is the same as the EventListener in the lab1-simple/tekton.yaml file:

```
apiVersion: tekton.dev/v1beta1
kind: EventListener
metadata:
  name: the-listener
...
```

Click on the log entry created and you will see `xx1` which matched the task name in the pipeline:

```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: pipeline
spec:
  tasks:
    - name: xx1
```

And you see the task steps that were executed. No surprises. The steps are commands executed in the associated container and give you a feel for the environment.  The `ubuntu` container was supplied by [hub.docker.com](https://hub.docker.com/_/ubuntu)

```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: the-task
spec:
  steps:
    - name: echo
      image: ubuntu
      command:
        - echo
      args:
        - "01 version"
    - name: lslslash
      image: ubuntu
...
```

Note that the last few steps show that the file system is not preserved between steps.