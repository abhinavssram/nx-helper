from configs.llm_configs import LLMConfig
from configs.nx_tools import create_nx_tools
from prompts.prompt_config import create_nx_prompt_template
from src.nx_graph_helper import NXGraphHelper
from src.tool_executor import ToolExecutor
from src.utility import load_nx_graph_from_json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def should_use_tools(query, llm):
    """Use LLM to decide if tools are needed"""
    classification_prompt = """
    You are a helpful assistant that determines if a user query requires using graph analysis tools.

    **When to Use Tools:**
    - Questions about specific entities (apps, libraries, e2e tests)
    - Questions about dependencies between entities
    - Questions about graph structure or analysis
    - Questions that require examining the actual graph data
    In above cases,
    Respond with only "YES" if the query requires graph analysis tools (finding nodes, edges, paths, etc.).

    **When NOT to Use Tools:**
    - Greetings (hello, hi, etc.)
    - Questions about your role or capabilities
    - General questions about NX or dependency graphs (concept explanations)
    In above cases,
    Respond with only "NO" if it's a simple greeting, general conversation, or doesn't need graph analysis.
    
    Query: {query}
    
    Answer:"""
    
    response = llm.invoke(classification_prompt.format(query=query))
    return response.content.strip().upper() == "YES"

def debug_main():
    # Load and setup
    graph = load_nx_graph_from_json("../nx-output.json")
    nx_helper = NXGraphHelper(graph)
    tools = create_nx_tools(nx_helper)
    tool_executor = ToolExecutor(tools)
    
    llm_config = LLMConfig()
    llm = llm_config.get_llm()
    llm_with_tools = llm_config.get_llm_with_tools(tools)
    prompt_template = create_nx_prompt_template()
    
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'exit':
            break

        # First, classify if tools are needed
        if should_use_tools(query, llm):
            print("DEBUG - Tools needed")
            # Use LLM with tools
            chain = prompt_template | llm_with_tools
            ai_response = chain.invoke({"query": query})
            print(f"AI MID tool Response: {ai_response.content}")
            tool_name = ai_response.tool_calls[0]["name"]
            print(f"Tool name: {tool_name}")
            tool_args = ai_response.tool_calls[0]["args"]
            tool_id = ai_response.tool_calls[0]["id"]

            tool_result = tool_executor.execute_tool(tool_name, **tool_args)
            # print(f"Tool result: {tool_result}")
            tool_message = ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_id)

            final_response_messages = [
                HumanMessage(content=query),
                ai_response,
                tool_message,
            ]
            final_response = llm.invoke(final_response_messages)
            print(f"Final response: {final_response.content}")       
        else:
            print("DEBUG - No tools needed")
            # Use regular LLM
            chain = prompt_template | llm
            ai_response = chain.invoke({"query": query})
            print(f"Response: {ai_response.content}")
if __name__ == "__main__":
    debug_main()