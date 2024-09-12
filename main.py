import os
import paramiko
import flet as ft
from pprint import pprint

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

def main(page: ft.Page):
    page.title = "SSH Hosts Dropdown"
    
    hosts = load_hosts_from_ssh_config()

    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(host) for host in hosts],
        autofocus=True,
        width=450
    )
    
    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=lambda e: (setattr(t, 'value', f"Dropdown value is: {dropdown.value}"), page.update()))
    
    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Select SSH Host", size=24, weight="bold"),
                dropdown,
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

ft.app(target=main)
