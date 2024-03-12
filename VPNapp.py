import asyncio
import uvloop
import tkinter as tk
from tkinter import messagebox
from threading import Thread

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class VPNServer:
    def __init__(self, hosts_ports):
        self.hosts_ports = hosts_ports
        self.server_tasks = []

    async def handle_client(self, reader, writer):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            response = self.process_data(data)
            writer.write(response)
            await writer.drain()
        writer.close()

    def process_data(self, data):
        # Process data here (e.g., encrypt/decrypt)
        return data

    async def start_servers(self):
        for host, port in self.hosts_ports:
            task = asyncio.create_task(
                asyncio.start_server(self.handle_client, host, port)
            )
            self.server_tasks.append(task)
            print(f'Serving on {host}:{port}')
            await task

    async def stop_servers(self):
        for task in self.server_tasks:
            task.cancel()
            await task
            print('Server stopped')

class VPNApp:
    def __init__(self, master):
        self.master = master
        master.title("VPN Server App")

        self.start_button = tk.Button(master, text="Start VPN Server", command=self.start_server)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop VPN Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack()

    def start_server(self):
        self.vpn_server = VPNServer([('0.0.0.0', 1194), ('0.0.0.0', 1195)])  # Example: Listen on two different ports
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        self.vpn_server.stop_servers()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_server(self):
        try:
            asyncio.run(self.vpn_server.start_servers())
        except asyncio.CancelledError:
            pass

def main():
    root = tk.Tk()
    app = VPNApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
