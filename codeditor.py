import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess

class MultiLanguageCompiler:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Language Compiler")
        self.root.geometry("1000x800")
        self.root.configure(bg="#2E3440")
        self.root.overrideredirect(True)  # Remove default title bar

        # Custom title bar
        self.title_bar = tk.Frame(self.root, bg="#3B4252", relief="raised", bd=0)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(self.title_bar, text="Multi-Language Compiler", bg="#3B4252", fg="#D8DEE9", font=("Arial", 10))
        self.title_label.pack(side="left", padx=10)

        self.close_button = tk.Button(self.title_bar, text="X", bg="#3B4252", fg="#D8DEE9", bd=0, command=self.root.destroy, font=("Arial", 10))
        self.close_button.pack(side="right", padx=10)

        # Gradient background
        self.canvas = tk.Canvas(self.root, bg="#2E3440", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Language selection
        self.language_var = tk.StringVar(value="Python")
        self.language_menu = ttk.Combobox(self.canvas, textvariable=self.language_var, values=[
            "Python", "C", "C++", "JavaScript", "Java", "PHP", "Ruby", "CSS", "HTML"
        ], font=("Arial", 12), state="readonly")
        self.language_menu.place(relx=0.5, rely=0.1, anchor="center", width=200, height=30)

        # Create a Text widget for code editing
        self.code_area = scrolledtext.ScrolledText(self.canvas, wrap="word", font=("Consolas", 14), bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9", bd=0, relief="flat")
        self.code_area.place(relx=0.5, rely=0.4, anchor="center", width=900, height=300)

        # Create a Run button with rounded corners and shadow
        self.run_button = tk.Button(self.canvas, text="Run", command=self.run_code, font=("Arial", 12), bg="#81A1C1", fg="#2E3440", activebackground="#88C0D0", activeforeground="#2E3440", bd=0, padx=20, pady=10, relief="flat")
        self.run_button.place(relx=0.5, rely=0.7, anchor="center")

        # Output area
        self.output_area = scrolledtext.ScrolledText(self.canvas, wrap="word", font=("Consolas", 14), bg="#3B4252", fg="#D8DEE9", state="disabled", bd=0, relief="flat")
        self.output_area.place(relx=0.5, rely=0.9, anchor="center", width=900, height=200)

        # Bind events for custom title bar
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def run_code(self):
        """Run the code in the selected language."""
        code = self.code_area.get(1.0, tk.END)
        language = self.language_var.get()

        try:
            if language == "Python":
                result = subprocess.run(["python", "-c", code], capture_output=True, text=True)
            elif language == "C":
                with open("temp.c", "w") as f:
                    f.write(code)
                result = subprocess.run(["gcc", "temp.c", "-o", "temp"], capture_output=True, text=True)
                if result.returncode == 0:
                    result = subprocess.run(["./temp"], capture_output=True, text=True)
            elif language == "C++":
                with open("temp.cpp", "w") as f:
                    f.write(code)
                result = subprocess.run(["g++", "temp.cpp", "-o", "temp"], capture_output=True, text=True)
                if result.returncode == 0:
                    result = subprocess.run(["./temp"], capture_output=True, text=True)
            elif language == "JavaScript":
                result = subprocess.run(["node", "-e", code], capture_output=True, text=True)
            elif language == "Java":
                with open("Main.java", "w") as f:
                    f.write(code)
                result = subprocess.run(["javac", "Main.java"], capture_output=True, text=True)
                if result.returncode == 0:
                    result = subprocess.run(["java", "Main"], capture_output=True, text=True)
            elif language == "PHP":
                result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
            elif language == "Ruby":
                result = subprocess.run(["ruby", "-e", code], capture_output=True, text=True)
            elif language == "CSS":
                result = subprocess.run(["echo", "CSS is not executable"], capture_output=True, text=True)
            elif language == "HTML":
                result = subprocess.run(["echo", "HTML is not executable"], capture_output=True, text=True)
            else:
                messagebox.showerror("Error", "Unsupported language")
                return

            output = result.stdout
            if result.stderr:
                output += f"\nError:\n{result.stderr}"
            self.output_area.config(state="normal")
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, output)
            self.output_area.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    compiler = MultiLanguageCompiler(root)
    root.mainloop()