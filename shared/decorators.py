from django.http import HttpResponseNotAllowed


def method_check(method):
    def inner_func(func):
        def wrapper(*args, **kwargs):
            if args[0].method == method:
                return func(*args, **kwargs)
            return HttpResponseNotAllowed('GET')

        return wrapper

    return inner_func


# def auth_check(func):
#     def wrapper(*args, **kwargs):
