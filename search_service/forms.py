from django import forms
from search_service.models import Favourites, LocationTag


class LatLonSearchForm(forms.Form):
    latitude = forms.DecimalField(
        min_value=-90, max_value=90, required=True, max_digits=8, decimal_places=4)
    longitude = forms.DecimalField(
        min_value=-180, max_value=180, required=True, max_digits=8, decimal_places=4)


class FavouritesForm(forms.ModelForm):
    class Meta:
        model = Favourites
        fields = ['photo_original_url']


class LocationTagForm(forms.ModelForm):
    class Meta:
        model = LocationTag
        fields = ['location_name', 'latitude', 'longitude']
