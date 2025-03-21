from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Payment, ProjectFunding, WITFunding

# from import_export.admin import ImportExportModelAdmin # ImportExportModel functionality


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        "confirmation_number",
        "created_at",
        "grand_total",
        "stripe_payment_intent_id",
    )
    field = (
        "confirmation_number",
        "amount",
        "created_at",
        "full_name",
        "email",
        "phone_number",
        "street_address1",
        "street_address2",
        "postcode",
        "town_or_city",
        "county",
        "country",
        "grand_total",
    )
    list_display = (
        "confirmation_number",
        "created_at",
        "full_name",
        "grand_total",
    )
    ordering = ("-created_at",)


admin.site.register(Payment, OrderAdmin)
admin.site.register(ProjectFunding)
admin.site.register(WITFunding)
