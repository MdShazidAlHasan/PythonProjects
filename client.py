import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '192.168.0.130'
PORT = 12345


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please enter you nickname")

        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "lightgrey")

        self.chatlabel = tkinter.Label(self.win, text = "Chat:", bg = "lightgrey")
        self.chatlabel.config(font=("Arial", 12))
        self.chatlabel.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(state="disabled")
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgrey")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)


        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode("ascii"))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('ascii')
                if message == "NICK":
                    self.sock.send(self.nickname.encode("ascii"))
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break

client = Client(HOST, PORT)


