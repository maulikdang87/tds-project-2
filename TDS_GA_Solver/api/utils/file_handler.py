import os
import tempfile
from fastapi import UploadFile

async def save_upload_file_temporarily(upload_file: UploadFile) -> str:
    """
    Save an uploaded file temporarily and return the file path.

    The function creates a temporary file using NamedTemporaryFile to avoid orphaned directories.
    """
    try:
        # Get a secure filename
        secure_filename = os.path.basename(upload_file.filename)
        
        # Create a temporary file with auto-deletion disabled
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{secure_filename}")

        # Read and write file contents
        contents = await upload_file.read()
        with open(temp_file.name, "wb") as f:
            f.write(contents)
        
        return temp_file.name  # Return the path to the saved file
    except Exception as e:
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)  # Ensure cleanup on failure
        raise e
