import hashlib
import os, glob
from typing import Literal

from fpdf import FPDF
from pypdf import PdfReader, PdfWriter
from loguru import logger


class NumberPDF(FPDF):
    def __init__(self, align: Literal["R", "L", "C"] = "C", font_family: str = "Arial", font_size: int = 14):
        super().__init__()
        self.align = align
        self.font_family = font_family
        self.font_size = font_size

        self._init_font()

    def footer(self) -> None:
        self.set_y(-15)

        self.cell(0, 10, str(self.page_no()), align=self.align)

    def _init_font(self) -> None:
        self.set_font(self.font_family, size=self.font_size)


class PdfEnumerator:
    def __init__(self, folder_path: list[str] | str):
        self.folder_paths = folder_path if isinstance(folder_path, list) else [folder_path]

    def main(self) -> None:
        for folder_path in self.folder_paths:
            logger.debug("Start processing folder: {}", folder_path)
            filepaths = self._find_all_files(folder_path)

            for filepath in filepaths:
                self._enumerate_file(filepath)
    
    def _enumerate_file(self, filepath: str) -> None:
        reader = PdfReader(filepath)
        temp_filepath = self._make_temp_enumerated_pdf(reader, filepath)
        merge_writer = self._merge_pdfs(reader, temp_filepath)
        os.remove(temp_filepath)
        result_filepath = self._save_pdf(merge_writer, filepath)
        logger.debug("Initial file hash {}, Result file hash: {}", self._get_file_hash(filepath), self._get_file_hash(result_filepath))

    def _find_all_files(self, folder_path: str) -> list[str]:
        return glob.glob(os.path.join(folder_path, "*.pdf"))

    def _make_temp_enumerated_pdf(self, reader: PdfReader, filepath: str) -> str:
        temp_enumerated = NumberPDF(font_size=12)

        for _ in range(len(reader.pages)):
            temp_enumerated.add_page()

        temp_filepath = f"{os.path.splitext(filepath)[0]}_temp_enumerated.pdf"
        temp_enumerated.output(temp_filepath)
        return temp_filepath

    def _merge_pdfs(self, reader: PdfReader, temp_filepath: str) -> PdfWriter:
        merge_writer = PdfWriter()
        temp_reader = PdfReader(temp_filepath)

        for index, page in enumerate(temp_reader.pages):
            input_page = reader.pages[index]
            input_page.merge_page(page)
            merge_writer.add_page(input_page)

        return merge_writer
    
    def _save_pdf(self, merge_writer: PdfWriter, filepath: str) -> str:
        result_dir = os.path.join(os.path.dirname(filepath), "results")
        os.makedirs(result_dir, exist_ok=True)
        
        result_filepath = os.path.join(result_dir, os.path.splitext(os.path.basename(filepath))[0] + "_enumerated.pdf")
        
        with open(result_filepath, "wb") as f:
            merge_writer.write(f)
        return result_filepath
    
    def _get_file_hash(self, filepath: str) -> str:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    pdf_enumerator = PdfEnumerator("C:/Users/your_path/")
    pdf_enumerator.main()
