import json
import logging
import flickrapi

from django.conf import settings
from django.db.models import F
from django.shortcuts import reverse, render
from django.http import JsonResponse
from search_service.forms import LatLonSearchForm, FavouritesForm, LocationTagForm
from search_service.models import Favourites, LocationTag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def home(request):
    template = 'home.html'
    context = {
        'search_form': LatLonSearchForm(),
        'search_url': reverse('search_lat_lon'),
        'location_form': LocationTagForm(),
        'title': "Flickr Geo Search"
    }
    return render(request, template, context)


def favourites(request):
    template = 'favourites.html'
    context = {
        'search_url': reverse('view_favourites_list'),
        'title': "Favourite Flickr Photos"
    }
    return render(request, template, context)


def constructPhotoUrl(farmId, serverId, id, secret, size):
    if size not in ['t', 'c']:
        logger.error("Incorrect construction parameters.")
        raise NotImplementedError("Incorrect construction parameters.")
    baseUrl = f"https://farm{farmId}.staticflickr.com/{serverId}/{id}_{secret}_{size}.jpg"
    return baseUrl


def searchLatLon(request):
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
            logger.error(exc)
            response['errors'] = exc.__str__()
            status = 500
    else:
        response['errors'] = form.errors.get_json_data(escape_html=True)
        status = 500
    return JsonResponse(response, status=status)


def addToFavourites(request):
    data = json.loads(request.body.decode('utf-8'))
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


def viewFavouritesList(request):
    favourites_list = Favourites.objects.all().order_by('-created_at').annotate(
        thumbnailUrl=F('photo_original_url')).values('thumbnailUrl')
    favourites_list = [fav for fav in favourites_list]
    response = {
        'photos': favourites_list
    }
    return JsonResponse(response)


def addLocationTag(request):
    data = json.loads(request.body.decode('utf-8'))
    form = LocationTagForm(data)
    response = {}
    status = 200
    if form.is_valid():
        obj = LocationTag.objects.filter(
            location_name=form.cleaned_data['location_name'])
        if obj.count() > 0:
            logger.info("A Location with this name already exists.")
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


def getLocationTags(request):
    location_tags_list = LocationTag.objects.all().values(
        'location_name', 'latitude', 'longitude')
    location_tags_list = [loc for loc in location_tags_list]
    response = {
        'locations': location_tags_list
    }
    return JsonResponse(response)
