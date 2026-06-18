from pypdf import PdfReader
import re

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        # Remove URL noise
        page_text = re.sub(
            r"https://aws\.amazon\.com/agreement/\s*\d+/\d+",
            "",
            page_text
        )

        # Remove timestamp noise
        page_text = re.sub(
            r"\d+/\d+/\d+,\s*\d+:\d+\s*[AP]M",
            "",
            page_text
        )

        text += page_text + "\n"

    return text