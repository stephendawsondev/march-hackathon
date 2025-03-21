import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def create_payment_session(request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": "Project Funding",
                        },
                        "unit_amount": int(request.post.get("amount") * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri("/payment/success/"),
            cancel_url=request.build_absolute_uri("/payment/cancel"),
        )
        return JsonResponse({"sessionId": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
