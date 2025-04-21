from django.shortcuts import render
from .serializer import SubscriptionSerializer
from .models import Subscriptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db.models import Sum


# Create your views here.

# Get & Create subscriptions
@api_view(['GET', 'POST'])
def subscriptionList(request):
    if request.method == 'GET':
        subs = Subscriptions.objects.all()
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)
    elif  request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

# Delete a subscription
@api_view(['DELETE'])
def deleteSubscription(reauest, id):
    try:
        subs = Subscriptions.objects.get(id=id)
        subs.delete()
        return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)
    except Subscriptions.DoesNotExist:
        return Response('There is no subscription with this id', status=status.HTTP_404_NOT_FOUND)
    

# Get total spends per month
@api_view(['GET'])
def getTotalMonthly(request):
    data = Subscriptions.objects.filter(cycle='mn').aggregate(Sum("price", default=0))
    return Response(data)

# Get total spends per year
@api_view(['GET'])
def getTotalYearly(request):
    data = Subscriptions.objects.filter(cycle='yr').aggregate(Sum("price", default=0))
    return Response(data)