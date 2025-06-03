from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
import logging
from .models import *

logger = logging.getLogger(__name__)


def seasons(request):
    seasons = Season.objects.all()
    template = loader.get_template("all_seasons.html")
    context = {
        "seasons": seasons,
    }
    return HttpResponse(template.render(context, request))


def season(request, id):
    season = Season.objects.get(id=id)
    episodes = Episode.objects.filter(season=season)
    template = loader.get_template("episodes_in_season.html")
    context = {"season": season, "episodes": episodes}
    return HttpResponse(template.render(context, request))


def episodes(request):
    episodes = Episode.objects.all()
    template = loader.get_template("all_episodes.html")
    context = {
        "episodes": episodes,
    }
    return HttpResponse(template.render(context, request))


def episode(request, id):
    ep = Episode.objects.get(id=id)
    template = loader.get_template("episode.html")
    context = {"ep": ep}
    return HttpResponse(template.render(context, request))


def prev_episode(request, id):
    ep = Episode.objects.get(id=id)
    prev_ep = ep.prev()
    if prev_ep:
        template = loader.get_template("episode.html")
        context = {"ep": prev_ep}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("This is the first season, first epidson", status=404)


def next_episode(request, id):
    ep = Episode.objects.get(id=id)
    next_ep = ep.next()
    if next_ep:
        template = loader.get_template("episode.html")
        context = {"ep": next_ep}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("No more epidson!!", status=404)


def casts(request):
    casts = Cast.objects.all().values()
    template = loader.get_template("all_casts.html")
    context = {
        "casts": casts,
    }
    return HttpResponse(template.render(context, request))


@login_required
@require_POST
def like_episode(request, id):
    try:
        episode = Episode.objects.get(id=id)
        if request.user in episode.likes.all():
            episode.likes.remove(request.user)
            liked = False
            logger.info(f"User {request.user.username} unliked episode {episode}")
        else:
            episode.likes.add(request.user)
            liked = True
            logger.info(f"User {request.user.username} liked episode {episode}")

        return JsonResponse({"liked": liked, "likes_count": episode.likes.count()})
    except ObjectDoesNotExist:
        logger.error(f"Episode with id {id} not found")
        return JsonResponse({"error": "Episode not found"}, status=404)
    except Exception as e:
        logger.error(f"Error in like_episode: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
