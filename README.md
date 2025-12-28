
# test_mcp_server

A simple **MCP (Model Context Protocol) server** project demonstrating both **local** and **remote** MCP server setups using **FastMCP**, **LangChain**, and **uv**.


## Requirements

* Python 3.9+
* `pip`
* `uv`



## First-Time Setup

### 1. Install `uv`

```bash
pip install uv
```

### 2. Navigate to the project directory

```bash
cd test_mcp_server
```

### 3. Initialize the project with `uv`

```bash
uv init .
```

### 4. Add FastMCP

```bash
uv add fastmcp
```


## Local MCP Server Setup

### 1. Create the local server file

Create a file named:

```text
local_server.py
```

This file contains your MCP server implementation.

### 2. Add required dependencies

```bash
uv add langchain langchain-openai langchain_mcp_adapters
```

### 3. Create the client

Create a client file:

```text
client.py
```

### 4. Run the local server using STDIO

The local MCP server communicates via **STDIO**.

Run the client:

```bash
uv run client.py
```



## Remote MCP Server Setup

### 1. Create MCP tools

* Define your MCP tools for the remote server
* Ensure they are compatible with FastMCP Cloud

### 2. Deploy to FastMCP Cloud

* Deploy the server to **FastMCP Cloud**
* Obtain the remote server configuration

### 3. Update configuration

* Add the remote MCP server configuration to your config file
* Replace the local STDIO setup with the remote server endpoint

### 4. Run the client with the remote server

```bash
uv run client.py
```


## Notes

* Local server uses **STDIO** for communication
* Remote server runs on **FastMCP Cloud**
* `uv` handles dependency management and execution
* Same client can be used for both local and remote servers by changing configuration



