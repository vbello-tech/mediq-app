from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.account_list),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login api view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
