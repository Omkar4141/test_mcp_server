from __future__ import annotations 
from fastmcp import FastMCP


mcp=FastMCP("math-server")


def _as_number(x):
    "Accepts int/float or numeric strigs else throws an error"
    if isinstance(x,(int,float)):
        return float(x)
    if isinstance(x,str):
        return float(x.strip())
    raise TypeError("Expected a number")

@mcp.tool
async def add(a:float , b:float)->float:
    return _as_number(a) + _as_number(b)

@mcp.tool
async def sub(a:float , b:float)->float:
    return _as_number(a) - _as_number(b)

if __name__ == "__main__":
    mcp.run()