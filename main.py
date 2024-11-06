# main.py
import flet as ft
import ssh_utils
import get_models
import ansible_utils
import yaml

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

    t = ft.Text()

    def on_submit(e):
        if host_dropdown.value is None or model_dropdown.value is None:
            t.value = "Error: Please select a host and a model!"
            page.update()
        else:
            t.value = "Running Ansible roles on the selected host..."
            page.update()

            # Update the model_name variable in the all.yml file
            model_name = model_dropdown.value.split(':')[0]
            with open('group_vars/all.yml', 'r') as f:
                data = yaml.safe_load(f)
            data['model_name'] = model_name
            with open('group_vars/all.yml', 'w') as f:
                yaml.safe_dump(data, f)

            # Run the Ansible roles
            host = host_dropdown.value
            ansible_utils.install_tool(host, 'docker')
            ansible_utils.install_tool(host, 'ollama')
            ansible_utils.install_tool(host, model_name)

            # Update the UI with the results
            t.value = f"Finished!"
            page.update()

    b = ft.ElevatedButton(text="Submit", on_click=on_submit)

    container = ft.Container(
        content=ft.Column(
            controls=[
                host_dropdown,
                model_dropdown,
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
