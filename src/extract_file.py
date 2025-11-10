import PyPDF2


def extract_text_from_file(file):

    filename = file.name.lower()

    if filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif filename.endswith(".docx"):
        import docx
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return ""
