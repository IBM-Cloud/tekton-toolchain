# lab 4 - Git
This lab extends the previous lab that created a workspace by populating the workspace with the contents of a git repository.

# Git Shared Task
A git clone task will be created in this lab.  It is generally useful so it will be placed in a shared directory that can be used by multiple pipelines.

Open the Delivery Pipeline again.  Open **Configure Pipeline**. Select the **Definitions** panel and edit to resemble the following:
|Repository|Branch|Path|
--
|https://github.com/powellquiring/tekton|master|lab4-git|
|https://github.com/powellquiring/tekton|master|shared|


Notice the **shared** directory.  Check out your forked git repo and look at the contents.  The new 


---- ---

Not using the shared git task it requires too many params
## Initialize
Before continuing another GitHub tool must be added to the toolchain.  Remember the Toolchain is the top level object that contains the pipeline.
- GitHub Server: GitHub
- Repository Type: Existing
- Repository URL: https://github.com/open-toolchain/tekton-catalog

|Repository|Branch|Path|
--
|https://github.com/powellquiring/tekton|master|lab4-git|
|https://github.com/open-toolchain/tekton-catalog|tkn_pipeline_beta_support|git|
