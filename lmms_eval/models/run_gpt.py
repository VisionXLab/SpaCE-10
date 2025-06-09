import requests
import json
import time

class GPTagent:
    def __init__(
        self,
        api,
        model_type,
        max_retries=1 # 控制最大重试次数
    ):
        self.model_type = model_type
        self.Baseurl = 'http://35.220.164.252:3888' 
        self.Skey = "sk-3QyVWzSBumceYp3EUVCQOGnZD3vSO3kqRTczn3Mh8J3Bhlly"
        self.url = self.Baseurl + "/v1/chat/completions"
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.Skey}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)', 
            'Content-Type': 'application/json'
        }
        self.max_retries = max_retries

    def get_caption(self, system_prompt, user_prompt, base64_images=None):
        content = [{"type": "text", "text": user_prompt}]

        # 直接添加 base64 编码图片（data URL 格式）
        if base64_images:
            for image_url in base64_images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        payload = json.dumps({
            "model": self.model_type,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            # "max_token": 512
        })

        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(self.url, headers=self.headers, data=payload)
                data = response.json()
                print(response)
                print(data)
                if 'choices' in data and data['choices']:
                    return data['choices'][0]['message']['content']
                else:
                    # Log and retry
                    retries += 1
                    print(f"Retry {retries}/{self.max_retries}: Invalid response, retrying...")
                    time.sleep(2)  # Increase sleep duration to prevent overwhelming the server
            except Exception as e:
                    # Log exception and retry
                    print(f"Exception during request: {e}")
                    retries += 1
                    time.sleep(2)  # Increase sleep duration to prevent overwhelming the server

        return ""
    