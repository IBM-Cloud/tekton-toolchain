# lab1
Very simple pipeline.

This is about the simplest pipeline that can be configured and added to a `pipeline service` of a toolchain.
- Create a toolchain (build your own toolchain) in the context of this toolchain:
- Add tool GitHub, repository type: existing, Repository URL: this repo or your clone: https://github.com/powellquiring/tekton
- Add tool `Delivery Pipeline`, name: whateever, Pipeline type: Tekton

Open Delivery Pipeline
- Definitions, Repository: GitHub repository above in drop down, Branch: master, Path: lab1 **NOTE**
- Private worker: (Beta)IBM Managed workers in DALLAS
- Triggers: Add trigger, Manual Trigger, EventListener: the-listener

Back to the delivery pipeline: Run Pipeline v Manual Trigger

This demonstrates some cool stuff:
- The name of the trigger in the drop down is the same as the EventListener in the lab1/tekton.yaml file:
```
apiVersion: tekton.dev/v1alpha1
kind: EventListener
metadata:
  name: the-listener
spec:
...
```

Click on the log entry created and you will see `xx1` which matched the task name in the pipeline:
```
apiVersion: tekton.dev/v1alpha1
kind: Pipeline
metadata:
  name: pipeline
spec:
  tasks:
    - name: xx1
```

And you see the task steps that were executed.  No surprises. The steps are commands executed in the associated container and give you a feel for the environment
```
apiVersion: tekton.dev/v1alpha1
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
Note that the last few steps show that the file system is preserved between steps.  Experiment some more to notice that the working directory is not maintained across tasks.
