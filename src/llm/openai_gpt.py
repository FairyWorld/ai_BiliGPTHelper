from typing import Tuple

import openai

from src.llm.base import LLMBase
from src.utils.logging import LOGGER

_LOGGER = LOGGER.bind(name="openai_gpt")


class OpenAIGPTClient(LLMBase):
    def __init__(self, api_key, endpoint="https://api.openai.com/v1"):
        self.api_key = api_key
        self.endpoint = endpoint
        self.openai = openai
        self.set_openai()

    def set_openai(self):
        self.openai.api_base = self.endpoint
        self.openai.api_key = self.api_key

    def get_openai(self):
        return self.openai

    def completion(
        self, prompt, model="gpt-3.5-turbo", **kwargs
    ) -> Tuple[str, int] | None:
        """调用openai的Completion API
        :param model: 模型名称
        :param prompt: 输入的文本（请确保格式化为openai的prompt格式）
        :param kwargs: 其他参数
        :return: 返回生成的文本和token总数 或 None
        """
        try:
            self.set_openai()
            resp = self.openai.ChatCompletion.create(
                model=model, messages=prompt, **kwargs
            )
            _LOGGER.debug(f"调用openai的Completion API成功，API返回结果为：{resp}")
            _LOGGER.info(
                f"调用openai的Completion API成功，本次调用中，prompt+response的长度为{resp['usage']['total_tokens']}"
            )
            return (
                resp["choices"][0]["message"]["content"],
                resp["usage"]["total_tokens"],
            )
        except Exception as e:
            _LOGGER.trace(f"调用openai的Completion API失败：{e}")
            return None
