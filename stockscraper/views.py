from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import praw
import nltk
import pandas as pd

import os
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError

from stockscraper.forms import SubredditForm
from stockscraper.models import Counter
import openpyxl

parentDir = os.path.dirname(__file__)
newPath = os.path.join(parentDir, 'nltk_data')
nltk.data.path.append(newPath)

def index(request):
    """View function for the home page of the site."""
    form = SubredditForm()
    count = Counter()
    tickers = None
    if request.method == 'POST':
        print(request.POST)
        form = SubredditForm(request.POST)
        user_subreddit = request.POST.get('subreddit')
        tickers = analyze_comments(5, user_subreddit)
        """
        try:
            tickers = analyze_comments(5, user_subreddit)
        except:
            tickers = None
            error_message = "You have entered an invalid subreddit. Please try again."
        """

    print(tickers)
    context = {
        "form": form,
        "tickers" : tickers,
    }
    return render(request, 'index.html/', context)

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 19:43:08 2021

@author: BenTheNetizen
"""



def get_excel_data(workbook_path):
    wb = openpyxl.load_workbook(workbook_path)
    worksheet = wb["Sheet1"]
    excel_data = list()

    for row in worksheet.iter_rows():
        excel_data.append(row[0].value)

    return excel_data

def get_file_path(filename):
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, filename)

    return file_path

def analyze_comments(num, user_input):
    nltk.download('punkt')


    nyse = get_excel_data(get_file_path('nyse.xlsx'))
    nasdaq = get_excel_data(get_file_path('nasdaq.xlsx'))
    english_words = get_excel_data(get_file_path('common_words.xlsx'))
    english_words = [x.upper() for x in english_words if not isinstance(x, float) and x is not None]
    acronyms = get_excel_data(get_file_path('acronyms.xlsx'))

    reddit = praw.Reddit(client_id = 'PB9EdYv3u8rqhw',
                         client_secret = 'U7JU7azYdF_vWb3is5FdGA0_4Q16cA',
                         user_agent='https://github.com/BenTheNetizen')

    subreddit = reddit.subreddit(user_input)

    num_comments = 0
    curr_comments = 0
    unread_comments = 0

    f = open(get_file_path('redditstream.txt'), "w+")

    print('\n')
    for submission in subreddit.hot(limit=num):
        try:
            f.write("TITLE: " + submission.title)
            print("Submission title: " + submission.title)
        except:
            print("Unable to read title")
        try:
            f.write("TEXT: " + submission.selftext)
        except:
            print("Unable to read submission text")

        for comment in submission.comments.list():
            try:
                f.write(comment.body + '\n')
                num_comments += 1
                curr_comments += 1

            except:
                unread_comments += 1


        print("Read comments: " + str(curr_comments))
        curr_comments = 0

    f.close()
    print('\n\n' + 60*'-')
    print("Unread comments: " + str(unread_comments))
    print("Total read comments: " + str(num_comments))
    print("The number next to each stock ticker is the level of interest. The tickers are displayed below in order of high to low interest.\n")

    f = open(get_file_path('redditstream.txt')).read()

    tokens = nltk.word_tokenize(f)

    tokens_l = [w.upper() for w in tokens]

    #breaks after this line
    freq = nltk.FreqDist(tokens_l)
    common_words = freq.most_common(100)
    print(common_words[1:5])

    for k, v in common_words:
        if (k in nyse or k in nasdaq) and k not in english_words and k not in acronyms and v > 3:
            if v > 3:
                tickers[k] = v


    print(tickers)
    print(str(len(tickers)) + ' tickers')
    return tickers
