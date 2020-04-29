# Global Imports
import logging

# Django Specific Imports
from django.shortcuts import reverse, render

# App Specific Imports
from search_service.forms import LatLonSearchForm, FavouritesForm, LocationTagForm

# Logging Setup.
# TODO: Add Global Logger Can use Sentry.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def home(request):
    '''
    Rendering View for Home Screen.
    '''
    template = 'home.html'
    context = {
        'search_form': LatLonSearchForm(),
        'search_url': reverse('search_lat_lon'),
        'location_form': LocationTagForm(),
        'title': "Flickr Geo Search"
    }
    return render(request, template, context)


def favourites(request):
    '''
    Rendering View for Favourites Screen.
    '''
    template = 'favourites.html'
    context = {
        'search_url': reverse('view_favourites_list'),
        'title': "Favourite Flickr Photos"
    }
    return render(request, template, context)
