from pathlib import Path

def load_text_file(file_path: str) -> dict:
    """
    Loads a .txt file and returns its content and document name.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported")

    text = path.read_text(encoding="utf-8")

    return {
        "document": path.name,
        "text": text
    }
