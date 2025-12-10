import os


def load_decade(path):
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    # Optional: keep only .txt files (remove this filter if not needed)
    files = [f for f in files if f.lower().endswith(".ocr")]

    if not files:
        print("No OCR files found.")
        return []

    # Load all files into a list
    documents = []

    for fname in files:
        with open(os.path.join(path, fname), "r", encoding="utf-8") as f:
            documents.append(f.read())

    return documents