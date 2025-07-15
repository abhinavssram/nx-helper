# from configs.llm_configs import LLMConfig
# from configs.nx_helper_tool_config import NXToolConfig
# from prompts.prompt_config import create_nx_prompt_template
# from src.nx_graph_helper import NXGraphHelper
# from src.tool_executor import ToolExecutor
# from src.utility import load_nx_graph_from_json
# from langchain_core.messages import ToolMessage
# import json

# def main():
#     # Initialize components
#     graph = load_nx_graph_from_json("../nx-output.json")
#     nx_helper = NXGraphHelper(graph)
#     tools = NXToolConfig.create_tools(nx_helper)
#     tool_executor = ToolExecutor(tools)
#     llm_config = LLMConfig()
#     llm = llm_config.get_llm_with_tools(tools)
#     prompt_template = create_nx_prompt_template()

#     print("NX Dependency Graph Analyzer")
#     print("Type 'exit' to quit.")
    
#     while True:
#         user_query = input("\nAsk your NX graph question: ")
#         if user_query.lower() == "exit":
#             break

#         # First LLM call
#         messages = prompt_template.format_messages(query=user_query)
#         ai_message = llm.invoke(messages)
#         print(f"\n[LLM] {ai_message}")

#         # Handle tool calls
#         # if hasattr(ai_message, 'tool_calls') and ai_message.tool_calls:
#         #     tool_messages = []
#         #     for tool_call in ai_message.tool_calls:
#         #         tool_name = tool_call["name"]
#         #         tool_args = tool_call["args"]
#         #         tool_id = tool_call["id"]
                
#         #         print(f"[TOOL CALL] {tool_name}({tool_args})")
#         #         result = tool_executor.execute_tool(tool_name, **tool_args)
#         #         print(f"[TOOL RESULT] {result}")
                
#         #         tool_message = ToolMessage(content=json.dumps(result), tool_call_id=tool_id)
#         #         tool_messages.append(tool_message)
            
#         #     # Second LLM call with tool results
#         #     messages_with_tools = messages + [ai_message] + tool_messages
#         #     final_ai_message = llm.invoke(messages_with_tools)
#         #     print(f"\n[FINAL ANSWER] {final_ai_message.content}")
#         # else:
#         #     print(f"[ANSWER] {ai_message.content}")

# if __name__ == "__main__":
#     main()

# from configs.llm_configs import LLMConfig
# from prompts.prompt_config import create_nx_prompt_template


# def test_without_tools():
#     llm_config = LLMConfig()
#     llm = llm_config.get_llm()  # No tools
#     prompt_template = create_nx_prompt_template()
    
#     while True:
#         user_query = input("\nAsk your question: ")
#         if user_query.lower() == "exit":
#             break
            
#         messages = prompt_template.format_messages(query=user_query)
#         ai_message = llm.invoke(messages)
#         print(f"\n[ANSWER] {ai_message.content}")

# if __name__ == "__main__":
#     test_without_tools()


# test_tools.py
# from configs.llm_configs import LLMConfig
# from configs.nx_helper_tool_config import NXToolConfig
# from src.utility import load_nx_graph_from_json
# from src.nx_graph_helper import NXGraphHelper

# def test_tool_creation():
#     # Test tool creation
#     graph = load_nx_graph_from_json("../nx-output.json")
#     nx_helper = NXGraphHelper(graph)
#     tools = NXToolConfig.create_tools(nx_helper)
    
#     print("Created tools:")
#     for tool in tools:
#         print(f"- {tool.name}: {tool.description}")
#         print(f"  Args schema: {tool.args_schema.model_fields.keys()}")
    
#     # Test LLM with tools
#     llm_config = LLMConfig()
#     llm = llm_config.get_llm_with_tools(tools)
#     print(f"\nLLM with {len(tools)} tools created successfully")

# if __name__ == "__main__":
#     test_tool_creation()


# main.py
# main.py
# from configs.llm_configs import LLMConfig
# from langchain_core.prompts import ChatPromptTemplate

# Simple_System_Prompt = '''
# You are a helpful assistant for NX dependency graph analysis.

# When users ask about specific entities or dependencies, use the available tools.
# For greetings and general questions, respond normally without tools.

# Be conversational and helpful.
# '''

# def create_simple_prompt():
#     return ChatPromptTemplate.from_messages([
#         ("system", Simple_System_Prompt),
#         ("human", "{query}")
#     ])
# def test_no_tools():
#     llm_config = LLMConfig()
#     llm = llm_config.get_llm()  # NO TOOLS
#     prompt = create_simple_prompt()
    
#     while True:
#         query = input("\nQuestion: ")
#         if query.lower() == 'exit':
#             break
        
#         messages = prompt.format_messages(query=query)
#         response = llm.invoke(messages)
        
#         print(f"Response: {response.content}")
#         print(f"Full response: {response}")

# if __name__ == "__main__":
#     test_no_tools()


# debug_main.py
from configs.llm_configs import LLMConfig
from configs.nx_tools import create_nx_tools
from prompts.prompt_config import create_nx_prompt_template
from src.nx_graph_helper import NXGraphHelper
from src.utility import load_nx_graph_from_json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
# from prompts.prompt_config import zero_shot_system_prompt

def debug_main():
    # Load and setup
    graph = load_nx_graph_from_json("../nx-output.json")
    nx_helper = NXGraphHelper(graph)
    tools = create_nx_tools(nx_helper)
    
    llm_config = LLMConfig()
    llm = llm_config.get_llm_with_tools(tools)
    prompt_template = create_nx_prompt_template()
    
    print("Debug mode - checking responses...")
    print("Debug mode - tools: ", tools)
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'exit':
            break
        
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", zero_shot_system_prompt),
        #         ("user", "{input}"),
        #     ]
        # )

        # 5. Create a runnable chain
        chain = prompt_template | llm

        # 6. Example usage with simple invoke and manual tool call handling
        # user_input = "What is the square of 7?"
        response = chain.invoke({"query": query})

        # print(f"AI Message: {response}")
        
        # Debug: Print full response
        print(f"DEBUG - Full response: {response}")
        print(f"DEBUG - Response type: {type(response)}")
        print(f"DEBUG - Response content: {response.content}")
        print(f"DEBUG - Has tool_calls: {hasattr(response, 'tool_calls')}")
        if hasattr(response, 'tool_calls'):
            print(f"DEBUG - Tool calls: {response.tool_calls}")
            tool_id = '89327897e3892'
            tool_message = ToolMessage(content={}, tool_call_id=tool_id)

            final_response_messages = [
                HumanMessage(content=query),
                response,
                tool_message,
            ]
            final_response = llm.invoke(final_response_messages)
            print(f"Final response: {final_response.content}")
        else:
            print(f"Response: {response.content}")

if __name__ == "__main__":
    debug_main()