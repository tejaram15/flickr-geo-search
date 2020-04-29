# Global Imports
import logging

# Logging Setup.
# TODO: Add Global Logger Can use Sentry.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def constructPhotoUrl(farmId, serverId, id, secret, size):
    '''
    Utility function to construct and return a URL from given parameters.
    Reference: https://www.flickr.com/services/api/misc.urls.html
    '''
    if size not in ['t', 'c']:
        logger.error("Incorrect construction parameters.")
        raise NotImplementedError("Incorrect construction parameters.")
    baseUrl = f"https://farm{farmId}.staticflickr.com/{serverId}/{id}_{secret}_{size}.jpg"
    return baseUrl
