from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search Books')


class RatingForm(forms.Form):
    rating = forms.DecimalField(max_digits=2, decimal_places=1, min_value=1.0, max_value=5.0)
