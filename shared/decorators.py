from django.http import JsonResponse


def method_check(method):
    def inner_func(func):
        def wrapper(*args, **kwargs):
            if args[0].method == method:
                return func(*args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        return wrapper

    return inner_func
