from langchain_core.tools import tool
import os

from src.utils import truncate_output

@tool
def read_file(file_path: str) -> str:
    """Reads the content of a file"""
    print(f"[Tool Executed] Reading file: {file_path}")

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return truncate_output(content)
    except Exception as e:
        return f"Error: reading file '{file_path}'. {str(e)}"

