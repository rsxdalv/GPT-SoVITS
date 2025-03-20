__version__ = "2.6.3"

import os,  json
import torch

import logging

from pydantic import BaseModel, Field
logging.getLogger("markdown_it").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("charset_normalizer").setLevel(logging.ERROR)
logging.getLogger("torchaudio._extension").setLevel(logging.ERROR)
def test_fp16_computation():
    # 检查CUDA是否可用
    if not torch.cuda.is_available():
        return False, "CUDA is not available. Please check your installation."

    try:
        # 创建一个简单的半精度张量计算任务
        # 例如，执行一个半精度的矩阵乘法
        a = torch.randn(3, 3, dtype=torch.float16).cuda()  # 将张量a转换为半精度并移动到GPU
        b = torch.randn(3, 3, dtype=torch.float16).cuda()  # 将张量b转换为半精度并移动到GPU
        c = torch.matmul(a, b)  # 执行半精度的矩阵乘法
        # 如果没有发生错误，我们认为GPU支持半精度运算
        return True, "Your GPU supports FP16 computation."
    except Exception as e:
        # 如果执行过程中发生异常，我们认为GPU不支持半精度运算
        return False, f"Your GPU does not support FP16 computation. Error: {e}"


def get_device_info(device_str:str = "auto", is_half_str:bool = False):
    is_half = False
    if device_str == "auto":
        device = get_optimal_torch_device()
        try:
            device_arch = get_optimal_arch_name(device)
            os.environ["TORCH_DEVICE_ARCH"] = device_arch
        except:
            os.environ["TORCH_DEVICE_ARCH"] = "cpu"
    else:
        device = torch.device(device_str)
    if is_half_str:
        if device.type == "cuda":
            is_half = True
    return device, is_half

def get_optimal_torch_device(index=0) -> torch.device:
    # Get the optimal Torch device
    if torch.cuda.is_available():
        return torch.device(f"cuda:{index % torch.cuda.device_count()}")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

def get_optimal_arch_name(device: torch.device) -> str:
    if device.type == "cuda":
        return "cuda"
    if device.type == "mps":
        return "mps"
    return "cpu"

def load_infer_config(model_path: str):
    config_path = os.path.join(model_path, "infer_config.json")
    print(f"Loading inference config from: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def auto_generate_infer_config(folder_path:str):
    """
    Automatically generate infer_config.json from the files in the folder
    """
    infer_config = {}
    for file in os.listdir(folder_path):
        if file.endswith(".ckpt"):
            infer_config["gpt_path"] = file
        elif file.endswith(".pth"):
            infer_config["sovits_path"] = file

    if "gpt_path" not in infer_config or "sovits_path" not in infer_config:
        raise FileNotFoundError("No .ckpt or .pth file found in the folder!")

    # Try to find reference audio files
    emotion_list = {}
    wav_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            wav_files.append(file)

    # If there are wav files, add them to emotion_list
    if len(wav_files) > 0:
        emotion_list["default"] = {
            "ref_wav_path": wav_files[0],  # Use the first wav file
            "prompt_text": "",
            "prompt_language": "auto"
        }

    infer_config["emotion_list"] = emotion_list

    # Save the config
    config_path = os.path.join(folder_path, "infer_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(infer_config, f, indent=4, ensure_ascii=False)

def remove_character_path(full_path,character_path):
    # 从full_path中移除character_path部分
    return os.path.relpath(full_path, character_path)
