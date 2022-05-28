from rest_framework import serializers

from .models import Client
from invoice.models import Invoice


class ClientInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "is_sent",
            "is_paid",
            "is_credited",
            "invoice_type",
            "net_amount",
            "vat_amount",
            "gross_amount",
            "get_due_date_formatted",
        ]


class ClientSerializer(serializers.ModelSerializer):
    invoices = ClientInvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        read_only_fields = (
            "created_by",
            "created_at",
        )
        fields = (
            "id",
            "name",
            "email",
            "org_num",
            "address1",
            "address2",
            "zipcode",
            "place",
            "country",
            "contact_person",
            "contact_reference",
            "invoices"
        )
