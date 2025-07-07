from django.urls import path
from scraper.views.data_views import item_list, refresh_data
from scraper.views.auth_views import register, user_login, user_logout


urlpatterns = [

    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('items/', item_list, name='item-list'),
    path('refresh/', refresh_data, name='refresh-data'),
]