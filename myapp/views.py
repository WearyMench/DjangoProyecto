"""Este es donde se hacen las vistas de las paginas."""
from django.http import HttpResponse
# Create your views here.


def hello(request):
    return HttpResponse("<h1>Hola Mundo</h1>")


def About(request):
    return HttpResponse("<h1>About</h1>")
