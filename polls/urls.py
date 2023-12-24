from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("create", views.create_question, name="create"),
]
