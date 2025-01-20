import base64
import json
import os.path
import os
import time
from openai import OpenAI


class GPTInterpreter:
    def __init__(self,
                 api_key,
                 setting,
                 example_data: dict = False,
                 version: str = "text",
                 ):

        self.api_key = api_key
        self.example_data = example_data
        self.version = version
        self.setting = setting[version]
        self.message = []

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            output = base64.b64encode(image_file.read()).decode('utf-8')
            return output

    def add_example_prompt(self, message_name: str):
        if not self.example_data:
            raise ValueError("There is no example json data")

        example_message = self.example_data[message_name]
        sorted_prompt = sorted(example_message, key=lambda x: x['index'])
        for i in range(len(sorted_prompt)):
            role = sorted_prompt[i]["role"]
            content_text = sorted_prompt[i]["content"]
            if sorted_prompt[i]["image_path"]:
                image_path = sorted_prompt[i]["image_path"]
                encoded_image = self.encode_image(image_path)
                content = [{"type": "text", "text": content_text},
                           {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]
                prompt = {"role": role, "content": content}
            else:
                prompt = {"role": role, "content": content_text}
            self.message.append(prompt)

    def add_message(self, role, content, image_url: list[str] or str or bool = False):
        if not image_url:
            # Only text message
            prompt = {"role": role, "content": content}
        else:
            prompt = [{"type": "text", "text": content}]
            if type(image_url) is str:
                image_url = [image_url]
            for image in image_url:
                encoded_image = self.encode_image(image)
                prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
            prompt = {"role": role, "content": prompt}

        self.message.append(prompt)

    def delete_message_index(self, index: int):
        if 0 <= index < len(self.message):
            print(f"Delete a message {self.message[index]}")
            del self.message[index]
        else:
            raise IndexError

    def run_prompt(self):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.setting["model"],
            messages=self.message,
            max_tokens=self.setting["max_token"],
            temperature=self.setting["temperature"],
            top_p=self.setting["top_p"]
        )
        answer = response.choices[0].message.content
        return answer

    def reset_message(self):
        self.message = []

    def pop_message(self):
        self.message.pop()
