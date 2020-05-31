from rest_framework import viewsets, permissions, views, mixins, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from account.models import Account
from account.serializer import AccountSerializer
from account.views import send_confirmation
from . import serializers, models

# from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Entity, Category

class RegisterView(views.APIView):
    def post(self, request, format=None):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')

        if email is None or username is None or password is None or password2 is None:
            return Response({"error": 'There is empty fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({"error": 'Passwords have to match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Account.objects.create_user(email, username, password)
        except IntegrityError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        send_confirmation(user)
        serializer = AccountSerializer(instance=user)
        return Response(serializer.data)
    

class EntityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        # fnd_pk = self.request.fnd_pk
        entity_pk = self.kwargs['entity_pk']
        # print(a)
        return models.Category.objects.filter(entity__pk=entity_pk)
    
    # def list(self, request, fnd_pk):
    #     qt = Category.objects.all()
    #     serializer = self.get_serializer(qt, many=True)
    #     return Response(serializer.data)



class WaiterViewSet(viewsets.ModelViewSet):
    queryset = models.Waiter.objects.all()
    serializer_class = serializers.WaiterSerializer


class CashierViewSet(viewsets.ModelViewSet):
    queryset = models.Cashier.objects.all()
    serializer_class = serializers.CashierSerializer


class ChefViewSet(viewsets.ModelViewSet):
    queryset = models.Chef.objects.all()
    serializer_class = serializers.ChefSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def create(self, request, *args, **kwargs):
        request.data['customer'] = request.user
        request.data['entity'] = kwargs['entity_pk']
        
        return super().create(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer
    
    def get_queryset(self):
        entity_pk = self.kwargs['entity_pk']
        status = self.request.query_params.get('status')

        queryset = models.Order.objects.filter(entity__pk=entity_pk)

        if status is not None:
            queryset = queryset.filter(status=status)
        
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        # order_status = request.query_params.get('status')
        status = request.query_params.get('order_item_status')

        if status is not None:
            if status == 'NEW':
                status = ('NEW', 'COO')
            else:
                status = (status)


            new_data = []
            for order in data:
                items = order['orderitem_set']
                filtered = []
                order['orderitem_set'] = filtered

                for order_item in items:
                    if order_item['status'] in status:
                        filtered.append(order_item)
                if len(filtered) != 0:
                    order['orderitem_set'] = filtered
                    new_data.append(order)
                elif 'DEL' in status:
                    new_data.append(order)
            data = new_data

        return Response(data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MenuItemSerializer

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')

        queryset = self.get_queryset()
        if category:
            queryset = queryset.filter(category__pk=category)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialzier = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        entity_pk = self.kwargs['entity_pk']
        return models.MenuItem.objects.filter(entity__pk=entity_pk)

