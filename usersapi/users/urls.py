from django.conf.urls import url
from .views import GetTokenView, GetUsersView, CreateUserView


urlpatterns = [
    url('get_token', GetTokenView.as_view(), name='get_token'),
    url('create_user', CreateUserView.as_view(), name='create_user'),
    url('get_users', GetUsersView.as_view(), name='get_all_users'),
    ]
