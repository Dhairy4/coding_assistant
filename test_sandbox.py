import subprocess
import os

def run_in_sandbox(command: str) -> str:

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

    return result.stdout

output = run_in_sandbox()
print(f"Output form docker: {output}")