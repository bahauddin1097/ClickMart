from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from users import views as UserViews
from products import views as ProductViews
from cart import views as CartViews
from orders import views as OrderViews

urlpatterns = [
    path('register/', UserViews.RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserViews.ProfileView.as_view()),

    path('products/', ProductViews.ProductListView.as_view()),
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view()),

    path('cart/', CartViews.CartView.as_view()),
    path('cart/add/', CartViews.AddToCartView.as_view()),
    path('cart/items/<int:pk>/', CartViews.ManageCartItemView.as_view()),

    path('orders/place/', OrderViews.PlaceOrderView.as_view()),
    path('orders/', OrderViews.MyOrderView.as_view()),
    path('orders/<int:pk>/', OrderViews.OrderDetailView.as_view())
]