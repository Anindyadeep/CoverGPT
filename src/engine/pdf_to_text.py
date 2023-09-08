import os
from pathlib import Path
from typing import Union, Optional 

import PyPDF2
from src.config import CoverGPTConfig
from src.logger import logger

class PDF2TextEngine:
    @classmethod
    def convert_to_text(self, pdf_path: Union[str, Path]) -> Union[str, None]:
        if isinstance(pdf_path, str):
            assert os.path.exists(pdf_path), "The pdf path is not valid"
        
        if isinstance(pdf_path, Path):
            assert pdf_path.exists(), "The pdf path is not valid"
        
        extracted_text = ""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text()
            return extracted_text
        except Exception as e:
            logger.warning(f"Unable to convert pdf to text. Error: {e}")
        return None

    @classmethod
    def convert_and_save(self, pdf_path: Union[str, Path], save_path: Optional[Union[str, Path]]=None) -> None:
        if isinstance(pdf_path, str):
            assert os.path.exists(pdf_path), "The pdf path is not valid"
        
        if isinstance(pdf_path, Path):
            assert pdf_path.exists(), "The pdf path is not valid"
        
        save_path = os.path.join(CoverGPTConfig.yourself_resume_text_path) \
        if save_path is None else save_path

        if converted_text := self.convert_to_text(pdf_path=pdf_path):
            with open(save_path, "w") as writer:
                writer.write(converted_text)
            logger.info(f"Extracted text from pdf and saved it successfully as {save_path}")
        else:
            logger.warning(f"Unable to convert and save extracted text")