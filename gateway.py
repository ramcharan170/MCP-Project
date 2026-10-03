import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fastmcp import FastMCP
mcp=FastMCP("UnifiedToolingGateway")
# UnifiedToolingGateway is the name You are giving to the mcp server
# Import the libraries and initiate the server.
load_dotenv()

SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")

supabase: Client =  create_client(SUPABASE_URL,SUPABASE_KEY)

@mcp.tool
def get_server_status()->dict:
    """Returns current operational status of the MCP gateway
    AI agents call this to verify that the gateway and its tools are active """
    return {
        "status":"online",
        "service": "UnifiedToolingGateway",
        "database":"Supabase postgre Sql"
    }
@mcp.tool
def get_tasks_by_status(status:str)->list[dict]:
    """Queries live tasks from the Supabase database filtered by status.
    Expected values:'pending' or 'completed'.
    """
    response=supabase.table("tasks").select("*").eq("status", status).execute()
    return response.data


if __name__=="__main__":
    mcp.run()
    