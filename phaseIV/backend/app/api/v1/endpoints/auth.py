from fastapi import APIRouter, HTTPException, Body
import httpx
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "https://fozi07-todo-full-stack-app.hf.space").rstrip("/")

@router.post("/signup")
async def proxy_signup(payload: dict = Body(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{AUTH_SERVICE_URL}/auth/signup", json=payload)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "Signup failed")
                except:
                    detail = response.text
                raise HTTPException(status_code=response.status_code, detail=detail)
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"Error proxying signup: {exc}")
            raise HTTPException(status_code=503, detail="Authentication service unavailable")

@router.post("/signin")
async def proxy_signin(payload: dict = Body(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{AUTH_SERVICE_URL}/auth/signin", json=payload)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "Signin failed")
                except:
                    detail = response.text
                raise HTTPException(status_code=response.status_code, detail=detail)
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"Error proxying signin: {exc}")
            raise HTTPException(status_code=503, detail="Authentication service unavailable")
