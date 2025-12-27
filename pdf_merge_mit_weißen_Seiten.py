from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog

def merge_pdfs_with_blank_pages():
    # Datei-Auswahl (mehrere PDFs in Reihenfolge auswählen)
    root = tk.Tk()
    root.withdraw()
    pdf_files = filedialog.askopenfilenames(
        title="Wähle die PDF-Dateien aus (in Reihenfolge)",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if not pdf_files:
        print("Keine Dateien ausgewählt.")
        return

    writer = PdfWriter()

    for file in pdf_files:
        reader = PdfReader(file)

        for page in reader.pages:
            # Original-Seite einfügen
            writer.add_page(page)

            # Prüfen, ob Text vorhanden ist
            text = page.extract_text()
            if text and text.strip():
                # 3 leere Seiten hinzufügen (mit gleicher Seitengröße)
                for _ in range(3):
                    writer.add_blank_page(
                        width=page.mediabox.width,
                        height=page.mediabox.height
                    )

    # Speicherort abfragen
    save_path = filedialog.asksaveasfilename(
        title="Speichern unter",
        defaultextension=".pdf",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if save_path:
        with open(save_path, "wb") as f:
            writer.write(f)
        print(f"PDF erfolgreich gespeichert als: {save_path}")
    else:
        print("Speichern abgebrochen.")

if __name__ == "__main__":
    merge_pdfs_with_blank_pages()
