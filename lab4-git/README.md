# lab 4 - Git
This lab extends the previous lab that created a workspace by populating the workspace with the contents of a git repository.

## Initialize
Before continuing another GitHub tool must be added to the toolchain.  Remember the Toolchain is the top level object that contains the pipeline.
- GitHub Server: GitHub
- Repository Type: Existing
- Repository URL: https://github.com/open-toolchain/tekton-catalog

Open the Delivery Pipeline again.  Open **Configure Pipeline**. Select the **Definitions** and edit to resemple the following:
|Repository|Branch|Path|
--
|https://github.com/powellquiring/tekton|master|lab4-git|
|https://github.com/open-toolchain/tekton-catalog|tkn_pipeline_beta_support|git|

IBM is proivding a catalog of tasks.  The git task is used to clone a repository into a workspace.  Currently the tkn_pipeline_beta_support is required, but it will soon be in the master branch.


---- ---

