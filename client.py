import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
import json
SERVERS=SERVERS = { 
    "math": {
        "transport": "stdio",
        "command": "C:/Python3.13/Scripts/uv.exe",
        "args": [
            "run",
            "fastmcp",
            "run",
            "C:/Users/hp/Desktop/MCP/Remote Server/test_mcp_server"
       ]
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatOllama(model="llama3.2:3b")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "add 3+2 "
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())