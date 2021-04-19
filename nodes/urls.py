from django.urls import path, include
from .views import RegisterNodeViewSet, DisplayNodeViewSet

urlpatterns = [
    path('connectNode/', RegisterNodeViewSet.as_view(), name='node-register'),
    path('path/', DisplayNodeViewSet.as_view(), name='path'),

]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
