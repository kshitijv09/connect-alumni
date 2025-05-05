from rest_framework import serializers
from .models import Fund, Donation
from person.models import User
from person.serializers import UserSerializer

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'amount' in data and data['amount'] is not None:
            data['amount'] = float(instance.amount)
        return data    

class DonationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donor', 'fund', 'amount', 'payment_status', 'transaction_id', 'message']


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    fund = FundSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'

    def get_user(self, obj):
        return UserSerializer(obj.donor).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'amount' in data and data['amount'] is not None:
            data['amount'] = float(instance.amount)
        return data