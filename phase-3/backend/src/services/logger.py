import logging
import sys

# Configure a structured logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("TodoApp")

def log_tool_call(tool_name: str, user_id: str, params: dict, result: str):
    """
    Log tool invocations for auditability.
    """
    logger.info(f"TOOL_CALL | User: {user_id} | Tool: {tool_name} | Params: {params} | Result: {result}")
