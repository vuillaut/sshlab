import argparse
import os
import yaml
from pathlib import Path
from . utils import kill_remote_process

DEFAULT_CONFIG_FILE = os.getenv("HOME") + "/.sshlab_config.yml"

def build_argparser():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', 
                        default=None, 
                        help='User configuration name to use (defined in the config file)')
    parser.add_argument('--file', '-f', 
                        default=DEFAULT_CONFIG_FILE,
                         type=Path,
                         help=f'YAML configuration file, default: {DEFAULT_CONFIG_FILE}')
    parser.add_argument('--process', '-p', default='jupyter', type=str,
                         help=f'Process name to kill, default: jupyter')
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

    print(f'Using configuration: {config_name}\n')

    # Get the SSH settings from the config file
    user = config['SSH']['user']
    server = config['SSH']['server']

    # Kill the remote Jupyter process
    kill_remote_process(user, server, args.process)

if __name__ == '__main__':
    main()
