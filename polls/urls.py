from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'polls'
urlpatterns = [
    path("", cache_page(60*15)(views.IndexView.as_view()), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("create", views.create_question, name="create"),
]
