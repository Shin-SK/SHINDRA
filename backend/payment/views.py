import stripe
import json
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from post.models import Post
from user.models import CustomUser  # 🔹 ユーザーモデルを取得
from .models import Donation
from .serializers import DonationSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Stripe API キーを設定


class CreateCheckoutSessionView(APIView):
    """Stripe Checkout セッションを作成"""
    permission_classes = [IsAuthenticated]  # 🔹 ログイン必須

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "jpy",
                    "product_data": {
                        "name": f"投げ銭: {post.title}",
                    },
                    "unit_amount": 500,  # 🔹 固定金額（可変にするならクライアントから受け取る）
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{settings.FRONTEND_URL}/donate/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/donate/cancel",
            metadata={"post_id": post.id, "user_id": request.user.id},
        )

        return Response({"url": checkout_session.url})


@csrf_exempt
def stripe_webhook(request):
    """Stripe からの Webhook で決済成功を処理"""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # ✅ `settings.py` から取得

    print(f"Received Webhook: {payload}")  # ✅ デバッグ用

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        post_id = session["metadata"]["post_id"]
        user_id = session["metadata"]["user_id"]

        user = get_object_or_404(CustomUser, id=user_id)  # 🔹 ユーザーを取得
        post = get_object_or_404(Post, id=post_id)  # 🔹 投稿を取得

        Donation.objects.create(user=user, post=post, amount=session["amount_total"] / 100)  # ✅ `amount_total` は `JPY`（分単位）

        print(f"Donation Recorded: {user.username} -> {post.title} ({session['amount_total']} JPY)")

    return JsonResponse({"status": "success"})


class DonationListView(generics.ListAPIView):
    """ログインユーザーの投げ銭履歴を取得"""
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user).order_by("-created_at")
