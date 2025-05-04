from django.urls import path
from .views import (
    FundListView,
    FundCreateView,
    FundDetailView,
    FundDeleteView,
    DonationListView,
    DonationCreateView,
    DonationDetailView,
    DonationDeleteView,
    FundExcelDownloadView,
    AllFundsExcelDownloadView
)

urlpatterns = [
    path('', FundListView.as_view(), name='fund-list'),  # List all funds
    path('create/', FundCreateView.as_view(), name='fund-create'),  # Create a new fund
    path('funds/<int:pk>/', FundDetailView.as_view(), name='fund-detail'),  # Retrieve/update a fund
    path('funds/<int:pk>/delete/', FundDeleteView.as_view(), name='fund-delete'),  # Delete a fund
    path('donations/', DonationListView.as_view(), name='donation-list'),  # List all donations
    path('donations/create/', DonationCreateView.as_view(), name='donation-create'),  # Create a new donation
    path('fund/<int:pk>/donations/', DonationDetailView.as_view(), name='donation-detail'),  # Fetch donations by fund ID
    path('donations/<int:pk>/delete/', DonationDeleteView.as_view(), name='donation-delete'),  # Delete a donation
    path('funds/<int:pk>/download/', FundExcelDownloadView.as_view(), name='fund-download'),  # Download fund details as Excel
    path('funds/download-all/', AllFundsExcelDownloadView.as_view(), name='all-funds-download'),  # Download all funds and donations as Excel
] 