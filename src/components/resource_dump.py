import os 
from typing import Union, Optional

import streamlit as st
from audiorecorder import audiorecorder
from pydub.audio_segment import AudioSegment
from dotenv import load_dotenv


load_dotenv()

# in app modules import
from src import logger
from src.config import CoverGPTConfig
from src.engine.audio_trascriber import (
    AssemblyAITranscriberEngine, 
    WhisperTranscriberEngine
)
from src.engine.pdf_to_text import PDF2TextEngine

# TODO:
# We need of updating the existing information 
# add instruction in a readme in record_component 
# Add some description in about_yourself

class ResourceDump:
    def upload_resume_and_dump(self) -> int:
        """Upload the latest resume
        
        Returns:
            The upload status. If 200 then everything is succesful else
            there is an internal server error
        """
        
        st.title("Upload your resume")
        uploaded_resume = st.file_uploader(
            label="Upload your latest resume",
            type=['.pdf']
        )
        if uploaded_resume:
            file_details = {"Filename": uploaded_resume.name, "Filesize": uploaded_resume.size}
            st.write("Uploaded File Details:", file_details)

            pdf_path = CoverGPTConfig.yourself_resume_pdf_path
            with open(pdf_path, "wb") as pdf_writer:
                pdf_writer.write(uploaded_resume.getbuffer())
            st.success("Resume successfully uploaded and saved")
            return 200
        else:
            return 500

    @property
    def recorder_component(self) -> Union[AudioSegment, None]:
        st.text("Record yourself")
        audio = audiorecorder("Click to record", "Click to stop recording")
        if not audio.empty():
            st.audio(audio.export().read())
            return audio 
        else:
            st.write("Audio did not recordeed")
            return None
    
    def text_writer_component(self):
        st.text("Write about yourself, don't be shy make yourself at home")
        text_input = st.text_area(label="", placeholder="Type here ...")
        
        if submit_text := st.button(label="submit"):
            with open(CoverGPTConfig.yourself_text_file_path, "w") as writer:
                writer.write(text_input)
            st.text("Awesome we have recorded your response")
        
    def audio_writer_component(self, transcribe_engine: str):
        assert transcribe_engine in ['whisper', 'assemblyai'], \
        "We do not transcriptions engine other than whisper and assemblyai"

        recorded_audio = self.recorder_component
        if recorded_audio:
            if submit_audio := st.button(label="Submit response"):
                recorded_audio.export(CoverGPTConfig.yourself_audio_file_path, format="wav")
                if transcribe_engine == "whisper":
                    # TODO: This should be done async through an API 
                    WhisperTranscriberEngine.transcribe_and_save(
                        audio_path=CoverGPTConfig.yourself_audio_file_path,
                        save_path=CoverGPTConfig.yourself_text_file_path
                    )
                else:
                    AssemblyAITranscriberEngine.transcribe_and_save(
                        audio_path=CoverGPTConfig.yourself_audio_file_path,
                        save_path=CoverGPTConfig.yourself_text_file_path
                    )
                st.text("Awesome we recorded your response")
    
    def update_about_yourself(self):
        pass
    
    def upload_research_paper(self):
        # first check whether the user wants to write or wants to record
        pass

    def attach_twitter(self):
        pass

    def attach_linkedin(self):
        pass

    def attach_github(self):
        pass

    def express_interest(self):
        pass
    
