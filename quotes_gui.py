import json
import random
import tkinter as tk
from random import choice

with open("data/quote_data.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)


class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quote App")
        self.quote, self.author, self.work = self.random_quote()

        self.quote_label = tk.Label(
            self.root, text=self.quote, wraplength=600, justify=tk.LEFT
        )
        self.quote_label.config(font=("Helvetica", 16))
        self.quote_label.pack(pady=10)

        self.author_label = tk.Label(
            self.root,
            text=f"- {self.author}, {self.work}",
            wraplength=600,
            justify=tk.RIGHT,
        )
        self.author_label.config(font=("Helvetica", 12))
        self.author_label.pack()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        self.input_label = tk.Label(self.input_frame, text="Enter command:")
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT)

        self.input_button = tk.Button(
            self.input_frame, text="Submit", command=self.process_input
        )
        self.input_button.pack(side=tk.LEFT)

        self.root.bind("<Return>", self.show_new_quote)

        self.help_label = tk.Label(
            self.root,
            text="Available commands: [s] start slide, [m] move quotes, [sa] same author quotes, [msa] move same author quotes",
        )
        self.help_label.pack(pady=10)

    def random_quote(self):
        quote = random.choice(quotes)
        quote_text, author, work = (
            quote["quote"],
            quote["author"],
            quote.get("work", ""),  # handle work not existing
        )
        # wrapped_quote = textwrap.fill(quote_text, width=100)
        # print(f"{wrapped_quote}\n\n- {author} {work if len(work) > 0 else ''}")
        return quote_text, author, work

    def show_new_quote(self, event):
        self.quote, self.author, self.work = self.random_quote()
        self.quote_label.config(text=self.quote)
        self.author_label.config(text=f"- {self.author}, {self.work}")

    def process_input(self):
        input_text = self.input_entry.get()
        if input_text == "s":
            # Start slide code here
            print("Starting slide...")
        elif input_text == "m":
            # Move quotes code here
            print("Moving quotes...")
        elif input_text == "sa":
            # Same author quotes code here
            print("Showing same author quotes...")
        elif input_text == "msa":
            # Move same author quotes code here
            print("Moving same author quotes...")
        else:
            print("Invalid command. Please try again.")

        self.input_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
