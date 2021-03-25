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

class NumberOfPostsForm(forms.Form):
    num = forms.IntegerField(help_text="Enter the number of posts you want to analyze. (integers only)")

    def clean_num(self):
        data = self.cleaned_data['num']

        return data

from .models import NameObject
#class should be called what we want our form to be called
class CreateNewList(forms.Form):
    subreddit = forms.CharField(max_length=200, help_text="enter a subreddit")
    num = forms.IntegerField(help_text="enter the number of posts you want to analyze")
    # class Meta:
    #     model = NameObject
    #     fields = '__all__'
