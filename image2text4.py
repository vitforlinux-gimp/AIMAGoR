import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import base64
import requests

class ImageDescriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descrizione immagine con Pollinations AI")

        frame_top = tk.Frame(root)
        frame_top.pack(padx=10, pady=10, fill=tk.X)

        self.load_btn = tk.Button(frame_top, text="Carica file", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT)

        self.file_label = tk.Label(frame_top, text="Nessun file selezionato", fg="blue")
        self.file_label.pack(side=tk.LEFT, padx=10)

        self.copy_btn = tk.Button(root, text="Copia testo selezionato", command=self.copy_text)
        self.copy_btn.pack(padx=10, pady=(0,5), anchor="e")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, state=tk.DISABLED)
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.exit_btn = tk.Button(root, text="Esci", command=self.exit_app)
        self.exit_btn.pack(padx=10, pady=(0,10), anchor="e")

        self.file_path = None

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Seleziona file immagine o altro",
            filetypes=[("Tutti i file", "*.*")]
        )
        if not path:
            return

        self.file_path = path
        self.file_label.config(text=path)

        # Disabilito la UI mentre elaboro
        self.load_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Elaborazione in corso...\n")
        self.text_area.config(state=tk.DISABLED)

        threading.Thread(target=self.process_image, daemon=True).start()

    def process_image(self):
        try:
            with open(self.file_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()

            payload = {
                "model": "openai",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_data}"
                            }
                        }
                    ]
                }]
            }

            response = requests.post("https://text.pollinations.ai/openai", json=payload, timeout=60)
            print(response)
            response.raise_for_status()
            result = response.json()
            description = result['choices'][0]['message']['content']
        except Exception as e:
            description = f"Errore durante la richiesta:\n{e}"

        self.root.after(0, self.show_result, description)

    def show_result(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)

        self.load_btn.config(state=tk.NORMAL)
        self.copy_btn.config(state=tk.NORMAL)

    def copy_text(self):
        try:
            selected = self.text_area.selection_get()
        except tk.TclError:
            selected = self.text_area.get(1.0, tk.END).strip()
        if selected:
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            messagebox.showinfo("Copiato", "Testo copiato negli appunti.")
        else:
            messagebox.showwarning("Nessun testo", "Nessun testo selezionato da copiare.")

    def exit_app(self):
        self.root.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ImageDescriptionApp(root)
    root.geometry("700x500")
    root.mainloop()

if __name__ == "__main__":
    main()