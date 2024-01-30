from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet,
    get_organisation,
    VerifyOrganisationView
)

router = DefaultRouter()

router.register("", OrganizationViewSet, basename="create")

urlpatterns = [
    path("", include(router.urls)),
    path('<str:uuid>/', get_organisation, name='organisation'),
    path('verify/<str:uuid>/', VerifyOrganisationView.as_view(), name='verify'),
]
