import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

#1 load api keys 

load_dotenv()

# 2 simple tool

@tool
def add(a :int, b : int) -> int: 
    """ add  two numbers """
    print(f"[Tool Excecuted] adding {a} and {b}")   
    return a + b

@tool
def multiply(a :int, b : int) -> int: 
    """ multiply  two numbers """
    print(f"[Tool Excecuted] multiplying {a} and {b}")   
    return a * b




availabel_tools = {"add" : add, 
                   "multiply" : multiply}


# 3 setup the model and bound the tools
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

llm_with_tools = llm.bind_tools(list(availabel_tools.values()))

# 4 agent loop
def simple_agent_loop(user_prompt: str):
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

            if tool_name in availabel_tools:
                tool_output = availabel_tools[tool_name].invoke(tool_args)

            else : 
                tool_output = f"Tool {tool_name} not found"

            messages.append(ToolMessage(content=str(tool_output), tool_call_id = tool_id))

        turn += 1

if __name__ == "__main__":
    user_prompt = "I want to subtract call the subtract tool with arguments 5 and 10 and then multiply the result by 2"
    simple_agent_loop(user_prompt)