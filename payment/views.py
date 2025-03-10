# payments/views.py

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
from user.models import CustomUser
from .models import Donation
from .serializers import DonationSerializer

# Stripe秘密鍵
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    """
    ログインユーザーが投げ銭金額を指定→StripeのCheckoutセッション作成
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        # 対象の投稿を取得 (存在しない/ID違いなら404)
        post = get_object_or_404(Post, id=post_id)

        # リクエストJSONから金額を取得
        try:
            amount = int(request.data.get("amount", 0))
        except ValueError:
            return Response({"error": "金額は数値で指定してください。"}, status=400)

        if amount < 100 or amount > 50000:
            return Response({"error": "金額は100～50000円の範囲で指定してください。"}, status=400)

        # StripeのCheckoutセッションを作成
        # metadataに user_id, post_id を入れて、Webhookで参照
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "jpy",
                    "product_data": {"name": "Donation"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{settings.FRONTEND_URL}payments/success",
            cancel_url=f"{settings.FRONTEND_URL}payments/cancel",
            metadata={
                "post_id": post.id,
                "user_id": request.user.id
            },
        )

        return Response({"url": checkout_session.url})


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe からのWebhookを受け取って、支払い完了(=checkout.session.completed)時に Donation を作成
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # ペイロードが不正
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        # 署名エラー
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Checkout完了イベントのみ処理
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        post_id = session["metadata"]["post_id"]
        user_id = session["metadata"]["user_id"]

        # 該当ユーザー、Postを取得
        user = get_object_or_404(CustomUser, id=user_id)
        post = get_object_or_404(Post, id=post_id)

        # 投げ銭をレコードに保存(amount_totalはcent単位なので100で割る)
        Donation.objects.create(
            user=user,
            post=post,
            amount=session["amount_total"]
        )

        print(f"[Webhook] Donation Recorded: {user.username} -> {post.title}, amount={session['amount_total']}")

    return JsonResponse({"status": "success"})


class DonationListView(generics.ListAPIView):
    """
    ログインユーザーの投げ銭一覧
    """
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ログインユーザーに紐づく Donation を新しい順で返す
        return Donation.objects.filter(user=self.request.user).order_by("-created_at")
