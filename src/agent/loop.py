import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

import sys
from pathlib import Path

# # Ensure project root is in sys.path when script is executed directly
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# import tools
from src.tools.file_tool import read_file
from src.tools.bash_exec import run_bash
#1 load api keys 

load_dotenv()


available_tools = {
    "read_file": read_file,
    "run_bash": run_bash
}


# 3 setup the model and bound the tools
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash"
# )

llm = ChatNVIDIA(
    model = "nvidia/nemotron-3-super-120b-a12b"
)

llm_with_tools = llm.bind_tools(list(available_tools.values()))

# 4 agent loop
def agent_loop(user_prompt: str):
    print(f"starting loop for {user_prompt}")
    messages = [HumanMessage(content=user_prompt)]

    turn = 1

    while turn <= 10 :
        print(f"turn {turn} Model Thinking...")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # stop condtition model didnot called any tools
        if not response.tool_calls:
            print(f"Model did not call any tools, stopping the loop{response.content}")
            break


        # Executed tool calls requested by model

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"[Model Requested Tool] : {tool_name} {tool_args}")
            

            # look up tools directly from tools map

            if tool_name in available_tools:
                tool_output = available_tools[tool_name].invoke(tool_args)

            else : 
                tool_output = f"Tool {tool_name} not found"

            messages.append(ToolMessage(content=str(tool_output), tool_call_id = tool_id))

        turn += 1

if __name__ == "__main__":
    user_prompt = "can you run the test1.py file and tell me the output"
    agent_loop(user_prompt)