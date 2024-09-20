import os
import paramiko

def load_hosts_from_ssh_config():
    ssh_config_path = os.path.expanduser("~/.ssh/config")
    ssh_config = paramiko.SSHConfig()

    try:
        with open(ssh_config_path, 'r') as file:
            ssh_config.parse(file)

        hosts = [entry.get('host')[0] for entry in ssh_config._config if entry.get('host') and len(entry.get('config'))]
        return hosts

    except FileNotFoundError:
        return ["File not found"]
    except PermissionError:
        return ["Permission denied"]
    except Exception as e:
        return [f"An error occurred: {e}"]
    

if __name__ == "__main__":

    print(10)  