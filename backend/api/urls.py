from django.urls import path
from . import views


# URLs
urlpatterns = [
    path('subscriptions', views.subscriptionList, name='get_subs'),
    path('subscriptions/<int:id>', views.deleteSubscription, name='Delete Subscription'),
    path('total_monthly', views.getTotalMonthly, name='Get Monthly Spends'),
    path('total_yearly', views.getTotalYearly, name='Get Yearly Spends')
]
