from shared.decorators import method_check

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@method_check(method='GET')
def game_list(request):
    # if request.method == 'GET':
    #     games = serializers.serialize('json', Game.objects.all())
    #     games_data = [{'name': game.name, 'description': game.description} for game in games]
    #     return JsonResponse({'games': games_data}, status=200)
    # return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    data = GameSerializer(Game.objects.all())
    return data.json_response()


@method_check(method='GET')
def games_detail(request, slug):
    data = GameSerializer(Game.objects.get(slug=slug))
    return data.json_response()


@method_check(method='GET')
def review_list(request):
    data = ReviewSerializer(Review.objects.all())
    return data.json_response()


@method_check(method='GET')
def review_detail(request, pk):
    data = GameSerializer(Game.objects.get(pk=pk))
    return data.json_response()


@method_check('POST')
def add_review(request):
    pass
