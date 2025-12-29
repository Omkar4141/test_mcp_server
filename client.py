import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
import json


SERVERS = { 
    "math": {
        "transport": "stdio",
        "command": "/Library/Frameworks/Python.framework/Versions/3.11/bin/uv", @ using which uv : uv installation full path
        "args": [
            "run",
            "fastmcp",
            "run",
            "local_server.py" # full path
        ]
    },
    "expense": {
        "transport": "streamable_http",  # if this fails, try "sse"
        "url": "https://OmkarLokhande.fastmcp.app/mcp"
    },
    
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatOllama(model="gpt-5")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "can u add 3 and 2" # can u rooll a dice twice or can u add my expense 500 to groceries
    response = await llm_with_tools.ainvoke(prompt) # in this in first call we are getting tool to use with its args and all then we are getting the response in second call

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        print("Tool Called{selected_tool}")
        print("Arguments : {json.dumps(selected_tool_args, indent=2)}")

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        print("Result {json.dumps(result, indent=2)}")
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())
