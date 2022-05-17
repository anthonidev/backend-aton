from rest_framework import serializers

from .models import Order


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "status",
            "transaction_id",
            "amount",
            "shipping_price",
            "date_issued",
            "address_line_1",
            "address_line_2",
        ]
