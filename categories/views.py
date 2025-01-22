from .models import Category

# Create your views here.


def category_list(request):
    categories = Category.objects.all()


def category_detail(request, name):
    category = Category.objects.get(name=name)
