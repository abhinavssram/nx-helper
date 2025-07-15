from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
import json

# 1. Define your tool
@tool
def calculate_square(number: int) -> int:
    """Calculates the square of an integer.

    Args:
        number: The integer to square.
    """
    return number * number

# 2. Initialize the Ollama model
llm = ChatOllama(model="llama3.2", temperature=0)

# 3. Bind the tool to the model
llm_with_tools = llm.bind_tools([calculate_square])

# 4. Create a simple prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "{input}"),
    ]
)

# 5. Create a runnable chain
chain = prompt | llm_with_tools

# 6. Example usage with simple invoke and manual tool call handling
user_input = "hello"
ai_message = chain.invoke({"input": user_input})

print(f"AI Message: {ai_message}")

# Check if the AI message contains tool calls
if ai_message.tool_calls:
    print("\nModel wants to call a tool!")
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        if tool_name == "calculate_square":
            print(f"Calling tool: {tool_name} with args: {tool_args}")
            # --- FIX IS HERE ---
            result = calculate_square.func(**tool_args) # Execute the original function
            # --- END FIX ---
            print(f"Tool output: {result}")

            # Send the tool's output back to the model as a ToolMessage
            tool_message = ToolMessage(content=json.dumps(result), tool_call_id=tool_id)
            final_response_messages = [
                HumanMessage(content=user_input),
                ai_message,
                tool_message
            ]
            print(f"Final response messages: {final_response_messages}")
            final_ai_message = llm.invoke(final_response_messages)
            print(f"\nFinal AI Message (after tool execution): {final_ai_message.content}")
        else:
            print(f"Unknown tool requested: {tool_name}")
else:
    print("\nModel did not request a tool call. Response:")
    print(ai_message.content)

