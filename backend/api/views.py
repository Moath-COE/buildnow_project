from django.shortcuts import render
from .serializer import SubscriptionSerializer
from .models import Subscriptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from decimal import Decimal
from django.db.models import Sum

# Create your views here.

# Get & Create subscriptions
@api_view(['GET', 'POST'])
def subscriptionList(request):
    if request.method == 'GET':
        subs = Subscriptions.objects.all()
        # for sub in subs:
        #     sub.next_payment = sub.calculate_next_payment
        #     sub.total_spends = sub.calculate_total_spends
        #     sub.save(update_fields=['next_payment', 'total_spends'])
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
    

# Get total spends
@api_view(['GET'])
def getTotal(request):
    # subs = Subscriptions.objects.all()
    # totalSpends = Decimal('0.00')
    # for sub in subs:
    #     totalSpends += sub.calculate_total_spends
    data = Subscriptions.objects.all().aggregate(Sum("total_spends", default=0))
    return Response(data['total_spends__sum'])  

# # Get total spends per month
# @api_view(['GET'])
# def getTotalMonthly(request):
#     subs = Subscriptions.objects.filter(cycle='mn')
#     monthlySpends = Decimal('0.00')
#     for sub in subs:
#         monthlySpends += sub.calculate_total_spends
#     return Response(monthlySpends)  

# # Get total spends per year
# @api_view(['GET'])
# def getTotalYearly(request):
#     subs = Subscriptions.objects.filter(cycle='mn')
#     yearlySpends = Decimal('0.00')
#     for sub in subs:
#         yearlySpends += sub.calculate_total_spends
#     return Response(yearlySpends)  