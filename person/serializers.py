from rest_framework import serializers
from .models import User, UserRole
from django.core.validators import RegexValidator

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'name', 'description')

class UserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(read_only=True)
    role_name = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='Password must be at least 8 characters long and contain both letters and numbers.'
            )
        ]
    )
    email = serializers.EmailField(
        required=False,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email address.'
        }
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'company', 'graduation_year', 'bio', 'profile_picture', 'email', 'password', 'phone_number', 'department', 'linkedin_url', 'role', 'role_name', 'is_verified')
        extra_kwargs = {
            'username': {'required': True, 'error_messages': {
                'required': 'Username is required.',
                'blank': 'Username cannot be blank.'
            }},
            'password': {'write_only': True, 'required': False},
            'is_verified': {'read_only': True},
            'email': {'required': False}
        }

    def validate(self, data):
        # Custom validation for graduation year
        if 'graduation_year' in data:
            from datetime import datetime
            current_year = datetime.now().year
            if data['graduation_year'] and data['graduation_year'] > current_year:
                raise serializers.ValidationError({
                    'graduation_year': f'Graduation year cannot be greater than {current_year}'
                })

        # Validate username uniqueness
        username = data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'username': 'This username is already taken.'
            })

        # Validate email uniqueness
        email = data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'This email is already registered.'
            })

        return data

    def create(self, validated_data):
        role_name = validated_data.pop('role_name', 'USER')
        try:
            role = UserRole.objects.get(name=role_name)
        except UserRole.DoesNotExist:
            role = UserRole.objects.get(name='USER')
        
        try:
            user = User.objects.create_user(**validated_data)
            user.role = role
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError({
                'error': f'Failed to create user: {str(e)}'
            })

    def update(self, instance, validated_data):
        # Handle user updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance 