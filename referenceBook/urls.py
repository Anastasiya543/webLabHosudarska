from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from referenceBook import views
from referenceBook.views import UserViewSet, index

app_name = "referenceBook"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'telephoneNumbers', views.TelephoneNumberViewSet, basename='telephoneNumbers')
telephone_numbers_router = routers.NestedSimpleRouter(router, r'telephoneNumbers', lookup='telephoneNumber')

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', UserViewSet.as_view(
        actions={'get': 'list', 'post': 'create'}), name='users-list'),
    path('users/<str:username>', UserViewSet.as_view(
        actions={'get': 'retrieve', 'head': 'exists', 'delete': 'destroy'}),
         name='users-detail'),
    path('', include(router.urls)),
    path('', include(telephone_numbers_router.urls)),
]
