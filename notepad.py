import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or set it directly like: "sk-..."

class AIInteractiveNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - AI Notepad")
        self.root.geometry("900x650")
        self.filename = None

        self.text_area = tk.Text(root, wrap="word", undo=True, font=("Consolas", 13))
        self.text_area.pack(expand=1, fill="both")

        # Scrollbar
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))

        # Format menu
        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Text Color", command=self.choose_text_color)
        format_menu.add_command(label="Background Color", command=self.choose_bg_color)

        # AI menu
        ai_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="AI", menu=ai_menu)
        ai_menu.add_command(label="Summarize Text", command=self.summarize_text)
        ai_menu.add_command(label="Fix Grammar", command=self.correct_text)
        ai_menu.add_command(label="Generate Content", command=self.generate_text)

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Status bar
        self.status = tk.Label(root, text="Line: 1 | Column: 0", anchor='e')
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind('<KeyRelease>', self.update_status)

    def update_status(self, event=None):
        line, col = self.text_area.index(tk.INSERT).split('.')
        self.status.config(text=f"Line: {line} | Column: {col}")

    def new_file(self):
        self.filename = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("Untitled - Notepad")

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt")
        if self.filename:
            self.root.title(f"{self.filename} - Notepad")
            with open(self.filename, "r", encoding="utf-8") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        if not self.filename:
            self.save_as()
        else:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def save_as(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if self.filename:
            self.save_file()
            self.root.title(f"{self.filename} - Notepad")

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose text color")[1]
        if color:
            self.text_area.config(fg=color)

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose background color")[1]
        if color:
            self.text_area.config(bg=color)

    def show_about(self):
        messagebox.showinfo("About", "AI Interactive Notepad\nDeveloped with OpenAI")

    def summarize_text(self):
        self.call_openai("summarize")

    def correct_text(self):
        self.call_openai("correct grammar")

    def generate_text(self):
        self.call_openai("generate continuation")

    def call_openai(self, task):
        user_text = self.text_area.get(1.0, tk.END).strip()
        if not user_text:
            messagebox.showwarning("Warning", "Text area is empty.")
            return

        prompt = f"Please {task} for the following text:\n\n{user_text}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that helps with text editing."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"OpenAI API Error:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AIInteractiveNotepad(root)
    root.mainloop()