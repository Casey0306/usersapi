from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView,\
    ListAPIView, CreateAPIView
from rest_framework.views import APIView
from .serializers import GetTokenSerializer, GetUsersSerializer,\
    CreateUserSerializer, UpdateUserSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User
from .pagination import StandardResultsSetPagination


class GetTokenView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'token': serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class GetUsersView(ListAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GetUsersSerializer
    authentication_class = JSONWebTokenAuthentication
    pagination_class = StandardResultsSetPagination


class CreateUserView(APIView):

    permission_classes = (IsAdminUser,)
    serializer_class = CreateUserSerializer
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED

        return Response(serializer.data, status=status_code)


class GetUserView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = GetUsersSerializer
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, pk):
        try:
            param_user = User.objects.filter(id=pk).first()
            token_user = request.user
            status_code = status.HTTP_200_OK
            if param_user.id == token_user.id or token_user.is_staff is True:
                response = {
                    "id": param_user.id,
                    "username": param_user.username,
                    "first_name": param_user.first_name,
                    "last_name": param_user.last_name,
                    "is_active": param_user.is_active,
                    "last_login": param_user.last_login,
                    "is_superuser": param_user.is_superuser,
                }
            else:
                status_code = status.HTTP_403_FORBIDDEN
                response = {
                    'success': 'false',
                    'status code': status_code,
                    'message': 'You dont have enough permission',
                }
        except Exception as e:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'false',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User does not exists',
                    'error': str(e)
                }
        return Response(response, status=status_code)


class UpdateUserView(APIView):

    permission_classes = (IsAdminUser,)
    serializer_class = UpdateUserSerializer
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def patch(self, request, pk):
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            testmodel_object = self.get_object(pk)
        except Exception:
            return Response({'error': 'User does not exists'},
                            status=status_code)
        serializer = UpdateUserSerializer(testmodel_object,
                                          data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class DeleteUserView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def delete(self, request, pk):
        try:
            param_user = User.objects.filter(id=pk).first()
            token_user = request.user
            if param_user.id == token_user.id or token_user.is_staff is True:
                User.objects.filter(id=pk).delete()
                status_code = status.HTTP_204_NO_CONTENT
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'User successfully deleted',
                }
            else:
                status_code = status.HTTP_403_FORBIDDEN
                response = {
                    'success': 'false',
                    'status code': status_code,
                    'message': 'You dont have enough permission',
                }
        except Exception as e:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'false',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User does not exists',
                    'error': str(e)
                }
        return Response(response, status=status_code)
