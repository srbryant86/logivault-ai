from fastapi import APIRouter, Request, Header
import stripe
import os

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Store user plan data — swap with real DB later
user_plans = {}

@router.post("/api/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return { "status": "invalid signature" }

    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]
        user_id = sub["metadata"].get("userId", "anon")
        plan = sub["items"]["data"][0]["price"]["nickname"]  # "Free", "Pro", etc.
        user_plans[user_id] = plan
        print(f"✅ Stripe plan updated for {user_id}: {plan}")
    
    return { "status": "ok" }