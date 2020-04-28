from django.contrib import admin
from django.urls import path
from search_service.views import home, searchLatLon
from auth_service.views import callback, logout, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search_lat_lon/', searchLatLon, name='search_lat_lon'),
    path('login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout')
]
