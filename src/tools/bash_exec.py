from langchain_core.tools import tool
import subprocess
import os

from src.utils import truncate_output

@tool
def run_bash(command : str) -> str:
    """
    Runs a bash command with 30 second timeout
    return stdout and stderr or error if timeout
    """

    print(f"[Tool Executed] Running bash command: {command}")

    try:
       # New code (runs safely inside Docker sandbox):
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",            # No internet access
            "-v", f"{os.getcwd()}:/workspace", # Mount current folder into container
            "-w", "/workspace",             # Set working dir inside container
            "python:3.13-slim",
            "sh", "-c", command
        ]

        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr

        if not output.strip():  
            output = "(command executed with no output)"
        return truncate_output(output)
    except subprocess.TimeoutExpired as e:
        return f"Error: '{command}' timed out after 30 seconds"
    except Exception as e:
        return f"Error:running bash command {str(e)}"



    
    