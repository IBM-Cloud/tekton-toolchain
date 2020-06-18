# lab 3

This lab focuses on workspaces.

A workspace is a disk volume made available to a task.

## Initialize

If continuing from the previous lab:

Open the **Pipeline Service**
Open the **Delivery Pipeline**

- Select the **Definitions** panel and edit to resemble the following:

| Repository                              | Branch | Path            |
| --------------------------------------- | ------ | --------------- |
| https://github.com/powellquiring/tekton-toolchain | master | lab3-workspaces |

## Trigger Template

The trigger template will create a PersistentVolumeClaim (PVC) and a PipelineRun with a workspace that uses the workspace. Notice that \$(uid) is used to create a unique id for the PVC adn workspace.

```
apiVersion: tekton.dev/v1beta1
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
    - apiVersion: tekton.dev/v1beta1
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

The workspace in the PipelineRun is named pipeline-workspace and is available in the Pipeline via the same name. Notice how it is referenced by name within the task list and available to the task by the name task-workspace.

```
apiVersion: tekton.dev/v1beta1
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

Finally it is available in the task where \$(workspaces.task-workspace.path) will reference the mounted directory of the workspace. The code will list the contents (initially empty) and add a string to a file. The second time this task is run observe the file exists and will end containing two strings.

```
kind: Task
metadata:
  name: task-workspace
spec:
  workspaces:
  - name: task-workspace
    # mountPath: /artifacts
  steps:
    - name: echoenvvar
      image: ubuntu
      command: ["/bin/bash", "-c"]
      args:
        - |
          set -x
          echo 00 lab3
          WS=$(workspaces.task-workspace.path)
          ls $WS
          cd $WS
          echo hi >> hi
          ls $WS
          cat hi
```
