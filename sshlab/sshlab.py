import subprocess
import yaml
import argparse
from pathlib import Path
import socket
import os
import signal
import atexit

DEFAULT_CONFIG_FILE = os.getenv("HOME") + "/.sshlab_config.yml"

# Function to check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


# Function to find an available port
def find_available_port(start_port=8888):
    port = start_port
    while not is_port_available(port):
        port += 1
    return port


# Function to get the PID of the remote Jupyter process
def get_remote_jupyter_pid(user, server):
    jupyter_pid_cmd = f"ssh {user}@{server} 'pgrep -f jupyter'"
    try:
        output = subprocess.check_output(jupyter_pid_cmd, shell=True).decode().strip()
        pid = int(output)
    except (subprocess.CalledProcessError, ValueError):
        pid = None

    return pid


# Function to kill the remote Jupyter process
def kill_remote_jupyter(user, server):
    pid = get_remote_jupyter_pid(user, server)
    if pid:
        kill_cmd = f"ssh {user}@{server} 'kill -TERM {pid} &> /dev/null'"
        subprocess.run(kill_cmd, shell=True)
        print(f"Terminated the Jupyter server {pid} on the remote machine.")


def cleanup(user, server, process):
    # Get the PID of the remote Jupyter process
    kill_remote_jupyter(user, server)

    # Check if the process is still running
    if process.poll() is None:
        # Terminate the SSH connection
        os.kill(process.pid, signal.SIGTERM)
        print("Closed the SSH connection.")


def build_argparser():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', default=None, help='User configuration name to use (defined in the config file)')
    parser.add_argument('--file', '-f', default=DEFAULT_CONFIG_FILE, type=Path, help=f'YAML configuration file, default: {DEFAULT_CONFIG_FILE}')
    args = parser.parse_args()
    return args


def main():

    args = build_argparser()

    # Read the configuration file
    with open(args.file, 'r') as f:
        configs = yaml.safe_load(f)

    if args.config is None:
        config_name, config = next(iter(configs.items()))
    else:
        config_name = args.config
        config = configs[args.config]

    print(f'Using configuration: {config_name}')

    # Get the SSH settings from the config file
    user = config['SSH']['user']
    server = config['SSH']['server']
    specified_port = int(config['SSH'].get('port', '8888'))
    ip = config['SSH'].get('ip', '127.0.0.1')

    # Check if the specified port is available, and find an available port if it's not
    port = specified_port if is_port_available(specified_port) else find_available_port(specified_port)

    # Build the SSH command string
    ssh_cmd = f'ssh -L {port}:{ip}:{port} {user}@{server}'

    # Get the environment settings from the config file
    env_cmd = config['Environment']['cmd']
    env_target = config['Environment']['target']
    env_cmd_options = config['Environment'].get('options', '')

    # Get the Jupyter settings from the config file
    jupyter_flavor = config['Jupyter']['flavor']
    jupyter_options = config['Jupyter'].get('options', '')

    # Build the Singularity command string
    env_cmd = f'{env_cmd} {env_cmd_options} {env_target} jupyter {jupyter_flavor} {jupyter_options} --port={port} --ip={ip}'

    # Combine the SSH and Singularity command strings
    cmd = f'{ssh_cmd} "{env_cmd}"'

    # Launch the command using subprocess.Popen
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)

    # Register the cleanup function to be called upon script exit
    atexit.register(lambda: cleanup(user, server, process))

    # Wait for the process to complete
    process.communicate()


if __name__ == '__main__':
    main()