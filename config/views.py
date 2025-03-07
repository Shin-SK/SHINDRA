# views.py
from rest_framework.views import APIView
from allauth.account.models import EmailConfirmationHMAC
from django.shortcuts import redirect
from django.http import Http404

class MyConfirmEmailView(APIView):
    def get(self, request, key):
        # トークンを検証
        try:
            emailconf = EmailConfirmationHMAC.from_key(key)
        except:
            raise Http404("Invalid or expired token")

        if not emailconf:
            raise Http404("Token not found or already used")

        emailconf.confirm(request)
        return redirect("http://localhost:5173/confirm-success")
