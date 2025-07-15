from langchain_ollama import ChatOllama

class LLMConfig:
    def __init__(self):
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        llm = ChatOllama(
            model="llama3.2",
            temperature=0.1,  # Not 0, might cause issues
            num_predict=256,
        )
        return llm
    
    def get_llm(self):
        return self.llm
    
    def get_llm_with_tools(self, tools):
        return self.llm.bind_tools(tools)