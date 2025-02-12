from django.http import JsonResponse


def custom_404(request, exception):
    return JsonResponse({'error': f'{str(exception)} not found'}, status=404)
