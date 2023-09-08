import os
from pathlib import Path
from typing import Optional, Union, List

import assemblyai as aai
from whispercpp import Whisper
from src.config import CoverGPTConfig as covergpt_config
from src.logger import logger

# TODO: provide a custom exception

class AssemblyAITranscriberEngine:
    aai.settings.api_key = covergpt_config.assemblyai_api_key
    transcriber = aai.Transcriber()
    
    @classmethod
    def transcribe(self, audio_path: Union[str, Path]) -> Union[str, List[str], None]:
        """Transcribes the text and returns string or a list of str

        Args:
            audio_path (Union[str, Path]): The path where the audio is located

        Returns:
            Union[str, List[str]]: Returns the transcribed text if transcription is successful else None
        """
        if isinstance(audio_path, str):
            assert os.path.exists(audio_path), "The audio path is not valid"
        
        if isinstance(audio_path, Path):
            assert audio_path.exists(), "The audio path is not valid"
        
        try:
            logger.info("Audio transcription process started ...")
            transcript = self.transcriber.transcribe(audio_path)
            return transcript.text 
        except Exception as e:
            logger.warning(f"Audio transcription failed Exception: {e}" )
        return None


    @classmethod
    def transcribe_and_save(self, audio_path: Union[str, Path], save_path: Optional[Union[str, Path]]=None) -> None:
        """Transcribes the voice and converts that to text and saves it into device using Assembly AI API. 
        
        Args:
            audio_path ([Union[str, Path]]): The path where the audio is located
        Please note, make sure that you have a valid Assembly AI key. Otherwise please claim that
        here: https://www.assemblyai.com/dashboard/activation
        """
        
        if isinstance(audio_path, str):
            assert os.path.exists(audio_path), "The audio path is not valid"
        
        if isinstance(audio_path, Path):
            assert audio_path.exists(), "The audio path is not valid"
        
        save_path = os.path.join(covergpt_config.artifacts_dir, covergpt_config.yourself_text_filename) \
        if save_path is None else save_path
        
        if transcribed_text := self.transcribe(audio_path=audio_path) is not None:
            with open(save_path, "w") as audio_transcribe_writer:
                audio_transcribe_writer.write(transcribed_text)
            logger.info(f"Saved transcript as: {save_path}")
        else:
            logger.warning(f"Audio transcription failed Exception" )


class WhisperTranscriberEngine:
    whisper_client = Whisper(covergpt_config.whispercpp_model)

    @classmethod
    def transcribe(self, audio_path: Union[str, Path]) -> Union[str, List[str], None]:
        """Transcribes the voice and converts that to text and saves it into device using local whisper cpp 
        
        Args:
            audio_path (Union[str, Path]): The path where the audio is located

        Returns:
            Union[str, List[str], None]: Returns the transcribed text if transcription is successful else None
        """
        try:
            logger.info("Audio transcription process started ...")
            transcribed_instance = self.whisper_client.transcribe(audio_path)
            return self.whisper_client.extract_text(transcribed_instance)
        except Exception as e:
            logger.warning(f"Audio transcription failed Exception: {e}" )
        return None

    @classmethod
    def transcribe_and_save(self, audio_path: Union[str, Path], save_path: Optional[Union[str, Path]]=None) -> None:
        if isinstance(audio_path, str):
            assert os.path.exists(audio_path), "The audio path is not valid"
        
        if isinstance(audio_path, Path):
            assert audio_path.exists(), "The audio path is not valid"
        
        save_path = os.path.join(covergpt_config.artifacts_dir, covergpt_config.yourself_text_filename) \
        if save_path is None else save_path
        if transcribed_text := self.transcribe(audio_path=audio_path) is not None:
            if isinstance(transcribed_text, str):
                with open(save_path, "w") as audio_transcribe_writer:
                    audio_transcribe_writer.write(transcribed_text)
            else:
                # assert isinstance(transcribed_text, List[str]), \
                # f"Transcribed text is expected to be a list of string but found {type(transcribed_text)}"

                with open(save_path, "w") as audio_transcribe_writer:
                    for text in transcribed_text:
                        audio_transcribe_writer.write(text, ' ')
            logger.info(f"Saved transcript as: {save_path}")
        else:
            logger.warning(f"Audio transcription failed Exception" )