# Global Imports
import json
import logging
import flickrapi

# Django Specific Imports
from django.db.models import F
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import reverse, render
from django.views.decorators.http import require_http_methods

# App Specific Imports
from search_service.utils import constructPhotoUrl
from search_service.models import Favourites, LocationTag
from search_service.forms import LatLonSearchForm, FavouritesForm, LocationTagForm

# Logging Setup.
# TODO: Add Global Logger Can use Sentry.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@require_http_methods(["GET"])
def searchLatLon(request):
    '''
    Search Api which recieves Latitude and Longitude to search public images.
    @param request (Request Object): Request from client.
    @param current_page (Integer): Accept Current Page as parameter.
    @param latitude (Float): Latitude Range -90 to 90 degrees.
    @param longitude (Float): Longitude Range -180 to 180 degrees
    '''
    current_page = request.GET.get('current_page', 1)
    flickr = flickrapi.FlickrAPI(
        settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='parsed-json')
    if isinstance(current_page, str):
        try:
            current_page = int(current_page)
        except ValueError as exc:
            logger.error("Incorrect page number returning page 1")
            current_page = 1
    form = LatLonSearchForm(request.GET)
    response = {}
    status = 200
    response["current_page"] = current_page
    if form.is_valid():
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        response['photos'] = []
        try:
            photos = flickr.photos.search(
                latitude=latitude, longitude=longitude, per_page=settings.PER_PAGE, current_page=current_page)
            # After receiving a photo object from Flickr API the url can be constructed as described in the following link:
            # https://www.flickr.com/services/api/misc.urls.html
            for photo in photos['photos']['photo']:
                farmId = photo['farm']
                serverId = photo['server']
                id = photo['id']
                secret = photo['secret']
                response['photos'].append({
                    'title': photo['title'],
                    'thumbnailUrl': constructPhotoUrl(farmId, serverId, id, secret, 't'),
                    'mediumUrl': constructPhotoUrl(farmId, serverId, id, secret, 'c'),
                })
        except Exception as exc:
            logger.error(
                "Error occurred while searching photo from flickr : %s", exc)
            response['errors'] = f"Error occurred while searching photo from flickr : {exc}"
            status = 500
    else:
        response['errors'] = form.errors.get_json_data(escape_html=True)
        status = 500
    return JsonResponse(response, status=status)


@require_http_methods(["POST"])
def addToFavourites(request):
    '''
    Api that adds a given URL to favourites.
    @param request (Request Object): Request object.
    @param photo_original_url (URL): Original Photo URL saved directly. 
    (Can be Hashed or indexed for fast searching)
    '''
    response = {}
    status = 200
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as exc:
        logger.error("Incorrect data received %s", exc)
        response['error'] = f"Incorrect data received {exc}"
        return JsonResponse({}, status=status)
    form = FavouritesForm(data)
    response = {}
    status = 200
    if form.is_valid():
        try:
            obj = Favourites(**form.cleaned_data)
            obj.save()
            response["success"] = "Successfully added to favourites."
        except Exception as exc:
            logger.exception("Error occurred while adding this URL : %s", exc)
            response["errors"] = "Error occurred while adding this URL : %s", exc
            status = 500
    else:
        response["errors"] = form.errors.get_json_data(escape_html=True)
        status = 500
    return JsonResponse(response, status=status)


@require_http_methods(["GET"])
def viewFavouritesList(request):
    '''
    API return a list of favourites in reverse chronological order of creation.
    '''
    favourites_list = Favourites.objects.all().order_by('-created_at').annotate(
        thumbnailUrl=F('photo_original_url')).values('thumbnailUrl')
    favourites_list = [fav for fav in favourites_list]
    response = {
        'photos': favourites_list
    }
    return JsonResponse(response)


@require_http_methods(["POST"])
def addLocationTag(request):
    '''
    API to add a location tag to a latitude/longitude pair.
    (Intended for use via `fetch` Javascript API.) => Implemented this way to demonstrate available options.
    @param request (Request Object): Request Object.
    @param latitude (Float): Latitude Range -90 to 90 degrees.
    @param longitude (Float): Longitude Range -180 to 180 degrees
    '''
    response = {}
    status = 200
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as exc:
        logger.error("Incorrect data received %s", exc)
        response['error'] = f"Incorrect data received {exc}"
        return JsonResponse({}, status=status)
    form = LocationTagForm(data)
    if form.is_valid():
        obj = LocationTag.objects.filter(
            location_name=form.cleaned_data['location_name'])
        if obj.count() > 0:
            logger.info("A Location with this name already exists.")
            obj = obj.first()
            obj.latitude = form.cleaned_data['latitude']
            obj.longitude = form.cleaned_data['longitude']
            obj.save()
            response["success"] = "Successfully updated location tag."
        else:
            try:
                obj = LocationTag(**form.cleaned_data)
                obj.save()
                response["success"] = "Successfully added to location tag."
            except Exception as exc:
                logger.exception(
                    "Exception occurred while adding to LocationTag: %s", exc)
                response["errors"] = "Exception occurred while adding to LocationTag: %s", exc
                status = 500
    else:
        response["errors"] = form.errors.get_json_data(escape_html=True)
        status = 500

    return JsonResponse(response, status=status)


@require_http_methods(["GET"])
def getLocationTags(request):
    '''
    API to get a list of location tags/latitude-longitude pairs.
    '''
    location_tags_list = LocationTag.objects.all().values(
        'location_name', 'latitude', 'longitude')
    location_tags_list = [loc for loc in location_tags_list]
    response = {
        'locations': location_tags_list
    }
    return JsonResponse(response)
