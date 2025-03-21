#!/bin/bash

# Update hardcoded file paths for the new package structure
echo "Starting file path update..."

# Find paths that need to be updated in Python files
find /workspaces/GPT-SoVITS -type f -name "*.py" | while read file; do
    # Skip files in venv if it exists
    if [[ "$file" == *"venv"* ]]; then
        continue
    fi
    
    # 1. Update Synthesizers file paths
    sed -i 's|os\.path\.join("Synthesizers/|os.path.join(os.path.dirname(os.path.dirname(__file__)), "Synthesizers/|g' "$file"
    sed -i 's|"Synthesizers/\([^"]*\)"|os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Synthesizers/\1")|g' "$file"
    
    # 2. Update tools file paths
    sed -i 's|"tools/\([^"]*\)"|os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools/\1")|g' "$file"
    
    # 3. Update src file paths
    sed -i 's|"src/\([^"]*\)"|os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src/\1")|g' "$file"
    
    # 4. Update webuis file paths
    sed -i 's|"webuis/\([^"]*\)"|os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "webuis/\1")|g' "$file"
    
    # 5. Update GPT_SoVITS file paths
    sed -i 's|"GPT_SoVITS/\([^"]*\)"|os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "GPT_SoVITS/\1")|g' "$file"
    
    echo "Updated file paths in $file"
done

# Specifically fix the gsv_task.py file which has the error
cat > /workspaces/GPT-SoVITS/gpt_sovits/Synthesizers/gsv_fast/gsv_task.py.new << 'EOFPY'
import os, json, sys
sys.path.append(".")
from uuid import uuid4
from typing import List, Dict, Literal, Optional, Any, Union
import urllib.parse
import hashlib
from gpt_sovits.Synthesizers.base import Base_TTS_Task, ParamItem, init_params_config

def get_params_config():
    # Use a more robust method to find the config file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "configs", "params_config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return init_params_config(json.load(f))
    except:
        raise FileNotFoundError(f"params_config.json not found or invalid at {config_path}")
    
params_config = get_params_config()
from pydantic import BaseModel, Field, model_validator

class GSV_TTS_Task(Base_TTS_Task):
    # character: Optional[str] = None
    # emotion: Optional[str] = None
    ref_audio_path: Optional[str] = None
    prompt_text: Optional[str] = None
    prompt_language: Optional[str] = None
    text_language: Optional[str] = None
    speaker_id: Optional[int] = None
    batch_size: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    temperature: Optional[float] = None
    cut_method: Optional[str] = None
    max_cut_length: Optional[int] = None
    seed: Optional[int] = None
    save_temp: Optional[bool] = False
    parallel_infer : Optional[bool] = True
    repetition_penalty : Optional[float] = 1.35
    # the gsv_fast model only supports 32000 sample rate
    sample_rate: int = 32000
    
    def __init__(self, other_task: Union[BaseModel, dict, None] = None, **data):
        data.setdefault('params_config', params_config)
        super().__init__(other_task, **data)
    
    @property
    def md5(self):
        m = hashlib.md5()
        if self.task_type == "audio":
            m.update(self.src.encode())
        elif self.task_type == "ssml":
            m.update(self.ssml.encode())
        elif self.task_type == "text":
            m.update(self.text.encode())
            m.update(self.text_language.encode())
            m.update(self.character.encode())
            m.update(str(self.speaker_id).encode())
            m.update(str(self.speed).encode())
            m.update(str(self.top_k).encode())
            m.update(str(self.top_p).encode())
            m.update(str(self.temperature).encode())
            m.update(str(self.cut_method).encode())
            m.update(str(self.emotion).encode())
        return m.hexdigest()
EOFPY

mv /workspaces/GPT-SoVITS/gpt_sovits/Synthesizers/gsv_fast/gsv_task.py.new /workspaces/GPT-SoVITS/gpt_sovits/Synthesizers/gsv_fast/gsv_task.py

echo "File path update completed!"
