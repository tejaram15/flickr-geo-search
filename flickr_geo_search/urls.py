from django.contrib import admin
from django.urls import path
from search_service.views import home, searchLatLon, addToFavourites, viewFavouritesList, favourites, addLocationTag, getLocationTags

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search_lat_lon/', searchLatLon, name='search_lat_lon'),
    path('favourites/', favourites, name='favourites'),
    path('add_to_favourites/', addToFavourites, name='add_to_favourites'),
    path('view_favourites_list', viewFavouritesList, name='view_favourites_list'),
    path('get_location_tags/', getLocationTags, name='get_location_tags'),
    path('add_location_tag/', addLocationTag, name='add_location_tag'),
]
