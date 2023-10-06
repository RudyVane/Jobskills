import os

from filetypes import docx, pdf, txt

# TODO: use library instead of my own ducttape files.
def file_parsing(file):
    # Determine the file extension
    file_extension = os.path.splitext(file)[1].lower()

    # Delegate parsing based on file extension
    if file_extension == ".docx":
        return docx.parse(file)
    elif file_extension == ".pdf":
        return pdf.parse(file)
    elif file_extension == ".txt":
        return txt.parse(file)
    else:
        return "Unsupported filetype"
