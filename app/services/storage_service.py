from supabase import create_client
from app.core.config import settings
import tempfile
from pathlib import Path

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY
)

def upload_file_to_storage(
    bucket: str,
    path: str,
    content: bytes,
    content_type: str,
):
    response = supabase.storage.from_(bucket).upload(
        path=path,
        file=content,
        file_options={"content-type": content_type},
    )

    if response.get("error"):
        raise RuntimeError(response["error"]["message"])

    return path

def get_signed_download_url(bucket: str, path: str, expires_in: int = 300):
    response = supabase.storage.from_(bucket).create_signed_url(
        path,
        expires_in,
    )

    if response.get("error"):
        raise RuntimeError(response["error"]["message"])

    return response["signedURL"]

def delete_file_from_storage(bucket: str, path: str):
    response = supabase.storage.from_(bucket).remove([path])

    if response.get("error"):
        raise RuntimeError(response["error"]["message"])
    
def download_file_to_temp(bucket: str, path: str) -> Path:
    response = supabase.storage.from_(bucket).download(path)

    if response.get("error"):
        raise RuntimeError(response["error"]["message"])

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(response)
    tmp.close()

    return Path(tmp.name)
