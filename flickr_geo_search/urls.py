# Django Specific Imports
from django.urls import path
from django.contrib import admin

# Rendering View Imports
from search_service.rendering_views import home, favourites
from search_service.api_views import searchLatLon, addToFavourites, \
    viewFavouritesList, addLocationTag, getLocationTags

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Rendering URLS
    path('', home, name='home'),
    path('favourites/', favourites, name='favourites'),

    # API URLS
    path('search_lat_lon/', searchLatLon, name='search_lat_lon'),
    path('add_location_tag/', addLocationTag, name='add_location_tag'),
    path('add_to_favourites/', addToFavourites, name='add_to_favourites'),
    path('get_location_tags/', getLocationTags, name='get_location_tags'),
    path('view_favourites_list', viewFavouritesList, name='view_favourites_list')
]
