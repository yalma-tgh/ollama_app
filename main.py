# main.py
import flet as ft
import ssh_utils
import get_models
import ansible_utils
from ruamel.yaml import YAML
from time import sleep

def main(page: ft.Page):
    page.title = "SSH Hosts Dropdown"

    hosts = ssh_utils.load_hosts_from_ssh_config()
    models = get_models.get_models()

    host_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(host) for host in hosts],
        autofocus=True,
        width=450,
        label="Select SSH Host"
    )

    model_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(f"{model['name']}") for model in models],
        width=450,
        label="Select Model"
    )

    port_input = ft.TextField(
        label="Enter Port",
        value="3000",
        width=450
    )

    t = ft.Text()

    def on_submit(e):
        if host_dropdown.value is None or model_dropdown.value is None or port_input.value is None:
            t.value = "Error: Please select a host, a model, and a port!"
            page.update()
        else:
            t.value = "Running Ansible roles on the selected host..."
            page.update()

            # Update the model_name and port variables in the all.yml file
            model_name = model_dropdown.value.split(':')[0]
            port = port_input.value
            yaml = YAML()
            with open('group_vars/all.yml', 'r') as f:
                data = yaml.load(f)
            data['model_name'] = model_name
            data['port'] = port
            with open('group_vars/all.yml', 'w') as f:
                yaml.dump(data, f)

            # Run the Ansible roles
            host = host_dropdown.value
            ansible_utils.install_tool(host, 'docker')
            ansible_utils.install_tool(host, 'ollama')
            ansible_utils.install_tool(host, 'open-webui')

            # Update the UI with the results
            t.value = f"Finished!"
            page.update()
            sleep(5)  # Wait for Ansible roles to complete
            exit()

    b = ft.ElevatedButton(text="Submit", on_click=on_submit)

    container = ft.Container(
        content=ft.Column(
            controls=[
                host_dropdown,
                model_dropdown,
                port_input,
                b,
                t
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    page.add(
        ft.Row(
            controls=[container],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
