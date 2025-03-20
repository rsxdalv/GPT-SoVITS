import json, os
from io import BytesIO
import wave

from fastapi import FastAPI, Request
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from gpt_sovits.src.common_config_manager import api_config, __version__
from gpt_sovits.Synthesizers.base import Base_TTS_Task, Base_TTS_Synthesizer

tts_synthesizer:Base_TTS_Synthesizer = None

def set_tts_synthesizer(synthesizer:Base_TTS_Synthesizer):
    global tts_synthesizer
    tts_synthesizer = synthesizer

# 用于打印版本信息，纯粹的后端接口默认开启
print(f"Backend Version: {__version__}")

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/tts")
@api.get("/tts")
async def tts(request: Request):
    # json格式
    body = await request.json()
    task = tts_synthesizer.params_parser(body)
    
    if task.stream:
        chunks = tts_synthesizer.generate(task)
        return StreamingResponse(chunks, media_type="audio/x-wav")
    else:
        save_path = tts_synthesizer.generate(task, return_type="filepath")
        return Response(open(save_path, "rb").read(), media_type="audio/x-wav")

@api.get("/character_list")
async def character_list(request: Request):
    res = JSONResponse(tts_synthesizer.get_characters())
    return res

if __name__ == "__main__":
    # 动态导入合成器模块, 此处可写成 from Synthesizers.xxx import TTS_Synthesizer, TTS_Task
    from importlib import import_module
    synthesizer_name = api_config.synthesizer
    synthesizer_module = import_module(f"gpt_sovits.Synthesizers.{synthesizer_name}")
    TTS_Synthesizer = synthesizer_module.TTS_Synthesizer
    TTS_Task = synthesizer_module.TTS_Task
    # 初始化合成器的类
    tts_synthesizer = TTS_Synthesizer(debug_mode=True)
    
    # 生成一句话充当测试，减少第一次请求的等待时间
    gen = tts_synthesizer.generate(tts_synthesizer.params_parser({"text":"你好，世界"}))
    next(gen)
    
    # 打印一些辅助信息
    print(f"Backend Version: {__version__}")
    print(f"Running pure api on port {api_config.tts_port}")
    uvicorn.run(api, host=api_config.tts_host, port=api_config.tts_port)

