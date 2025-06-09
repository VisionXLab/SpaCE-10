import base64
import json
import os
import time
from copy import deepcopy
from io import BytesIO
from typing import List, Tuple, Union

from PIL import Image
from tqdm import tqdm

from lmms_eval.api.instance import Instance
from lmms_eval.api.model import lmms
from lmms_eval.api.registry import register_model
from .run_gpt import GPTagent

from loguru import logger
eval_logger = logger

try:
    import anthropic
    import numpy as np
    from decord import VideoReader, cpu
except Exception as e:
    eval_logger.warning(f"Error importing optional dependencies: {e}")

# 设置 Claude API Key 和 URL
os.environ["ANTHROPIC_API_KEY"] = "sk-3QyVWzSBumceYp3EUVCQOGnZD3vSO3kqRTczn3Mh8J3Bhlly"
API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY")

@register_model("custom_api")
class Custom_API(lmms):
    def __init__(
        self,
        model_version: str = "claude-3-opus-20240229",
        image_token: str = "<image>",
        system_prompt: str = "",
        modality: str = "image",
        max_frames_num: int = 10,
        continual_mode: bool = False,
        response_persistent_folder: str = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.model_version = model_version
        self.image_token = image_token
        self.system_prompt = system_prompt
        self.modality = modality
        self.max_frames_num = max_frames_num
        self.response_persistent_folder = response_persistent_folder
        self.device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"

    def encode_image(self, image):
        output_buffer = BytesIO()
        image.save(output_buffer, format="JPEG")
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode("utf-8")
        return base64_str

    def flatten(self, input):
        return [j for i in input for j in i]

    def generate_until(self, requests) -> List[str]:
        json_path = "/mnt/petrelfs/gongziyang/all_mix_data_for_testing/experiments_dirs/claude-double/func2.json"
        with open(json_path, 'r') as f:
            json_file = json.load(f)
        # exist_doc_id = list(json_file.keys())
        exist_doc_id = []
        # print(exist_doc_id)
        # exit()
        agent = GPTagent(api=API_KEY, model_type=self.model_version)
        res = []
        doc_responses = {}  # 用来保存 doc_id 和模型回答
        pbar = tqdm(total=len(requests), desc="Model Responding")

        for contexts, gen_kwargs, doc_to_visual, doc_id, task, split in [reg.args for reg in requests]:
            # if str(doc_id) in exist_doc_id:
            #     print(f'{doc_id} has been generated!')
            # else:
            visuals = [doc_to_visual(self.task_dict[task][split][doc_id])]
            # visuals = visuals[:1]
            visuals = self.flatten(visuals)
            base64_images = []

            for visual in visuals:
                if isinstance(visual, str) and os.path.exists(visual):
                    base64_images.append(self.encode_image(visual))
                elif isinstance(visual, Image.Image):
                    buffered = BytesIO()
                    visual.save(buffered, format="JPEG")
                    mime_type = "image/jpeg"
                    base64_encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    data_url = f"data:{mime_type};base64,{base64_encoded}"
                    base64_images.append(data_url)
                else:
                    eval_logger.warning(f"Unsupported visual format: {type(visual)}")
                    continue

            response_text = agent.get_caption(
                system_prompt=self.system_prompt,
                user_prompt=contexts,
                base64_images=base64_images
            )
            print(response_text)
            
            # 将 doc_id 和模型回答保存到字典
            doc_responses[doc_id] = response_text
            with open('/mnt/petrelfs/gongziyang/all_mix_data_for_testing/experiments_dirs/gpt-4o-2024-11-20/identification.json', 'w') as f:
                json.dump(doc_responses, f, ensure_ascii=False, indent=4)
            res.append(response_text)
            pbar.update(1)

        pbar.close()
        

        return res
    def loglikelihood(self, requests: List[Instance]) -> List[Tuple[float, bool]]:
        raise NotImplementedError("Loglikelihood evaluation is not supported for this model.")

    def generate_until_multi_round(self, requests) -> List[str]:
        raise NotImplementedError("Multi-round generation not implemented.")
