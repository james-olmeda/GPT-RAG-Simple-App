import tkinter as tk
from tkinter.font import Font
import threading

from orchestrator_request import chatgpt
from flask import json

class Chat:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Chat")
        self.main_window.geometry("600x600")

        self.chat_font = Font(family="Helvetica", size=16)

        self.chat_window = tk.Text(self.main_window, state=tk.DISABLED, wrap=tk.WORD, font=self.chat_font)
        self.chat_window.tag_configure('right', justify='right')
        self.chat_window.tag_configure('left',  justify='left')
        self.chat_window.pack(padx=10, pady=10, expand=True, fill='both')

        self.entry = tk.Entry(self.main_window, width=30)
        self.entry.pack(padx=10, pady=10, fill='x', expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.main_window, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side='right')

    def fetch_gpt_response(self, user_message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"\n\nGPT: ", 'left')
        self.chat_window.config(state=tk.DISABLED)

        response_text = chatgpt(user_message)
        response_data = json.loads(response_text)

        # Extract the "answer" field
        response = response_data.get("answer")
        print(f"Response from GPT: {response}")
        for partial_response in response:
            self.main_window.after(0, self.update_chat_window, partial_response, True)

        self.main_window.after(0, self.update_chat_window, "\n\n", True)

    def update_chat_window(self, response, append=False):
        self.chat_window.config(state=tk.NORMAL)

        if append:
            self.chat_window.insert(tk.END, response)
        else:
            self.chat_window.insert(tk.END, f"\n\nGPT: {response}\n\n", 'left')
        self.chat_window.config(state=tk.DISABLED)

    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message:
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.insert(tk.END, f"\n\nUser: {user_message}  \n\n", 'right')
            self.chat_window.config(state=tk.DISABLED)
            self.entry.delete(0, tk.END)
            threading.Thread(target=self.fetch_gpt_response, args=(user_message,)).start()

    def run(self):
        self.main_window.mainloop()


