from rest_framework import serializers
from .models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from re import compile


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class GetTokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150, write_only=True)
    token = serializers.CharField(max_length=150, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User does not exists'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Incorrect username or password'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }


class GetUsersSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=30, read_only=True)
    last_name = serializers.CharField(max_length=150, read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active',
                  'last_login', 'is_superuser']


class CreateUserSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    is_active = serializers.BooleanField()
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name',
                  'last_name', 'is_active',
                  'last_login', 'is_superuser']

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        USERNAME_REGEX = compile(r'^[\w.@+-]+$')
        PASSWORD_REGEX = compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')

        user = User.objects.filter(username=username).first()

        if user:
            raise serializers.ValidationError(
                r'The username already exists')

        if USERNAME_REGEX.match(username) is None:
            raise serializers.ValidationError(
                r'Please enter username compatible with ^[\w.@+-]+$')

        if PASSWORD_REGEX.match(password) is None:
            raise serializers.ValidationError(
                r'Please enter password compatible '
                r'with ^(?=.*[A-Z])(?=.*\d).{8,}$')
        return attrs

    def create(self, validated_data):
        user_temp = User.objects.create_user(
            username=validated_data.get('username', None),
            password=validated_data.get('password', None),
        )
        User.objects.filter(id=user_temp.id).update(
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
            is_active=validated_data.get('is_active', None),
        )
        user = User.objects.filter(id=user_temp.id).first()
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    is_active = serializers.BooleanField()
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name',
                  'last_name', 'is_active',
                  'last_login', 'is_superuser']

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        USERNAME_REGEX = compile(r'^[\w.@+-]+$')
        PASSWORD_REGEX = compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')

        if username is not None and USERNAME_REGEX.match(username) is None:
            raise serializers.ValidationError(
                r'Please enter username compatible with ^[\w.@+-]+$')

        if password is not None and PASSWORD_REGEX.match(password) is None:
            raise serializers.ValidationError(
                r'Please enter password compatible '
                r'with ^(?=.*[A-Z])(?=.*\d).{8,}$')
        return attrs

    def update(self, instance, validated_data):
        user = User.objects.get(id=instance.id)
        User.objects.filter(id=instance.id).update(**validated_data)
        password = validated_data.get('password', None)
        if password is not None:
            user = User.objects.get(id=instance.id)
            user.set_password(password)
            user.save()
        return user
