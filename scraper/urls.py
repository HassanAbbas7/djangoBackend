from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # path(route=, view=, kwargs=, name=)
    # path('', lambda req: redirect('/start_scrape/')),
    path('', views.index , name='index'),
    path('start_scrape/', views.start_scrape, name="start_scrape"),
    path('API', views.APIcall, name="API")
]
