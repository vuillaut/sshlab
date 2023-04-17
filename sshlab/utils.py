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


# Function to get the PID of the remote Jupyter process
def get_remote_jupyter_pid(user, server):
    jupyter_pid_cmd = f"ssh {user}@{server} 'pgrep -f jupyter -u {user}'"
    try:
        output = subprocess.check_output(jupyter_pid_cmd, shell=True).decode().strip().split('\n')[0].strip()
        pid = int(output)
    except (subprocess.CalledProcessError, ValueError):
        pid = None

    return pid


def kill_remote_jupyter(user, server):
    pid = get_remote_jupyter_pid(user, server)
    
    if pid:
        print(f"Jupyter server PID on remote machine: {pid}")
        kill_cmd = f"ssh {user}@{server} 'kill -TERM {pid} &> /dev/null'"
        subprocess.run(kill_cmd, shell=True)
        print(f"Sent termination signal to Jupyter server {pid} on the remote machine.")
        
        # Wait for the Jupyter process to terminate
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            time.sleep(1)
            current_pid = get_remote_jupyter_pid(user, server)
            if not current_pid:
                print(f"Terminated the Jupyter server {pid} on the remote machine.")
                break
            else:
                print(f"Jupyter server {pid} still running. Retry count: {retry_count}")
            retry_count += 1
        else:
            print(f"Unable to terminate the Jupyter server {pid} on the remote machine.")
    else:
        print("No Jupyter server found on the remote machine.")
