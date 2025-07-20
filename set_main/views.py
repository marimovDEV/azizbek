from django.shortcuts import render
from django.http import JsonResponse
from .models import Order, User, Car, Route

# DRF imports
from rest_framework import viewsets, serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_id', 'full_name', 'phone']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'direction', 'date', 'phone', 'trip_type', 'car', 'address', 'comment', 'created_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'direction', 'date', 'phone', 'trip_type', 'car', 'address', 'comment']

# ViewSets
class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('user')
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

# Stats endpoints
class OrderStatsView(APIView):
    def get(self, request):
        count = Order.objects.count()
        return Response({'orders': count})

class UserStatsView(APIView):
    def get(self, request):
        count = User.objects.count()
        return Response({'users': count})

# Web views

def index(request):
    """Asosiy sahifa"""
    context = {
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'total_cars': Car.objects.count(),
        'total_routes': Route.objects.count(),
    }
    return render(request, 'set_main/index.html', context)

def api_stats(request):
    """API endpoint for statistics"""
    stats = {
        'orders': Order.objects.count(),
        'users': User.objects.count(),
        'cars': Car.objects.count(),
        'routes': Route.objects.count(),
    }
    return JsonResponse(stats)
