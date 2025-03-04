from django.urls import path
from .views import CreateCheckoutSessionView, stripe_webhook, DonationListView

urlpatterns = [
    path("<int:post_id>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
    path("history/", DonationListView.as_view(), name="donation-history"),
]
