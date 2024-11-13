import os
import shutil
import ansible_runner
import tempfile
import logging

def setup_runner_environment(host, play_source, custom_roles_path=None):
    base_path = tempfile.mkdtemp(prefix="ansible_runner_")
    project_path = os.path.join(base_path, 'project')
    roles_path = os.path.join(project_path, 'roles')
    inventory_path = os.path.join(base_path, 'inventories')
    group_vars_path = os.path.join(project_path, 'group_vars')

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(roles_path, exist_ok=True)
    os.makedirs(inventory_path, exist_ok=True)
    os.makedirs(group_vars_path, exist_ok=True)

    # ایجاد فایل Playbook
    playbook_path = os.path.join(project_path, 'playbook.yml')
    with open(playbook_path, 'w') as playbook_file:
        playbook_file.write(play_source)

    # کپی کردن نقش‌ها
    roles_src_path = os.path.join(os.path.dirname(__file__), 'roles')
    if os.path.exists(roles_src_path):
        shutil.copytree(roles_src_path, roles_path, dirs_exist_ok=True)

    # کپی کردن group_vars
    group_vars_src_path = os.path.join(os.path.dirname(__file__), 'group_vars')
    if os.path.exists(group_vars_src_path):
        shutil.copytree(group_vars_src_path, group_vars_path, dirs_exist_ok=True)

    # تنظیم فایل inventory
    hosts_path = os.path.join(inventory_path, 'hosts')
    with open(hosts_path, 'w') as hosts_file:
        if host:
            if isinstance(host, str):
                if host == 'localhost':
                    hosts_file.write('[all]\nlocalhost ansible_connection=local')
                else:
                    hosts_file.write('[all]\n' + host)
            else:
                hosts_file.write('[all]\n' + '\n'.join(host))
        else:
            hosts_file.write('[all]\nlocalhost ansible_connection=local')

    logging.debug("Contents of inventory file:")
    with open(hosts_path, 'r') as file:
        logging.debug(file.read())

    return base_path, 'playbook.yml', inventory_path

def install_tool(host, role_name, custom_roles_path=None, use_local_connection=False, password=None):
    play_source = f"""
---
- name: Install and configure {role_name}
  hosts: all
  become: true
  become_method: sudo
  roles:
    - {role_name}
    """
    logging.debug(f"Generated Playbook For {host}:\n{play_source}")
    base_path, playbook_name, inventory_path = setup_runner_environment(host, play_source, custom_roles_path)
    logging.debug(f"Running Ansible Runner with playbook at {os.path.join(base_path, playbook_name)}")

    envvars = {
        'ANSIBLE_STDOUT_CALLBACK': 'default',
        'ANSIBLE_LOAD_CALLBACK_PLUGINS': 'True',
        'ANSIBLE_BECOME_ASK_PASS': 'True',  # درخواست رمز عبور برای sudo
    }

    if password is not None:
        envvars['ANSIBLE_BECOME_PASS'] = password

    if use_local_connection:
        envvars['ANSIBLE_CONNECTION'] = 'local'

    r = ansible_runner.run(
        private_data_dir=base_path,
        playbook=playbook_name,
        inventory=inventory_path,
        envvars=envvars,
        verbosity=1
    )
    logging.debug(f"Ansible Runner finished with status: {r.status}")

    # پیدا کردن فایل‌های لاگ
    log_dir = os.path.join(base_path, 'artifacts')
    logs = "No log file found."
    if os.path.exists(log_dir):
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                if file == 'stdout':
                    log_file = os.path.join(root, file)
                    with open(log_file, 'r') as f:
                        logs = f.read()
                        break
    else:
        logging.warning("Log directory does not exist.")

    # پاک کردن دایرکتوری موقت پس از اجرا
    shutil.rmtree(base_path, ignore_errors=True)

    return logs if logs != "No log file found." else r.status
