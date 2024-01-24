from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
]