from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


router = routers.DefaultRouter()

router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('articles', views.ArticleViewSet)
router.register('authors', views.AuthorViewSet)
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="OpenAPI Documentation",
      default_version='v1',
   )
)

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote/', views.choice_vote),
    path('accounts/register/', views.register),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
