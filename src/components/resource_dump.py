import os 
from pathlib import Path
from typing import Union

import streamlit as st
import assemblyai as aai
from audiorecorder import audiorecorder
from dotenv import load_dotenv

load_dotenv()

# in app modules import
from src import logger

# TODO:
# We need of updating the existing information 

class ResourceDump:
    _assemblyai_api_key = os.getenv("ASSEMBLY_AI_API_KEY")
    aai.settings.api_key = _assemblyai_api_key
    transcriber = aai.Transcriber()

    # All of these paths will be going inside the config.py
    audio_save_path=os.path.join("artifacts", "yourself.wav")
    yourself_text = os.path.join("artifacts", "yourself.text")

    def resume_upload_component(self):
        """Upload the latest resume"""
        st.title("Upload your resume")
        uploaded_document = st.file_uploader(
            label="Upload your latest resume",
            type=['.pdf']
        )
        return uploaded_document

    def update_about_yourself(self):
        pass

    def recoder_component(self, title: str, audio_save_path: Union[str, Path]) -> Union[audiorecorder, None]:
        # if isinstance(audio_save_path, Path):
        #     assert audio_save_path.exists(), f"The path: {str(audio_save_path)} does not exists"

        # if isinstance(audio_save_path, str):
        #     assert os.path.exists(audio_save_path), f"The path: {audio_save_path} does not exists"
        
        st.title(f"Record your {title}")
        audio = audiorecorder(
            "Click to record",
            "Click to stop recording"
        )

        if not audio.empty():
            st.audio(audio.export().read())
            return audio 
        else:
            st.write("Audio did not recordeed")
            return None
    
    def about_yourself(self):
        # TODO: Add some description 
        use_audio = st.sidebar.checkbox("Record ")
        use_text = st.sidebar.checkbox("Write it")

        if use_text:
            st.text("Write about yourself, don't be shy make yourself at home")
            text_input = st.text_area(
                label="",
                placeholder="Type here ..."
            )
            submit_text = st.button(label="submit")
            if submit_text:
                # save the text
                with open(self.yourself_text, "w") as writer:
                    writer.write(text_input)
                st.text("Awesome we have recorded your response")
        
        elif use_audio:
            recorded_audio = self.recoder_component(title="", audio_save_path=self.audio_save_path)
            submit_audio = st.button(label="Submit response")
            
            # TODO: Move it to config
            if submit_audio:
                recorded_audio.export(self.audio_save_path, format="wav")
                try:
                    logger.info("Audio transcription process started")
                    transcript = self.transcriber.transcribe(
                        self.audio_save_path
                    )

                    # save the transcript file
                    # assumption: The user can either use the text or the audio if both are used 
                    # then the prior used will be deleted

                    with open(self.yourself_text, "w") as audio_transcript_writer:
                        audio_transcript_writer.write(transcript.text)

                    logger.info(f"Saved transcript file as {self.yourself_text}")
                    st.text("Awesome we have recorded your response")

                except Exception as e:
                    logger.warning(
                        "Audio transcription failed"
                        f"Exception: {e}" #TODO: provide a custom exception
                    ) 
                # TODO: use assembly ai to trascibe this response
                st.text("Awesome we recorded your response")

    
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

    def main(self):
        self.resume_upload_component()

        write_it, record_it = st.columns(2)
        with write_it:
            check_write = st.radio("Write about yourself")
            # pass the text box
        with record_it:
            check_record = st.radio("Record about yourself")
        self.about_yourself()

if __name__ == '__main__':
    resource = ResourceDump().main()