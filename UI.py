import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import fitz  # from PyMuPDF
from summarize import load_model, text_summarizer  # Updated import

# Initialize summarizer
#summarizer = load_model()

def upload_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Choose a PDF file"
    )
    if file_path:
        file_label.config(text=f"Selected File:\n{file_path}")
        read_pdf(file_path)
    else:
        messagebox.showwarning("No File", "No file was selected.")

def read_pdf(path):
    try:
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        preview_text.config(state=tk.NORMAL)
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, text.strip())
        preview_text.config(state=tk.DISABLED)
        return text.strip()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF:\n{e}")
        return ""

def summarize_text():
    text = preview_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("No Text", "No text to summarize.")
        return
    try:
        summary = text_summarizer(summarizer, text)
        messagebox.showinfo("Summary", summary)
    except Exception as e:
        messagebox.showerror("Summarization Error", str(e))

# Main GUI Window
root = tk.Tk()
root.title("Pleasant PDF Uploader")
root.geometry("600x500")
root.configure(bg="#f0f4f7")

# Style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12), padding=10)
style.configure("TLabel", font=("Segoe UI", 10))

# Upload button
upload_btn = ttk.Button(root, text="📁 Upload PDF", command=upload_pdf)
upload_btn.pack(pady=20)

# File path label
file_label = ttk.Label(root, text="No file selected", background="#f0f4f7", wraplength=500, anchor="center")
file_label.pack(pady=10)

# Text preview area
preview_text = tk.Text(root, height=15, width=70, wrap=tk.WORD, font=("Segoe UI", 10))
preview_text.pack(padx=20, pady=10)
preview_text.config(state=tk.DISABLED)

# Scrollbar
scrollbar = ttk.Scrollbar(root, command=preview_text.yview)
scrollbar.place(in_=preview_text, relx=1.0, rely=0, relheight=1.0, anchor='ne')
preview_text.config(yscrollcommand=scrollbar.set)

# Summarize button
summarize_btn = ttk.Button(root, text="🧠 Summarize Text", command=summarize_text)
summarize_btn.pack(pady=10)

# Start the application
root.mainloop()
