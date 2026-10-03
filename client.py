# imports and parameters specification
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params= StdioServerParameters(
    command=sys.executable,
    args=["gateway.py"]
)
async def run_client():
    print("Client: starting gateway and connectiing via Stdio..")

    async with stdio_client(server_params) as (read,write):
        # stdio_client(...) launches gateway.py in the background as a subprocess and binds:
        # read: Pipe reading the data from the servers stdout
        # write: Pipe sending the data to the servers stdin.
        async with ClientSession(read,write) as session:
            # it automatically handles our calls into the json rpc messages and reading incoming responses.
            # await session.initialize(): Sends the mandatory message to exchange capabilities and verify the protocol versin compacitbility before calliing any tools 
            await session.initialize()
            print("Client : Connected succesfully!\n")

            tools_response= await session.list_tools()
            print("Available tools in the Gateway:")
            for tool in tools_response.tools:
                print(f"-{tool.name} : {tool.description}")
            print("\n Client: Calling 'get_tasks_by_status' with status='pending'...")
            result=await session.call_tool(
                "get_tasks_by_status",
                arguments={"status":"pending"}
            )

            for content_block in result.content:
                print(f"\n Server Response : \n{content_block.text}")
if __name__== "__main__":
    asyncio.run(run_client())

            