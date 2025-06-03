from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import *

def seasons(request):
  seasons = Season.objects.all()
  template = loader.get_template('all_seasons.html')
  context = {
    'seasons': seasons,
  }
  return HttpResponse(template.render(context, request))

def season(request, id):
  season = Season.objects.get(id = id)
  episodes = Episode.objects.filter(season = season)
  template = loader.get_template('episodes_in_season.html')
  context = {
    'season': season,
    'episodes': episodes
  }
  return HttpResponse(template.render(context, request))

def episodes(request):
  episodes = Episode.objects.all()
  template = loader.get_template('all_episodes.html')
  context = {
    'episodes': episodes,
  }
  return HttpResponse(template.render(context, request))

def episode(request, id):
    ep = Episode.objects.get(id=id)
    template = loader.get_template('episode.html')
    context = {
      'ep': ep
    }
    return HttpResponse(template.render(context, request))
      
def prev_episode(request, id):
    ep = Episode.objects.get(id=id)
    prev_ep = ep.prev()
    if prev_ep:
        template = loader.get_template('episode.html')
        context = {
            'ep': prev_ep
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("This is the first season, first epidson", status=404)

def next_episode(request, id):
    ep = Episode.objects.get(id=id)
    next_ep = ep.next()
    if next_ep:
        template = loader.get_template('episode.html')
        context = {
            'ep': next_ep
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("No more epidson!!", status=404)


def casts(request):
  casts = Cast.objects.all().values()
  template = loader.get_template('all_casts.html')
  context = {
    'casts': casts,
  }
  return HttpResponse(template.render(context, request))
  