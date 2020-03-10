# lab 3
This lab focuses on workspaces.

A workspace is a disk volume made available to a task.

## Initialize
If continuing from the previous lab open the pipeline configuration and configure a single definition for the lab3 path

A private worker will be needed to create a workspace.

## Trigger Template
The trigger template will create a PersistentVolumeClaim (PVC) and a PipelineRun with a workspace that uses the workspace.  Notice that $(uid) is used to create a unique id for the PVC adn workspace.

```
apiVersion: tekton.dev/v1alpha1
kind: TriggerTemplate
metadata:
  name: trigger-workspace
spec:
  resourcetemplates:
    - apiVersion: v1
      kind: PersistentVolumeClaim
      metadata:
        name: pipelinerun-$(uid)-pvc
      spec:
        resources:
          requests:
            storage:  1Gi
        volumeMode: Filesystem
        accessModes:
          - ReadWriteOnce
    - apiVersion: tekton.dev/v1alpha1
      kind: PipelineRun
      metadata:
        name: pipelinerun-$(uid)
      spec:
        pipelineRef:
            name: pipeline-workspace
        workspaces:
          - name: pipeline-workspace
            persistentVolumeClaim:
              claimName: pipelinerun-$(uid)-pvc

```

The workspace is part of the pipeline and the task connected through the name
```
apiVersion: tekton.dev/v1alpha1
kind: Pipeline
metadata:
  name: pipeline-workspace
spec:
  workspaces:
  - name: pipeline-workspace
  tasks:
    - name: task1
      workspaces:
      - name: task-workspace
        workspace: pipeline-workspace          
      taskRef:
```
