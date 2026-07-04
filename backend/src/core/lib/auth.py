from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from typing import Optional, Dict, Any
from supabase_auth.types import User
import json
from core.lib.db import get_supabase_client

security = HTTPBearer()

# BASE_PATH = "/core/v1"

async def verify_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[User]:

    supabase =await get_supabase_client()
    
    if not credentials:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated required",
        )
    
    token = credentials.credentials
    
    try:
        user_response = await supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user session",
            )
        return user_response.user

    except Exception as e:
        print(f"Error while Authentication: {e}")
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    