from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Fund, Donation
from .serializers import FundSerializer, DonationSerializer, DonationCreateSerializer
from person.permissions import IsAdmin
from openpyxl import Workbook
from django.http import HttpResponse
from datetime import datetime

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
            # The DonationSerializer will now automatically include user details
            donation_data = DonationSerializer(donation).data
            
            # Fetch the related fund and serialize its details
            fund = donation.fund
            fund_serializer = FundSerializer(fund)
            
            # Add fund details to the donation data
            donation_data['fund'] = fund_serializer.data
            
            donations.append(donation_data)

        return Response(donations, status=200)

class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()
        return Response(DonationSerializer(donation).data, status=status.HTTP_201_CREATED)



class DonationDetailView(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    permission_classes = []

    def get(self, request, *args, **kwargs):
        fund_id = kwargs.get('pk')
        try:
            fund = self.get_queryset().get(id=fund_id)
            donations = Donation.objects.filter(fund=fund).order_by('-amount')[:3]
            serializer = DonationSerializer(donations, many=True)

            total_donations = sum(d['amount'] for d in serializer.data if d['amount'] is not None)

            return Response({
                "donations": serializer.data,
                "total_donations": total_donations
            }, status=200)

        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=404)

class DonationDeleteView(generics.DestroyAPIView):
    queryset = Donation.objects.all()
    permission_classes = []  # No permission restrictions

class FundExcelDownloadView(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    permission_classes = []

    def get(self, request, *args, **kwargs):
        fund_id = kwargs.get('pk')
        try:
            fund = self.get_queryset().get(id=fund_id)
            donations = Donation.objects.filter(fund=fund)
            
            # Create a new Excel workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Fund Details"

            # Write Fund Details
            ws.append(["Fund Details"])
            ws.append(["Title", fund.title])
            ws.append(["Description", fund.description])
            ws.append(["Creator", fund.creator.username])
            ws.append(["Amount", fund.amount])
            ws.append(["Status", fund.status])
            ws.append([])  # Empty row for spacing

            # Write Donations Header
            ws.append(["Donations"])
            ws.append(["Donor", "Amount", "Payment Status", "Transaction ID", "Message", "Donation Date"])

            # Write Donation Details
            for donation in donations:
                ws.append([
                    donation.donor.username,
                    donation.amount,
                    donation.payment_status,
                    donation.transaction_id,
                    donation.message,
                    donation.donation_date.replace(tzinfo=None)
                ])

            # Create response
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=fund_{fund_id}_details.xlsx'
            
            # Save workbook to response
            wb.save(response)
            return response

        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=404)

class AllFundsExcelDownloadView(generics.ListAPIView):
    queryset = Fund.objects.all()
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            funds = self.get_queryset()
            
            # Create a new Excel workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "All Funds and Donations"

            # Write header for funds
            ws.append(["All Funds and Donations Report"])
            ws.append(["Generated on", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            ws.append([])  # Empty row for spacing

            # Write Fund Details
            for fund in funds:
                ws.append(["Fund Details"])
                ws.append(["Title", fund.title])
                ws.append(["Description", fund.description])
                ws.append(["Creator", fund.creator.username])
                ws.append(["Amount", fund.amount])
                ws.append(["Status", fund.status])
                ws.append([])  # Empty row for spacing

                # Write Donations Header
                ws.append(["Donations for this Fund"])
                ws.append(["Donor", "Amount", "Payment Status", "Transaction ID", "Message", "Donation Date"])

                # Write Donation Details
                donations = Donation.objects.filter(fund=fund)
                for donation in donations:
                    ws.append([
                        donation.donor.username,
                        donation.amount,
                        donation.payment_status,
                        donation.transaction_id,
                        donation.message,
                        donation.donation_date.replace(tzinfo=None)
                    ])
                
                ws.append([])  # Empty row for spacing between funds
                ws.append([])  # Another empty row for better readability

            # Create response
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=all_funds_and_donations.xlsx'
            
            # Save workbook to response
            wb.save(response)
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=500) 