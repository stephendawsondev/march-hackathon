import json
import os

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import PaymentForm, ProjectFundingForm, WITFundingForm
from .models import Payment, ProjectFunding, WITFunding

stripe.api_key = settings.STRIPE_SECRET_KEY


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


def donations(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user = request.user
            payment.save()

            target = payment_form.cleaned_data["target"]
            if target == "project":
                project_form = ProjectFundingForm(request.POST)
                if project_form.is_valid():
                    project_funding = project_form.save(commit=False)
                    project_funding.payment = payment
                    project_funding.save()
            elif target == "wit":
                wit_form = WITFundingForm(request.POST)
                if wit_form.is_valid():
                    wit_funding = wit_form.save(commit=False)
                    wit_funding.payment = payment
                    wit_funding.save()

            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),  # Stripe expects the amount in cents
                currency="usd",
                metadata={"integration_check": "accept_a_payment"},
            )

            payment.stripe_payment_intent_id = intent["id"]
            payment.save()

            messages.success(request, "Your donation has been successfully processed.")
            return redirect("donations")
    else:
        payment_form = PaymentForm()
        project_form = ProjectFundingForm()
        wit_form = WITFundingForm()

    context = {
        "payment_form": payment_form,
        "project_form": project_form,
        "wit_form": wit_form,
    }

    return render(request, "donations/donations.html", context)
