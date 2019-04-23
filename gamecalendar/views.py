import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
import requests
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from gamecalendar.models import Game


def view_games(request):
    game_list = Game.objects.order_by('release_date').all()
    return render(request, 'gamescalendar/list.html', context={'game_list': game_list})


@require_GET
def search_games(request):
    search_name = request.GET.get('name')

    response = requests.get('https://api-v3.igdb.com/search',
                            data="""search "{}"; fields game.name;""".format(
                                search_name),
                            headers={"user-key": "68400254c758f0487efaf50486583bbc"})

    response_json = response.json()

    print(response_json)
    games = list(filter(lambda x: x is not None and type(x) is dict and x['name'] is not None,
                        map(lambda x: x.get('game', None), response_json)))

    return render(request, 'gamescalendar/add_game.html',
                  context={'games': games, 'searched': True, 'search_name': search_name})


def add_game(request, igdb_id=None):
    if request.method == 'GET':
        return render(request, 'gamescalendar/add_game.html')
    elif request.method == 'POST':
        if igdb_id is None:
            messages.add_message(request, messages.ERROR, 'Failed to add game')
            return render(request, 'gamescalendar/add_game.html')

        try:
            game = Game.objects.get(igdb_id=igdb_id)
        except Game.DoesNotExist:
            pass
        else:
            messages.add_message(request, messages.INFO, 'Game has already been added')
            return render(request, 'gamescalendar/add_game.html')

        response = requests.get('https://api-v3.igdb.com/games',
                                data="""fields cover,first_release_date,hypes,name,updated_at,url;
                                where id = {};""".format(
                                    igdb_id),
                                headers={"user-key": "68400254c758f0487efaf50486583bbc"})

        response_json = response.json()[0]

        new_game = Game(
            igdb_id=response_json['id'],
            cover=response_json['cover'],
            release_date=datetime.fromtimestamp(response_json['first_release_date']),
            hypes=response_json['hypes'],
            name=response_json['name'],
            updated_at=datetime.fromtimestamp(response_json['updated_at']),
            url=response_json['url']
        )
        new_game.save()

        messages.add_message(request, messages.SUCCESS, '{} has been added'.format(response_json['name']))
        return render(request, 'gamescalendar/add_game.html')
