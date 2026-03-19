from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from users import views as UserViews
from products import views as ProductViews

urlpatterns = [
    path('register/', UserViews.RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserViews.ProfileView.as_view()),

    path('products/', ProductViews.ProductListView.as_view()),
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view())
]