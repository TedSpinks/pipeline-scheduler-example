#!/usr/bin/env python3

""" Run a codefresh pipeline build for each list item in a provided scheduling YAML file.
    Required environment variables:
      - SCHEDULE_FILE = path to the schduling YAML file
      - DEPLOY_PIPELINE = name of the pipeline to run, format: project/pipeline
      - DEPLOY_TRIGGER = name of the trigger within the pipeline to run (includes the Git repo)
      - DEPLOY_BRANCH = Git branch
    Optional environment variables
      - LOG_LEVEL = set the logging level (ex: DEBUG)
"""

import os           # to read env vars
import logging
import subprocess   # to run codefresh process
import yaml

def run_cmd(cmd, args_with_spaces=[], input=None, fail_on_non_zero=True, no_log_cmd=False):
    """Run a command in the OS. Any command args that contain spaces should be 
    passed separately in the args_with_spaces list param (don't include quotes)"""
    log_cmd = cmd
    for arg in args_with_spaces:
        log_cmd += " " + arg
    if no_log_cmd: log_cmd = "[REDACTED]"
    print(log_cmd)
    result = subprocess.run(cmd.split() + args_with_spaces, 
        input=input, 
        stdout=subprocess.PIPE,   # send stderr to stdout
        stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8').rstrip()
    returncode = result.returncode
    summary = "\n  Command: {}".format(log_cmd) + \
                "\n  Return code: {}".format(returncode) + \
                "\n  Output:\n{}".format(output)
    if fail_on_non_zero: assert(returncode == 0), summary
    return output, returncode

def verify_input_file_structure(input_file_dict):
    """ Parse the dict representation of the input YAML file. Loops through all the
        schedule elements and makes sure they contain the needed structure.
    """
    logging.debug("Parsing input file to validate tree structure...")
    try:
        deployment_list = input_file_dict['deployments']
    except KeyError:
        logging.error("Input file does not contain any deployments.")
        raise
    assert (isinstance(deployment_list, list)), "Input file does not contain any deployments."
    for deployment in deployment_list:
        logging.debug(deployment)
        assert (type(deployment) is dict), "Deployment list element is not a dictionary"
        # TODO - add more validation here as needed
    logging.debug("Finished validating tree structure.")

def set_logging(log_level_env_var):
    """ Log level is INFO unless a valid LOG_LEVEL env var was provided
    """
    log_level = 'WARN'  # Default log level
    if str(log_level_env_var).upper() in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        log_level = log_level_env_var
    logging.basicConfig(level=log_level)

def get_inputs_from_env_vars():
    # Required environment variables
    schedule_file = os.environ.get("SCHEDULE_FILE")
    if not schedule_file:
        raise ValueError("Missing required environment variable: SCHEDULE_FILE.")
    deploy_pipeline = os.environ.get("DEPLOY_PIPELINE")
    if not deploy_pipeline:
        raise ValueError("Missing required environment variable: DEPLOY_PIPELINE.")
    deploy_trigger = os.environ.get("DEPLOY_TRIGGER")
    if not deploy_trigger:
        raise ValueError("Missing required environment variable: DEPLOY_TRIGGER.")
    deploy_branch = os.environ.get("DEPLOY_BRANCH")
    if not deploy_branch:
        raise ValueError("Missing required environment variable: DEPLOY_BRANCH.")
    # Not required
    log_level_env_var = os.environ.get('LOG_LEVEL')
    return schedule_file, deploy_pipeline, deploy_trigger, deploy_branch, log_level_env_var

def main():
    # Read env vars
    schedule_file, deploy_pipeline, deploy_trigger, deploy_branch, log_level_env_var = get_inputs_from_env_vars()
    
    # Set log level
    set_logging(log_level_env_var)
    logging.debug("Pipeline to run is '{}'".format(deploy_pipeline))

    # Read scheduling info from input YAML file
    with open(schedule_file, "r") as read_file:
        schedule_info = yaml.load(read_file, Loader=yaml.SafeLoader)
    verify_input_file_structure(schedule_info)

    # Execute pipeline per schedule
    logging.debug("Processing list of deployments...")
    for deployment in schedule_info['deployments']:
        logging.debug(deployment)
        client = deployment['client']
        region = deployment['region']
        env = deployment['env']
        fulllayerpath = deployment['fulllayerpath']
        cmd = "codefresh run"
        cmd_args = [deploy_pipeline, "--detach", "-t=" + deploy_trigger, "-b=" + deploy_branch, "-v=CLIENT=" + client,
            "-v=REGION=" + region, "-v=ENV=" + env, "-v=FULLLAYERPATH=" + fulllayerpath]
        output, exit_code = run_cmd(cmd, cmd_args)
        print("\nStarted build https://g.codefresh.io/build/" + output + "\n")

if __name__ == "__main__":
    main()