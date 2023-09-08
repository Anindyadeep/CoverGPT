import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
@dataclass
class CoverGPTConfig:
    # Please note any one of the engine (audio / llm) should be make True
    # == available audio engine === 
    using_whisper: bool = True
    using_assembly: bool = False

    # == available llm engine ===
    using_llama2: bool = True
    using_openai: bool = False 

    # api keys
    assemblyai_api_key: str = os.getenv("ASSEMBLY_AI_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    # whisper cpp config
    whispercpp_model: str = "medium"

    # paths
    covergpt_cache_dir: str = os.path.join(os.path.expanduser("~"), '.cache')
    logs_parent_dir: str = os.path.join(covergpt_cache_dir, 'Logs')
    artifacts_dir: str = os.path.join(covergpt_cache_dir, "artifacts")
    
    # == route specific config ===
    # resource_dump.py

    yourself_resume_pdf_path: str = os.path.join(artifacts_dir, "resume.pdf")
    yourself_resume_text_path: str = os.path.join(artifacts_dir, "resume_text_content.text")
    yourself_audio_file_path: str = os.path.join(artifacts_dir, "resource_dump_yourself.wav")
    yourself_text_file_path: str = os.path.join(artifacts_dir, "resource_dump_yourself.text")


os.makedirs(CoverGPTConfig.covergpt_cache_dir, exist_ok=True)
os.makedirs(CoverGPTConfig.logs_parent_dir, exist_ok=True)
os.makedirs(CoverGPTConfig.artifacts_dir, exist_ok=True)