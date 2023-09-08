import os
import streamlit as st
from pathlib import Path
from typing import Optional, Union
from audiorecorder import audiorecorder

class ResourceDump:
    def resume_upload_component(self):
        """Upload the latest resume"""
        st.title("Upload your resume (.pdf)")
        uploaded_document = st.file_uploader(
            label="Upload your latest resume",
            type=['.pdf']
        )
        return uploaded_document

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
                placeholder="Type here ..."
            )
            submit_text = st.button(label="submit")
            if submit_text:
                # save the text
                with open("yourself.text", "w") as writer:
                    writer.write(text_input)
                st.text("Awesome we have recorded your response")
        
        elif use_audio:
            self.recoder_component(
                title="",
                audio_save_path="yourself.wav"
            )
    
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
        self.about_yourself()

if __name__ == '__main__':
    resource = ResourceDump().main()