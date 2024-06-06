import tkinter as tk
from tkinter import filedialog
from VahePealne import VahePealne

class GUI:
    def __init__(self, master):
        self.master = master
        self.vahepealne = VahePealne()

        self.label = tk.Label(master, text="Vali JSON-fail")
        self.label.pack(pady=20)

        self.button = tk.Button(master, text="Vali fail", command=self.open_file_dialog)
        self.button.pack()

        self.stats_label = tk.Label(master, text="Statistika:")
        self.stats_label.pack()

        self.stats_var = tk.StringVar()
        self.stats_display = tk.Label(master, textvariable=self.stats_var, wraplength=400, justify="left")
        self.stats_display.pack(pady=10)

    def open_file_dialog(self):
        filename = filedialog.askopenfilename(title="Vali JSON-fail", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        if filename:
            self.vahepealne.read_file_content(filename)
            stats = self.vahepealne.get_statistics()
            self.display_statistics(stats)

    def display_statistics(self, stats):
        stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        self.stats_var.set(stats_text)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON statistika")

    gui = GUI(root)

    root.mainloop()
