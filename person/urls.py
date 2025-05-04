from django.urls import path
from .views import (
    SignUpView,
    UserDetailView,
    UserVerificationView,
    UserListView,
    UserUpdateView,
    GoogleLoginView,
    CustomTokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/verify/', UserVerificationView.as_view(), name='user-verify'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 