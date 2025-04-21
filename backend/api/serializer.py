from rest_framework.serializers import ModelSerializer
from .models import Subscriptions

# Serializers

class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'