from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

class LLMConfig:
    load_dotenv()
    def __init__(self):
        self.llm = self._intialize_anthropic_llm()
    
    def _initialize_llm(self):
        llm = ChatOllama(
            model="llama3.2",
            temperature=0.1,  # Not 0, might cause issuesa
            num_predict=1024,
        )
        return llm
    
    def get_llm(self):
        return self.llm
    
    def get_llm_with_tools(self, tools):
        return self.llm.bind_tools(tools)
    
    def _intialize_anthropic_llm(self):
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0.1,
            max_tokens=1024,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        return llm