# lab 2 parameters

This lab focuses on parameters and secrets.  There are a few different ways to parameterize tasks so skim all of the possibilities and drill down on the one that meets your needs.

## Turn on github building

Fork the github repo if you have not already done so and perform the steps in lab1 to create the toolchain containing the forked github repository and the pipeline service.

Open the **Pipeline Service**
Open the **Delivery Pipeline**
Open **Configure Pipeline**

- Select the **Definitions** panel and edit to resemble the following.  Note the Path change from the previous lab:

| Repository                              | Branch | Path            |
| --------------------------------------- | ------ | --------------- |
| https://github.com/powellquiring/tekton | master | lab2-parameters |

- Select the **Triggers** panel and add manual triggers for all EventListeners.  Name the trigger the same as the EventListener name.  This will result in the following:
  - n010-task-environment
  - n020-task-default-variable
  - n030-pipeline-supplied-variable
  - n040-user-defined-variable
  - n050-user-defined-secret-variable

Hit **Save**.

## Environment for a Task
The **Enviroment properties** stored in the console UI pipeline configuration can be placed directly into the environment of a Task.  Notice that the **Secure property** is referenced through secretKeyRef and secure-properties while the **Text property** and **Text area property** are accessed through configMapKeyRef and environment-properties in the code below:

```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: task-ibm
spec:
  steps:
    - name: individualpropertiesandsecureproperty
      image: ubuntu
      env:
        - name: NAMEapikey
          valueFrom:
            secretKeyRef:
              name: secure-properties
              key: apikey
        - name: NAMEvar
          valueFrom:
            configMapKeyRef:
              name: environment-properties
              key: var  
        - name: NAMEtextarea
          valueFrom:
            configMapKeyRef:
              name: environment-properties
              key: textarea  
```

If the Task step can use the identically named properties and secrets you can add them all without renaming:

Properties:
```
      envFrom:
        - configMapRef:
            name: environment-properties
```
Secrets:
```
      envFrom:
        - secretRef:
            name: secure-properties     
```

There area also some handy properties that may help you out.  Check out the docs [Tekton Pipelines environment and resources](https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton_environment) for the full list
      env:
        - name: ibm-build-number
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['devops.cloud.ibm.com/build-number']


To see this in action in the GUI click on **Environment Properties**
- add **Text property** `var` with a value like `defined in environment properties`
- add **Text area property** `textarea` with a value like `text area with some new lines`
- add **Secure property area property** `apikey` with a value like `veryprivate`
- **Save**
- **Run Pipeline** with the trigger **n010-task-environment**.

The environment properties that have a name matching the TriggerTemplate parameter specification will be expanded.  In our case the `var` environment property will be expanded in the PipelineRun

Check the output and verify the parameters were passed through correctly.


## Parameter for a task

Below an input parameter `var` is declared and it has a default `VALUE`.

```
kind: Task
metadata:
  name: the-var-task
spec:
  inputs:
    params:
      - name: var
        description: var example in task
        default: VALUE
  steps:
    - name: echoenvvar
      image: ubuntu
      env:
        - name: VAR
          value: $(inputs.params.var)
      command:
        - "/bin/bash"
      args:
        - "-c"
        - "echo 01 lab2 env VAR: $VAR"
    - name: echovar
      image: ubuntu
      command:
        - /bin/echo
      args:
        - $(inputs.params.var)
    - name: shellscript
      image: ubuntu
      env:
        - name: VAR
          value: $(inputs.params.var)
      command: ["/bin/bash", "-c"]
      args:
        - |
          echo this looks just like a shell script and the '$ ( inputs.params.var ) ' is subbed in here: '$(inputs.params.var)'
          env | grep VAR
          echo done with shellscript
```

Click the **Run Pipeline** and choose n020-task-default-variable and when it completes click on the pipeline run results to see the following output:

```
[pdv : echoenvvar]
01 lab2 env VAR: VALUE

[pdv : echovar]
VALUE

[pdv : shellscript]
this looks just like a shell script and the $ ( inputs.params.var )  is subbed in here: VALUE
VAR=VALUE
done with shellscript
```

In the `shellscript` step notice the string `$(inputs.params.var)` substitution is made before the shell script is executed.  

>> Note: The tekton parameter specification `$(inputs.params.var)` looks a little like a bash shell variable which it is not and can potentially be confusing.

## Parameters from a pipeline to a task

But how do I get parameters to the task? In the pipeline:

```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: pipeline-supplied-variable
spec:
  tasks:
    - name: psv
      params:
        - name: var
          value: PIPELINE_SUPPLIED
      taskRef:
        name: the-var-task
```
The Pipeline task is supplying parameters to the same `the-var-task`.  Click **Run Pipeline** and chose n030-pipeline-supplied-variable and check out the results.

## Parameters from a user to a task

How do I get them parameterized from a user clicking in the Delivery Pipeline? A parameter specification is declared in the TriggerTemplate and can be referenced using `$(param.var)`.  The PipelineRun parameter, `$(param.var)`, is expanded when the PipelineRun is created.  In our example this is done when the **Run Pipeline** button is clicked.

```
apiVersion: tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: trigger-user-supplied-variable
spec:
  params:
    - name: var
      description: var example
  resourcetemplates:
    - apiVersion: tekton.dev/v1beta1
      kind: PipelineRun
      metadata:
        name: pipelinerun-$(uid)
      spec:
        pipelineRef:
          name: pipeline-input-parameter-variable
        params:
          - name: var
            value: $(params.var)
```

Simnilarly the Pipeline has a parameter specification and the task is enhanced with a parameter expansion:

```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: pipeline-input-parameter-variable
spec:
  params:
    - name: var
      description: var example in pipeline
  tasks:
    - name: pipv
      params:
        - name: var
          value: $(params.var)
      taskRef:
        name: the-var-task
```
To see this in action in the GUI click on **Environment Properties**
- **Run Pipeline** with the trigger **n040-user-defined-variable**.

## Secrets

A kubernetes Secret object can be created by the TriggerTemplate. Below a Secret object named `secret-object` will be created.  As we saw earlier the `apikey` identifies the property in the console ui Environment Properties of the pipeline configuration in the console UI. The Secret object holds {key: value} pairs.  In this case {secret_key: $(params.apikey)}.

```
kind: TriggerTemplate
metadata:
  name: trigger-user-supplied-secret-variable
spec:
  params:
    - name: apikey
      description: the ibmcloud api key
  resourcetemplates:
    - apiVersion: v1
      kind: Secret
      metadata:
        name: secret-object
      type: Opaque
      stringData:
        secret_key: $(params.apikey)
```

Note the parameter is not passed through the PipelineRun into the Pipeline.  Instead the Task can pull the value from the Secret object.

- secret-object: name of the Secrets resource
- secret_key: key of the {key: value} pair.

```
kind: Task
spec:
  steps:
    - name: echoenvvar
      env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: secret-object
              key: secret_key
```

To see this in action in the GUI click on **Environment Properties**
- **Run Pipeline** with the trigger **n050-user-defined-secret-variable**.
