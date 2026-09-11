import fitz  # PyMuPDF


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from a PDF or TXT file given its raw bytes.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename:   Original filename (used to determine file type).

    Returns:
        Extracted plain text as a single string.

    Raises:
        ValueError: If the file extension is not .pdf or .txt.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = [page.get_text() for page in doc]
        return "\n".join(pages)

    if ext == "txt":
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1")

    raise ValueError(
        f"Unsupported file type '.{ext}'. Please upload a PDF or TXT file."
    )
