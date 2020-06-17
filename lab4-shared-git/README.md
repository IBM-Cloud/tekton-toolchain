# lab 4 - Git

This lab extends the previous lab that created a workspace by populating the workspace with the contents of a git repository.

# Git Shared Task

A git clone task will be created in this lab. It is generally useful so it will be placed in a shared directory that can be used by multiple pipelines.

Open the Delivery Pipeline again. Open **Configure Pipeline**. Select the **Definitions** panel and edit to resemble the following:
|Repository|Branch|Path|
|-|-|-|
|https://github.com/powellquiring/tekton-toolchain|master|lab4-shared-git|
|https://github.com/powellquiring/tekton-toolchain|master|shared|

Notice the **shared** directory. Check out the shared/tasks.yaml file in your clone:

```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: clone-repo
spec:
  workspaces:
  - name: artifacts
  inputs:
    params:
    - name: repository
      description: the git repository
    - name: branch
      description: the git branch
      default: master
  steps:
    - name: clone
      image: ibmcom/pipeline-base-image
      command: ["/bin/bash", "-c"]
      args:
        - |
          WS=$(workspaces.artifacts.path)
          REPOSITORY=$(inputs.params.repository)
          BRANCH=$(inputs.params.branch)
          cd $WS
          git --version
          git clone --single-branch --branch $BRANCH $REPOSITORY
          ls $WS
```

By now this task looks familiar. The task accepts parameters for repository and branch and uses the values in the script as described in the prevous lab

The pipeline is also unsurprising. Parameters with default values hold the repository and branch. The second task is going to wait for the clone to complete before continuing. Some details are elided, take a look at the source code.

```
kind: Pipeline
spec:
  workspaces:
  - name: pipeline-workspace
  params:
  - name: repository
    default: https://github.com/powellquiring/tekton.git
  - name: branch
    default: master
  tasks:
    - name: clone
      workspaces:
      - name: artifacts
        workspace: pipeline-workspace
      taskRef:
        name: clone-repo
      params:
      - name: repository
        value: $(params.repository)
      - name: branch
        value: $(params.branch)

    - name: task1
      runAfter:
      - clone
```

---

Not using the shared git task it requires too many params

## Initialize

Before continuing another GitHub tool must be added to the toolchain. Remember the Toolchain is the top level object that contains the pipeline.

- GitHub Server: GitHub
- Repository Type: Existing
- Repository URL: https://github.com/open-toolchain/tekton-catalog

## |Repository|Branch|Path|

|https://github.com/powellquiring/tekton|master|lab4-git|
|https://github.com/open-toolchain/tekton-catalog|tkn_pipeline_beta_support|git|
