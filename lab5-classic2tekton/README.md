# Example Upgrade
In this lab an existing toolchain with a classic pipeline will be converted to a Tekton pipeline.

# Existing Toolchain
The solution tutorial: [Apply end to end security to a cloud application](https://cloud.ibm.com/docs/tutorials?topic=solution-tutorials-cloud-e2e-security) has a toolchain that can be found here: https://github.com/IBM-Cloud/secure-file-storage.  If you followed along on the previous labs all of the concepts have been introduced to implement the classic pipeline to tekton.

The toolchain can be found here: https://github.com/IBM-Cloud/secure-file-storage.  Notice the .bluemix/ directory where the template for a toolchain can be observed.  Also notice the README.md file where the `Create toolchain` button is located which invokes the `deploy` cloud function with the parameters for the repository (this repository), env_id (data center), and type (tekton or classic)

```
[![Create toolchain](https://cloud.ibm.com/devops/graphics/create_toolchain_button.png)](https://cloud.ibm.com/devops/setup/deploy/?repository=https%3A//github.com/IBM-Cloud/secure-file-storage&env_id=ibm:yp:us-south&type=tekton)
```

The .bluemix/toolchain.yml file in the repository contains the contents of the toolchain.  You can find a tutorial here: https://www.ibm.com/cloud/architecture/tutorials/create-a-template-for-a-custom-toolchain  Here are some highlights.

toolchain.yml:
```
    service_id: pipeline
      type: $env.type
      configuration:
        content:
          $text: >
            $env.type + '.yml'

```

The $env.type is provided by the url parameter `type=tekton` and the type will be tekton and the file that provides the pipeline is tekton.yml.

tekton.yml inputs show up in the Definitions portion of the pipeline configuration.  Notice it is identifying the .tekton/ folder in the repository. All of the tekton files in this location will be added to the pipeline.
```
inputs:
- type: git
  branch: ${GIT_BRANCH}
  path: .tekton
  service: repo
```

properties are reflected in the Environment properties:
```
properties:
- name: GIT_REPO
  value: ${GIT_REPO_URL} 
  type: text 
...

```

triggers are reflected in the trigger panel:
```
triggers:
- eventListener: BUILD
  name: BUILD
  type: manual
```

# Converting to tekton
The classic pipelines had jobs and stages which are similar to tekton Pipelines and Tasks.

For example the classic DEPLOY job:
```
- name: DEPLOY
  inputs:
  - type: job
    stage: BUILD
    job: Build Docker image
  triggers:
  - type: stage
  properties:
  - name: buildprops
    value: build.properties
    type: file
  - name: TARGET_NAMESPACE
    value: ${TARGET_NAMESPACE}
    type: text
...
  jobs:
  - name: Deploy
    type: deployer
    target:
      region_id: ${TARGET_REGION_ID}
      api_key: ${API_KEY}
      kubernetes_cluster: ${TARGET_CLUSTER_NAME}
      resource_group: ${TARGET_RESOURCE_GROUP}
    script: |
      #!/bin/bash
      ./scripts/pipeline-DEPLOY.sh
```

Remember the .tekton/ directory will contain the tekton files and now we are back to familiar territory.  all.yaml:
```
apiVersion: tekton.dev/v1beta1
kind: EventListener
metadata:
  name: DEPLOY
spec:
  triggers:
  - binding:
      name: pipeline-DEPLOY
    template:
      name: tt-common
---
apiVersion: tekton.dev/v1beta1
kind: TriggerBinding
metadata:
  name: pipeline-DEPLOY
spec:
  params:
  - name: script
    value: ./scripts/pipeline-DEPLOY.sh
```

Notice how the TriggerBinding adds the parameter: script.  This is the same script used in the classic pipeline.  Here is a cut down of the Trigger Template:
```
kind: TriggerTemplate
metadata:
  name: tt-common
spec:
  params:
  - name: script
  resourcetemplates:
  - kind: PipelineRun
    spec:
      pipelineRef:
        name: pipeline-input-parameter-variable
      workspaces:
      - name: pipeline-workspace
        persistentVolumeClaim:
          claimName: pipelinerun-$(uid)-pvc
      params:
      - name: script
        value: $(params.script)

Notice how the workspace is created.  And the script to execute is passed to the created pipeline.  This way the same pipeline can be used for all of the EventListeners:
```
kind: Pipeline
metadata:
  name: pipeline-input-parameter-variable
spec:
  workspaces:
  - name: pipeline-workspace
  params:
    - name: script
      value: $(params.script)
    taskRef:
      name: gasket
```

The gasket Task is responsible for setting up the environment that allows the script to be executed.  This configuration was part of the classic runtime environment for Kubernetes deployment:
```
kind: Task
metadata:
  name: gasket
spec:
  workspaces:
  - name: task-workspace 
    mountPath: /working   
  inputs:
    - name: script
  steps:
  - env:
    - name: script
      value: $(inputs.params.script)
    command: ["/bin/bash", "-c"]
    args:
    - |
      env
      # BUILD needs this:
      export ARCHIVE_DIR=.
...
      bash $script

```
