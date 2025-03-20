#!/bin/bash

# Fix relative imports within the gpt_sovits package
echo "Starting fix for internal relative imports..."

# Create a temporary file to store TTS.py with corrected imports
cat > /workspaces/GPT-SoVITS/gpt_sovits/GPT_SoVITS/TTS_infer_pack/TTS.py.new << 'EOFPY'
from copy import deepcopy
import math
import os, sys
import random
import traceback
from tqdm import tqdm
now_dir = os.getcwd()
sys.path.insert(0, now_dir)
sys.path.insert(0, os.path.join(now_dir, "GPT_SoVITS"))
import ffmpeg
import os
from typing import Generator, List, Tuple, Union
import numpy as np
import torch
import torch.nn.functional as F
import yaml
from transformers import AutoModelForMaskedLM, AutoTokenizer
from gpt_sovits.GPT_SoVITS.AR.models.t2s_lightning_module import Text2SemanticLightningModule
from gpt_sovits.GPT_SoVITS.feature_extractor.cnhubert import CNHubert
from gpt_sovits.GPT_SoVITS.module.models import SynthesizerTrn
import librosa
from time import time as ttime
from gpt_sovits.tools.i18n.i18n import I18nAuto
from gpt_sovits.GPT_SoVITS.my_utils import load_audio
from gpt_sovits.GPT_SoVITS.module.mel_processing import spectrogram_torch
from gpt_sovits.GPT_SoVITS.TTS_infer_pack.text_segmentation_method import splits
from gpt_sovits.GPT_SoVITS.TTS_infer_pack.TextPreprocessor import TextPreprocessor
import pickle
i18n = I18nAuto()

# Rest of the file continues as is...
EOFPY

# Copy the new TTS.py over the old one
cat /workspaces/GPT-SoVITS/gpt_sovits/GPT_SoVITS/TTS_infer_pack/TTS.py | tail -n +21 >> /workspaces/GPT-SoVITS/gpt_sovits/GPT_SoVITS/TTS_infer_pack/TTS.py.new
mv /workspaces/GPT-SoVITS/gpt_sovits/GPT_SoVITS/TTS_infer_pack/TTS.py.new /workspaces/GPT-SoVITS/gpt_sovits/GPT_SoVITS/TTS_infer_pack/TTS.py

# Let's also check for and fix other relative imports
find /workspaces/GPT-SoVITS/gpt_sovits -type f -name "*.py" | while read file; do
    # Fix relative imports from AR
    sed -i 's/from AR\./from gpt_sovits.GPT_SoVITS.AR./g' "$file"
    sed -i 's/import AR\./import gpt_sovits.GPT_SoVITS.AR./g' "$file"
    
    # Fix relative imports from module
    sed -i 's/from module\./from gpt_sovits.GPT_SoVITS.module./g' "$file"
    sed -i 's/import module\./import gpt_sovits.GPT_SoVITS.module./g' "$file"
    
    # Fix relative imports from feature_extractor
    sed -i 's/from feature_extractor\./from gpt_sovits.GPT_SoVITS.feature_extractor./g' "$file"
    sed -i 's/import feature_extractor\./import gpt_sovits.GPT_SoVITS.feature_extractor./g' "$file"
    
    # Fix relative imports from text
    sed -i 's/from text\./from gpt_sovits.GPT_SoVITS.text./g' "$file"
    sed -i 's/import text\./import gpt_sovits.GPT_SoVITS.text./g' "$file"
    
    # Fix relative imports from TTS_infer_pack
    sed -i 's/from TTS_infer_pack\./from gpt_sovits.GPT_SoVITS.TTS_infer_pack./g' "$file"
    sed -i 's/import TTS_infer_pack\./import gpt_sovits.GPT_SoVITS.TTS_infer_pack./g' "$file"
    
    # Fix relative imports from my_utils
    sed -i 's/from my_utils/from gpt_sovits.GPT_SoVITS.my_utils/g' "$file"
    sed -i 's/import my_utils/import gpt_sovits.GPT_SoVITS.my_utils/g' "$file"
done

echo "Internal relative import fixes completed!"
