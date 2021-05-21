# pipeline-scheduler-example

## Directions for installing the custom typed step

1. Look up your Codefresh account name in the UI or CLI
    codefresh auth get-contexts
1. Edit step.yaml and replace account-name with your account name
1. Install the step.yaml
    codefresh create step-type -f step.yaml

## Directions for using the step

1. Create a run_list.yaml with the pipelines that you want to run. Ultimately you would generate this file dynamically in your pipeline via a script.
1. Store the run_list.yaml file in a git repo that you can clone from your test pipeline
1. Create a test pipeline to run the step - start with the example ./pipelines/example-parent-pipeline.yaml