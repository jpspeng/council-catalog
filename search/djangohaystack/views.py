from django.shortcuts import render

# Create your views here.
from haystack.query import SearchQuerySet

from django.views.generic import TemplateView


def home(request):
	pass



class SearchView(TemplateView):

    template_name = 'mysearch/search.html'


search_view = SearchView.as_view()