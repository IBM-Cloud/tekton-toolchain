# lab 2
This lab on next steps: interactive use, git integration for pipeline start and getting github source for tekton tasks

## Turn on github building

Fork the github repo if you have not already done so and perorm the steps in lab1 to create the toolchain containing the forked github repository and the pipeline service.

In the `Pipeline Service` definitions change the `Path` to lab2

First step is to open the toolchain then open the delivery pipeline, click `Configure Pipeline` and open the `Triggers` panel. Add a `Git Trigger` and specify the the git repo for your fork.

The tekton pipeline will be triggered automatically when your fork is changed.  Make a change to the repository.  In the file lab2/example.yaml change the string:

```
      args:
        - "-c"
        - "echo 01 lab2 env VAR: $VAR"
```
to
```
      args:
        - "-c"
        - "echo 02 lab2 env VAR: $VAR"
```
You can even do this in the github web site.  Just hit the pencil and start editing.

Open the `Delivery Pipeline` and in a few moments a new pipeline run will appear.  Open the log and verify the change.

## Running tkn command line and using private workers
You can optionally improve your development environment by running tekton from the command line.  This is also a good time to step back and create your own kubernetes cluster and worker nodes.  It can be helpful in debugging to poke around in the tekton pods which is not possible when using the public, shared, workers.  

Remember this section is optional, but to blaze ahead follow the instructions in the docs to:

- Create a free kubernetes cluster
- Install and initialize kubectl, following the instructions on the Access tab of the kubernetes cluster
- Configure a **Delivery Pipeline Private Worker** in the toolchain
- Follow the Getting Started instruction in the Deliery Pipeline Private Worker to install private worker support into the kuberrnetes cluster

Now that kubectl is installed and have connected to the kuberrnetes server you can install tkn, the Tekton command line tool: https://github.com/tektoncd/cli.  For me I see

```
$ tkn version
Client version: 0.7.0
```

Lets kick off a pipeline.  Notice how pipeline start command prints out the command to paste to watch it complete, for my case: tkn pipelinerun logs pipeline-run-zn6gd -f -n default.  The EventListener, TriggerBinding and TriggerTemplate are not part of the core, ignore those warnings:

```
$ kubectl apply -f example.yaml
pipeline.tekton.dev/pipeline created
task.tekton.dev/the-var-task created
unable to recognize "example.yaml": no matches for kind "EventListener" in version "tekton.dev/v1alpha1"
unable to recognize "example.yaml": no matches for kind "TriggerBinding" in version "tekton.dev/v1alpha1"
unable to recognize "example.yaml": no matches for kind "TriggerTemplate" in version "tekton.dev/v1alpha1"
$ tkn pipeline start pipeline
Pipelinerun started: pipeline-run-zn6gd

In order to track the pipelinerun progress run:
tkn pipelinerun logs pipeline-run-zn6gd -f -n default
$ tkn pipelinerun logs pipeline-run-zn6gd -f -n default
[xx1 : echoenvvar] 01 lab2 env VAR: VALUE

[xx1 : echovar] VALUE

```

## Run a shell script

To run a shell script in a task the directory of the shell script needs to be available to the task.  Notice in lab2/scripts there is an example script: `hello.sh`.

There are some handy tasks provided by the open toolchain and one of them deals with git repositories.  First open the toolchain and add a tool `GitHub`, Repository type: Existing, GitHub URL: https://github.com/open-toolchain/tekton-catalog

Borrowing heavily from this example, check it out: https://github.com/open-toolchain/tekton-catalog/blob/master/git/sample/listener-simple-clone.yaml

Before getting too deep lets look at parameters starting with tasks.  Below an input parameter `var` is declared and it has a default `VALUE`.
```
kind: Task
metadata:
  name: the-task
spec:
  inputs:
    params:
      - name: var
        description: var example in task
        default: VALUE
  steps:
    - name: echovar
      image: ubuntu
      command:
        - /bin/echo
      args:
        - $(inputs.params.var)
    - name: echoenvvar
      image: ubuntu
      env:
        - name: VAR
          value: $(inputs.params.var)
      command:
        - "/bin/bash"
      args:
        - "-c"
        - "echo env VAR: $VAR"
```

This explains the output for lab2 from the pipeline:
```
[xx1 : echoenvvar] 01 lab2 env VAR: VALUE

[xx1 : echovar] VALUE
```

But how do I get parameters to the task? In the pipeline:
```
apiVersion: tekton.dev/v1alpha1
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

How do I get them parameterized from a user?  First, provide a parameter to the pipeline:
```
```

And provide the pipeline from a Pipelinerun which is an output of the TemplateTrigger in our configuration:








Open the Delivery Pipeline, click `Configure Pipeline` and in the `Definitions` tab choose `Add`, Repository: tekton-catalog, Branch

