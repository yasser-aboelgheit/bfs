from django.urls import path
# from .views import PassengerAPIView, SelfRegisterViewSet
from .views import RegisterNodeViewSet, DisplayNodeViewSet

urlpatterns = [
    # path('nodes/', PassengerAPIView.as_view(), name='passengers'),
    path('connectNode/', RegisterNodeViewSet.as_view(), name='node-register'),
    path('path/', DisplayNodeViewSet.as_view(), name='node-register'),

]
