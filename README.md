# pipeline-scheduler-example

## Deprecation Notice

This step have moved to https://github.com/codefresh-io/steps/tree/master/incubating/codefresh-run-dynamic. All future updates will be in that repo.

## Directions for installing the custom typed step

1. Look up your Codefresh account name in the UI, or in the CLI via `codefresh auth get-contexts`
1. Edit `step.yaml` and replace `account-name` with your account name
1. Install the step in the CLI via `codefresh create step-type -f step.yaml`

## Directions for using the step

1. Create a `run_list.yaml` with the pipelines that you want to run. See example `example_run_list.yaml`
1. Store the `run_list.yaml` file in a git repo that you can clone from your test pipeline. Note: ultimately you would generate this file dynamically in your pipeline via a script.
1. Create a test pipeline to run the step - start with the example `./pipelines/example-parent-pipeline.yaml`
