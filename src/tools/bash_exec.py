from langchain_core.tools import tool
import subprocess

@tool
def run_bash(command : str) -> str:
    """
    Runs a bash command with 30 second timeout
    return stdout and stderr or error if timeout
    """

    print(f"[Tool Executed] Running bash command: {command}")

    try:
        # run command with 30 sec timeout
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
    
        )

        output = result.stdout + result.stderr

        if not output