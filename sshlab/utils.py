import socket
import subprocess
import time


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


def get_remote_cmd_pid(user, server, cmd):
    pid_cmd = f"ssh {user}@{server} 'pgrep -f \"{cmd}\" -u {user}'"
    try:
        output = subprocess.check_output(pid_cmd, shell=True).decode().strip().split('\n')[0].strip()
        pid = int(output)
    except (subprocess.CalledProcessError, ValueError):
        pid = None

    return pid


def get_remote_jupyter_pid(user, server):
    jupyter_cmd = 'jupyter'
    return get_remote_cmd_pid(user, server, jupyter_cmd)


def get_remote_tensorboard_pid(user, server):
    tensorboard_cmd = 'tensorboard'
    return get_remote_cmd_pid(user, server, tensorboard_cmd)


def kill_remote_process(user, server, cmd):
    pid = get_remote_cmd_pid(user, server, cmd)
    print(f"PID {pid}")
    
    if pid:
        print(f"Process PID on remote machine: {pid}")
        kill_cmd = f"ssh {user}@{server} 'kill -TERM {pid} &> /dev/null'"
        subprocess.run(kill_cmd, shell=True)
        print(f"Sent termination signal to process {pid} on the remote machine.")
        
        # Wait for the process to terminate
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            time.sleep(1)
            current_pid = get_remote_cmd_pid(user, server, cmd)
            if not current_pid:
                print(f"Terminated the process {pid} on the remote machine.")
                break
            else:
                print(f"Process {pid} still running. Retry count: {retry_count}")
            retry_count += 1
        else:
            print(f"Unable to terminate the process {pid} on the remote machine.")
    else:
        print("No process found on the remote machine.")


def kill_remote_jupyter(user, server):
    jupyter_cmd = 'jupyter'
    kill_remote_process(user, server, jupyter_cmd)


def kill_remote_tensorboard(user, server):
    tensorboard_cmd = 'tensorboard'
    kill_remote_process(user, server, tensorboard_cmd)


def delete_remote_dir(user, server, dir_path):
    print(f"Deleting temporary directory {dir_path} on the remote machine.")
    delete_cmd = f"ssh {user}@{server} 'rm -rf {dir_path}'"
    subprocess.run(delete_cmd, shell=True)
