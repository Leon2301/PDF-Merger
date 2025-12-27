from PyPDF2 import PdfMerger
import tkinter as tk
from tkinter import filedialog

def merge_pdfs():
    # Fenster für Dateiauswahl öffnen
    root = tk.Tk()
    root.withdraw()  # Hauptfenster ausblenden
    pdf_files = filedialog.askopenfilenames(
        title="Wähle die PDF-Dateien aus (in Reihenfolge)",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if not pdf_files:
        print("Keine Dateien ausgewählt.")
        return

    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    # Speicherort abfragen
    save_path = filedialog.asksaveasfilename(
        title="Speichern unter",
        defaultextension=".pdf",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if save_path:
        merger.write(save_path)
        merger.close()
        print(f"PDF erfolgreich gespeichert als: {save_path}")
    else:
        print("Speichern abgebrochen.")

if __name__ == "__main__":
    merge_pdfs()
