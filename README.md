# Flickr Geo Search

This app demonstrates the use of Flickr API to search public images using python and Django framework.

## Setup Instructions:

### Using Source Build:

1. Create a virtual environment.\
   `python3 -m venv flickr`

2. Install all the dependencies provided via the requirements.txt file.\
   `pip3 install requirements.txt`

3. Create a Flickr App and get your api key and secret from [Flickr Api](https://www.flickr.com/services/api/keys/).

4. Create a `secrets.json` file consisting of the following fields. The parameters `FLICKR_API_KEY` and `FLICKR_API_SECRET` are to be fetched from the app created in Flickr. `PER_PAGE` argument is the number of images to be shown per page. (This option won't work if this is more than 100 as there is a restriction from Flickr API.)

```
{
  "FLICKR_API_KEY": "XXXXX",
  "FLICKR_API_SECRET": "XXXXX",
  "PER_PAGE": "10"
}
```

5. Run migrations.\
   `python3 manage.py migrate`

6. Run the app via following command:\
   `python3 manage.py runsslserver`

## App Description

This app is structured in the following way:

1.  `search_service` where all the code resides. This is the main service of the application.
2.  `flickr_geo_search` this is the main app where all the settings, urls and configuration are available.

<style>.heart{color:#e25555;font-size:18px}</style>

Made with <span class="heart">❤</span> by Mindfire.
