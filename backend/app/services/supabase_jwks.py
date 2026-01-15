import httpx
from app.core.config import settings

JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

_cached_keys = None


async def get_signing_key(kid: str):
    global _cached_keys

    if _cached_keys is None:
        headers = {
            "apikey": settings.SUPABASE_ANON_KEY,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL, headers=headers)
            response.raise_for_status()
            _cached_keys = response.json()["keys"]

    for key in _cached_keys:
        if key["kid"] == kid:
            return key

    raise ValueError("Signing key not found")
