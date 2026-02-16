from fastapi import APIRouter, Request, HTTPException
import stripe
import json
import os
from main import load_users, save_users
from secrets import token_hex

router = APIRouter()

# Your Stripe webhook secret will go here later
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_details", {}).get("email")

        if not email:
            raise HTTPException(status_code=400, detail="No email found")

        data = load_users()

        # Find existing user
        user = next((u for u in data["users"] if u["email"] == email), None)

        if not user:
            # Create new user with API key
            user = {
                "email": email,
                "api_key": token_hex(16),
                "credits": 100  # credits per purchase
            }
            data["users"].append(user)
        else:
            # Add credits to existing user
            user["credits"] += 100

        save_users(data)

    return {"status": "success"}
