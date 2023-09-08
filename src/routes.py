import streamlit as st 

from src.logger import logger
from src.prompt_store import ABOUT_YOURSELF_BODY
from src.config import CoverGPTConfig 
from src.engine.pdf_to_text import PDF2TextEngine
from src.components.resource_dump import ResourceDump

# TODO:
# send this to an API as an async thing 
# Introduce a settings and there make it happen 

class Routes:
    def upload_assets(self):
        dumper = ResourceDump()
        # upload resume
        upload_status = uploaded_resume = dumper.upload_resume_and_dump()
        if upload_status == 200:
            PDF2TextEngine.convert_and_save(
                pdf_path=CoverGPTConfig.yourself_resume_pdf_path,
                save_path=CoverGPTConfig.yourself_resume_text_path
            )

        st.text("Personal information")
        options = st.selectbox(
            "Now tell something about yourself. You can either write it or record it",
            ("write", "record")
        )
        st.markdown(ABOUT_YOURSELF_BODY.format(option=options))
        if options == "write":
            dumper.text_writer_component()
        else:
            dumper.audio_writer_component(transcribe_engine="whisper")