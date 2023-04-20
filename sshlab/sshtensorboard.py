import subprocess
import yaml
import argparse
from pathlib import Path
import os
import signal
import atexit

import utils

DEFAULT_CONFIG_FILE = os.getenv("HOME") + "/.sshlab_config.yml"


def cleanup(user, server, process):
    # Get the PID of the remote Jupyter process
    utils.kill_remote_tensorboard(user, server)

    # Check if the process is still running
    if process.poll() is None:
        # Terminate the SSH connection
        os.kill(process.pid, signal.SIGTERM)
        print("Closed the SSH connection.")


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', default=None, 
                        help='User configuration name to use (defined in the config file)')
    parser.add_argument('--file', '-f', default=DEFAULT_CONFIG_FILE, type=Path,
                         help=f'YAML configuration file, default: {DEFAULT_CONFIG_FILE}')
    parser.add_argument('exp_names', metavar='EXP_NAMES', type=str,
                        help='Comma-separated list of experiment names')
    args = parser.parse_args()
    return args

def main():
    args = build_argparser()

    with open(args.file, 'r') as f:
        configs = yaml.safe_load(f)

    if args.config is None:
        config_name, config = next(iter(configs.items()))
    else:
        config_name = args.config
        config = configs[args.config]

    print(f'Using configuration: {config_name}\n')

    user = config['SSH']['user']
    server = config['SSH']['server']
    specified_port = int(config['SSH'].get('port', '6006'))
    ip = config['SSH'].get('ip', '127.0.0.1')

    port = specified_port if utils.is_port_available(specified_port) else utils.find_available_port(specified_port)

    ssh_cmd = f'ssh -L {port}:{ip}:{port} {user}@{server}'

    # Get the environment settings from the config file
    env_cmd = config['Environment']['cmd']
    env_target = config['Environment']['target']
    env_cmd_options = config['Environment'].get('options', '')

    # Build the tensorboard command string
    tensorboard_cmd = config['Tensorboard']['cmd']
    logdir = config['Tensorboard']['logdir']
    exp_names = args.exp_names.split(',')
    logdirs = ",".join([f'{exp_name}:{os.path.join(logdir, exp_name)}' for exp_name in exp_names])

    env_cmd = f'{env_cmd} {env_cmd_options} {env_target} {tensorboard_cmd} --logdir={logdirs} --bind_all --port {port}'

    # Combine the SSH and Singularity command strings
    cmd = f'{ssh_cmd} "{env_cmd}"'

    print(cmd)

    try:
        # Launch the command using subprocess.Popen
        process = subprocess.Popen(cmd, shell=True)

        # Register the cleanup function to be called upon script exit
        atexit.register(lambda: cleanup(user, server, process))

        # Wait for the process to complete
        process.communicate()

    except KeyboardInterrupt:
        print("\nCTRL+C detected. Terminating Jupyter process...")
        cleanup(user, server, process)


if __name__ == '__main__':
    main()
