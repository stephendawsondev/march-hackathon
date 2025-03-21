import json
import os

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from donations.models import Payment


@require_POST
def cache_donation_data(request):
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "donation_data": json.dumps(request.session.get("donate", {})),
                "save_info": request.POST.get("save_info"),
                "username": request.user.username,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. Please try again later.",
        )
        return HttpResponse(content=e, status=400)


# Create your views here.
def donations(request):
    stripe_public_key = os.environ.get("STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
