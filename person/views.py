from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserRole
from .serializers import UserSerializer, UserRoleSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin
from rest_framework.views import APIView

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'user': serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to create user',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'User deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class UserVerificationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, pk):
        user = self.get_object()
        user.is_verified = True
        user.save()
        return Response({
            'message': 'User verified successfully',
            'user': self.get_serializer(user).data
        }, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        queryset = User.objects.all()
        
        filters = request.data
        name = filters.get('name', None)
        company = filters.get('company', None)
        graduation_year = filters.get('graduation_year', None)
        role_name = filters.get('role_name', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if company:
            queryset = queryset.filter(company__icontains=company)
        if graduation_year:
            queryset = queryset.filter(graduation_year=graduation_year)
        if role_name:
            try:
                role = UserRole.objects.get(name=role_name.upper())
                queryset = queryset.filter(role=role)
            except UserRole.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': f'Role {role_name} does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK) 