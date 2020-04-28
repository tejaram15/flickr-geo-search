import logging
import flickr_api

from django.conf import settings
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def login(request):
    if 'token' in request.session:
        token = request.session['token']
        logger.info("Taking token from session %s", token)
    else:
        token = None
        logger.info("No token in session")

    flickr_api.set_keys(api_key=settings.FLICKR_API_KEY,
                        api_secret=settings.FLICKR_API_SECRET)
    if not token:
        authHandler = flickr_api.auth.AuthHandler(
            callback=request.build_absolute_uri(reverse('callback')))
        request.session['authHandler'] = authHandler.todict()
        perms = "write"
        authUrl = authHandler.get_authorization_url(perms)
        return HttpResponseRedirect(authUrl)

    return HttpResponseRedirect('/')


def callback(request):
    logger.info('We got a callback from Flickr, store the token')
    token = request.GET.get('oauth_verifier')
    a = flickr_api.auth.AuthHandler()
    a = a.fromdict(request.session['authHandler'])
    a.set_verifier(token)
    flickr_api.set_auth_handler(a)
    request.session['token'] = token

    return HttpResponseRedirect('/')


def logout(request):
    logger.info("logging out")
    del request.session['token']
    return HttpResponseRedirect('/')
