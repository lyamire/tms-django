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
router.register('register', views.RegistrationViewSet)
router.register('current_user/orders', views.OrdersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote/', views.choice_vote),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/update/', views.UpdateCartView.as_view(), name='update_cart'),
    path('complete_order/', views.CompleteOrderView.as_view(), name='complete_order'),
    path('current_user/', views.CurrentUserViewSet.as_view({
        'get': 'retrieve',
        'post': 'update',
    })),
    path('repeat_order/', views.RepeatOrderView.as_view(), name='repeat_order')
]
