import flet as ft
import ssh_utils

from ansible_utils import install_tool


def main(page: ft.Page):
    page.title = "SSH Hosts Dropdown"

    hosts = ssh_utils.load_hosts_from_ssh_config()

    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(host) for host in hosts],
        autofocus=True,
        width=450
    )

    domain_input = ft.TextField(
        label="Enter Domain",
        width=450
    )

    t = ft.Text()

    def on_submit(e):
        if not dropdown.value:
            t.value = "Error: Please select a host!"
        else:
            t.value = "Running Ansible roles on the selected host..."
            page.update()

            # Run the Ansible roles
            host = dropdown.value
            install_tool(host, 'docker')
            install_tool(host, 'ollama')

            # Update the UI with the results
            t.value = f"Finished!"
            page.update()

    b = ft.ElevatedButton(text="Submit", on_click=on_submit)

    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Select SSH Host", size=24, weight="bold"),
                dropdown,
                domain_input,
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
