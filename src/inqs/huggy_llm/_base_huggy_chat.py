from typing import List, Dict, Literal
from hugchat.hugchat import ChatBot

from ._base_login import HFCredentialManager

_AVAILABLE_MODELS = Literal['meta-llama/Meta-Llama-3.1-70B-Instruct',
              'CohereForAI/c4ai-command-r-plus-08-2024',
              'Qwen/Qwen2.5-72B-Instruct',
              'meta-llama/Llama-3.2-11B-Vision-Instruct',
              'NousResearch/Hermes-3-Llama-3.1-8B',
              'mistralai/Mistral-Nemo-Instruct-2407',
              'microsoft/Phi-3.5-mini-instruct'
              ]

class BaseHuggyLLM(HFCredentialManager, ChatBot):
    MODELS: List[str] = ['meta-llama/Meta-Llama-3.1-70B-Instruct',
              'CohereForAI/c4ai-command-r-plus-08-2024',
              'Qwen/Qwen2.5-72B-Instruct',
              'meta-llama/Llama-3.2-11B-Vision-Instruct',
              'NousResearch/Hermes-3-Llama-3.1-8B',
              'mistralai/Mistral-Nemo-Instruct-2407',
              'microsoft/Phi-3.5-mini-instruct'
              ]

    def __new__(cls, hf_email=None, hf_password=None, cookie_dir_path="./cookies/", save_cookies=True,
                system_prompt:str = "",default_llm:int = 0):
        instance = super().__new__(cls)
        instance.__init__(hf_email, hf_password, cookie_dir_path, save_cookies)
        return ChatBot(default_llm=default_llm,system_prompt=system_prompt,cookies=instance.cookies.get_dict())

class HuggyLLM():
    def __init__(
        self,
        model_name:_AVAILABLE_MODELS=None,
        hf_email=None,
        hf_password=None,
        cookie_dir_path="./cookies/",
        save_cookies=True,
        system_prompt:str = "",
        default_llm:int = 0,
        _llm: BaseHuggyLLM|None = None
    ):
        self.model_name = model_name
        self.llm = _llm if _llm is not None else BaseHuggyLLM(hf_email=hf_email,
                                                              hf_password=hf_password,
                                                              cookie_dir_path=cookie_dir_path,
                                                              save_cookies=save_cookies,
                                                              system_prompt=system_prompt,
                                                              default_llm=default_llm)
    @property
    def models(self):
        return self.llm.MODELS

    def _get_sys_and_user_prompt(self,messages: List[Dict]|str):
        if isinstance(messages, str):
            return "",messages
        return messages[0]['content'],messages[1]['content']

    def invoke(self,messages: List|str, model_name:_AVAILABLE_MODELS=None, **kwargs):
        sys_prompt,user_prompt = self._get_sys_and_user_prompt(messages)
        self.llm.new_conversation(modelIndex=self.llm.MODELS.index(model_name) if model_name else 0,
                                  system_prompt=sys_prompt,
                                  switch_to=True)
        res = self.llm.chat(user_prompt,**kwargs)
        res.wait_until_done()
        return res.text

    def stream(self,messages: List|str, model_name:_AVAILABLE_MODELS=None,**kwargs):
        sys_prompt,user_prompt = self._get_sys_and_user_prompt(messages)
        self.llm.new_conversation(modelIndex=self.llm.MODELS.index(model_name) if model_name else 0,
                                  system_prompt=sys_prompt,
                                  switch_to=True)
        res = self.llm.chat(user_prompt,stream = True,**kwargs)
        for x in res:
            if x and isinstance(x,dict):
                yield x.get('token',"")

    def pstream(self,messages:List[Dict]|str,model_name:_AVAILABLE_MODELS=None,**kwargs):
        for _ in self.stream(messages,model_name=model_name,**kwargs):
            print(_,end = "",flush=True)