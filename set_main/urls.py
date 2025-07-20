
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'set_main'

router = DefaultRouter()
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'routes', views.RouteViewSet, basename='route')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'orders', views.OrderViewSet, basename='order')

schema_view = get_schema_view(
    openapi.Info(
        title="Taxi Bot API",
        default_version='v1',
        description="Taxi bot uchun ochiq API endpointlar",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/orders/stats/', views.OrderStatsView.as_view(), name='order_stats'),
    path('api/users/stats/', views.UserStatsView.as_view(), name='user_stats'),
    path('api/stats/', views.api_stats, name='api_stats'),
    # Swagger and Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
