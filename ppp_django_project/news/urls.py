from django.urls import path
from .views import index, add, get

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name="add"),
    path('<int:id>/', get, name='get'),
]
