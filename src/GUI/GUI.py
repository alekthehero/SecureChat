import tkinter as tk
from src.Server.TCPServer import TCPServer
from src.Client.Client import Client


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.title('Multi-Screen GUI')

        self.resizable(False, False)
        self.attributes('-fullscreen', False)

        self.frames = {}

        frame = MainPage(self)  # Create the frame
        self.frames[MainPage] = frame
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configure the grid to expand the frame to fill the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind the close protocol to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.show_frame(MainPage)

        self.mainloop()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def on_close(self):
        self.destroy()


class MainPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.server_window = None
        self.client_windows = []

        title = tk.Label(self, text='Welcome to the ssl test application!')
        title.grid(row=0, column=0, pady=10, sticky='ew')

        slider_label = tk.Label(self, text="Select the number of clients:")
        slider_label.grid(row=1, column=0, pady=10, sticky='ew')

        slider = tk.Scale(self, from_=1, to=10, orient='horizontal')
        slider.grid(row=2, column=0, pady=10, sticky='ew')

        client_button = tk.Button(self, text="Start Clients", command=lambda: self.start_clients(slider.get()))
        client_button.grid(row=3, column=0, pady=10, sticky='ew')

        server_button = tk.Button(self, text="Start Server", command=lambda: self.start_server())
        server_button.grid(row=4, column=0, pady=10, sticky='ew')

        self.grid_columnconfigure(0, weight=1)

    def start_clients(self, num_clients):
        # Filter out closed client windows first
        self.client_windows = [client for client in self.client_windows if client.winfo_exists()]

        for _ in range(num_clients):
            client_window = ClientPage(self.master)
            self.client_windows.append(client_window)

        print(f"Total clients: {len(self.client_windows)}")

    def start_server(self):
        self.server_window = ServerPage(self.master)


class ServerPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.TCP_server = None

        self.title("Server")
        self.geometry("400x400")

        self.resizable(False, False)
        self.attributes('-fullscreen', False)

        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text='Server is Running!')
        title.grid(row=0, column=0, pady=10, sticky='ew')

        self.log = tk.Text(self)
        self.log.grid(row=1, column=0, pady=10, sticky='news', padx=10)
        self.grid_rowconfigure(1, weight=1)

        button = tk.Button(self, text="Stop Server", command=lambda: self.stop_server())
        button.grid(row=2, column=0, pady=10, padx=10, sticky='ew')

        self.start_server()

    def start_server(self):
        self.TCP_server = TCPServer('localhost', 12345, self.log_server_message)

    def stop_server(self):
        self.TCP_server.close()
        self.TCP_server.server_thread.join()
        self.destroy()

    def log_server_message(self, message):
        # Tkinter is not thread safe so this makes it safe
        self.log.after(0, lambda: self.log.insert(tk.END, message + '\n'))


class ClientPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Client")
        self.geometry("400x400")

        self.resizable(False, False)
        self.attributes('-fullscreen', False)

        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text='Client is Running!')
        title.grid(row=0, column=0, pady=10, sticky='ew')

        label = tk.Label(self, text="Enter your username and password:")
        label.grid(row=1, column=0, pady=10, sticky='ew')

        username = tk.Entry(self)
        username.grid(row=2, column=0, pady=10, padx=10, sticky='ew')

        password = tk.Entry(self)
        password.grid(row=3, column=0, pady=10, padx=10, sticky='ew')

        login = tk.Button(self, text="Login", command=lambda: self.login(username.get(), password.get()))
        login.grid(row=4, column=0, pady=10, padx=10, sticky='ew')

        register = tk.Button(self, text="Register", command=lambda: self.register_acc(username.get(), password.get()))
        register.grid(row=5, column=0, pady=10, padx=10, sticky='ew')

        self.response = tk.Label(self, text="")
        self.response.grid(row=6, column=0, pady=10, sticky='ew')

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.client_connection = Client(self.logger)

    def login(self, username, password):
        self.client_connection.send_login(username, password)

    def register_acc(self, username, password):
        self.client_connection.send_create(username, password)

    def logger(self, message):
        # makes the logger thread safe
        self.response.after(0, lambda: self.response.config(text=message))

    def on_close(self):
        self.destroy()
