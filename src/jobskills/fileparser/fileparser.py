
import textract

def file_parsing(file):
    try:
        text_bytes = textract.process(file)
        return text_bytes.decode('utf-8')
    except textract.exceptions.ShellError as e:
        # return error message 
        return f"Unsupported filetype"
