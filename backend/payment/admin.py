from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")
