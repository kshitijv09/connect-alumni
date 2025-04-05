from django.urls import path
from .views import SignUpView, UserDetailView, UserVerificationView, UserListView, UserUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/verify/', UserVerificationView.as_view(), name='user-verify'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
] 