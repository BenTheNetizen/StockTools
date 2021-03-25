import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class SubredditForm(forms.Form):
    subreddit = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'placeholder' : 'Enter a subreddit that discusses stocks (ex: wallstreetbets, stocks, robinhood, etc.)'}), empty_value="stocks", )

    def clean_subreddit(self):
        data = self.cleaned_data['subreddit']

        #Check if subreddit entered was not a string
        if data.isnumeric():
            raise ValidationError(_('Invalid input - cannot be integers'))

        return data
