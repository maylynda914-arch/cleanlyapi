from fastapi import FastAPI, Header, HTTPException
import json
import os
from cleaners import clean_text, remove_emojis, normalize_whitespace, strip_urls, batch_clean
from stripe_webhook import router as stripe_router

app = FastAPI()
app.include_router(stripe_router)

USERS_FILE = "users.json"

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_by_key(api_key):
    data = load_users()
    for user in data["users"]:
        if user["api_key"] == api_key:
            return user
    return None

@app.get("/")
def health_check():
    return {"status": "CleanlyAPI is running"}

@app.get("/credits")
def get_credits(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {"email": user["email"], "credits": user["credits"]}
@app.post("/clean-text")
def clean_text_endpoint(data: dict, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    text = data.get("text", "")
    cleaned = clean_text(text)

    user["credits"] -= 1
    save_users(load_users())

    return {"cleaned_text": cleaned}


@app.post("/remove-emojis")
def remove_emojis_endpoint(data: dict, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    text = data.get("text", "")
    cleaned = remove_emojis(text)

    user["credits"] -= 1
    save_users(load_users())

    return {"cleaned_text": cleaned}


@app.post("/normalize-whitespace")
def normalize_whitespace_endpoint(data: dict, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    text = data.get("text", "")
    cleaned = normalize_whitespace(text)

    user["credits"] -= 1
    save_users(load_users())

    return {"cleaned_text": cleaned}


@app.post("/strip-urls")
def strip_urls_endpoint(data: dict, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    text = data.get("text", "")
    cleaned = strip_urls(text)

    user["credits"] -= 1
    save_users(load_users())

    return {"cleaned_text": cleaned}


@app.post("/batch-clean")
def batch_clean_endpoint(data: dict, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]
    user = get_user_by_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if user["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    texts = data.get("texts", [])
    cleaned_list = batch_clean(texts)

    user["credits"] -= len(texts)
    save_users(load_users())

    return {"cleaned_texts": cleaned_list}

