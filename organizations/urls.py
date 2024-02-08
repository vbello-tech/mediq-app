from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationCreateAndFetchAll,
    OrganizationRetrieveUpdateDeleteView,
    VerifyOrganisationView,
    VerifyContactPersonView,
    send_invite,
    accept_invite
)

router = DefaultRouter()

# router.register("create-or-fetch-all", OrganizationViewSet, basename="create")

urlpatterns = [
    # path("", include(router.urls)),
    path('create-or-fetch-all/', OrganizationCreateAndFetchAll.as_view(), name="create_or_fetch_all"),
    path('<str:uuid>/', OrganizationRetrieveUpdateDeleteView.as_view(), name='fetch_update_delete'),
    path('<str:uuid>/verify/', VerifyOrganisationView.as_view(), name='verify_organization'),
    path('<str:uuid>/verify/contact-person/', VerifyContactPersonView.as_view(), name='verify_contact'),
    path('<str:uuid>/send-invite/', send_invite, name="send_invite"),
    path('accept-invite/<str:slug>/', accept_invite, name="accept_invite"),
]
