from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Fund, Donation
from .serializers import FundSerializer, DonationSerializer
from person.permissions import IsAdmin

class FundListView(generics.ListAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = []  # No permission restrictions

class FundCreateView(generics.CreateAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = []  # No permission restrictions

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

class FundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = []  # No permission restrictions

class FundDeleteView(generics.DestroyAPIView):
    queryset = Fund.objects.all()
    permission_classes = []  # No permission restrictions

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = []  # No permission restrictions

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        donations = []

        for donation in queryset:
            # Serialize the donation data
            donation_data = DonationSerializer(donation).data
            
            # Fetch the related fund and serialize its details
            fund = donation.fund  # Access the related fund directly
            fund_serializer = FundSerializer(fund)  # Serialize the fund details
            
            # Add fund details to the donation data
            donation_data['fund'] = fund_serializer.data
            
            # Append the modified donation data to the list
            donations.append(donation_data)

        return Response(donations, status=200)

class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = []  # No permission restrictions

class DonationDetailView(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    serializer_class = DonationSerializer
    permission_classes = []  # No permission restrictions

    def get(self, request, *args, **kwargs):
        fund_id = kwargs.get('pk')  # Get fund ID from URL parameters
        try:
            fund = self.get_queryset().get(id=fund_id)  # Fetch fund by ID
            # Fetch donations related to the fund, sort by amount, and get top 3
            donations = Donation.objects.filter(fund=fund).order_by('-amount')[:3]
            serializer = DonationSerializer(donations, many=True)
            return Response(serializer.data, status=200)
        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=404)

class DonationDeleteView(generics.DestroyAPIView):
    queryset = Donation.objects.all()
    permission_classes = []  # No permission restrictions 