from django.urls import path, include
from rest_framework import routers

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()

router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('articles', views.ArticleViewSet)
router.register('authors', views.AuthorViewSet)
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote/', views.choice_vote),
    path('accounts/register/', views.register),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
