from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'places', views.PlaceViewSet)
router.register(r'products', views.ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
