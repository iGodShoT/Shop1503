from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import *
from shop.models import *
from django.contrib import messages
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    return render(request, 'queries/index.html')

class ProductList(ListView):
    model = Product
    template_name = 'queries/query_all.html'
class ProductDetail(DetailView):
    model = Product
    template_name = 'queries/detail.html'
    @method_decorator(permission_required('shop.view_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ProductCreate(CreateView):
    model = Product
    template_name = 'queries/product_form.html'
    form_class = ProductForm
    extra_context = {
        'action': 'Создание',
        'action_button': 'Создать'
    }
    @method_decorator(permission_required('shop.add_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class ProductUpdate(UpdateView):
    model = Product
    template_name = 'queries/product_form.html'
    form_class = ProductForm
    extra_context = {
        'action': 'Изменение',
        'action_button': 'Изменить'
    }
    @method_decorator(permission_required('shop.change_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class ProductDelete(DeleteView):
    model = Product
    template_name = 'queries/product_confirm_delete.html'
    success_url = reverse_lazy('catalog_products_page')

    @method_decorator(permission_required('shop.delete_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

def get_suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        'list': suppliers # list - ключ, который будет использоваться как переменная в HTML
    }
    return render(request, 'supplier/catalog.html', context)

def detail_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier/detail.html', {'obj': supplier})
def create_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = Supplier(**form.cleaned_data)
            supplier.save()
            messages.success(request, 'Поставщик успешно добавлен!')
            return redirect('suppliers_page')
        messages.error(request, 'Неверно заполнены поля')
    form = SupplierForm()
    context = {
        'form': form
    }
    return render(request, 'supplier/create_supplier.html', context)

def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home_page')
        messages.error(request, 'Что-то пошло не так')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print('is_anon: ', request.user.is_anonymous)
            print('is_auth: ', request.user.is_authenticated)
            print(user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('home_page')
        messages.error(request, 'Что-то пошло не так')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('user_login_page')


def anon(request):
    print('is_active:', request.user.is_active)
    print('is_anon:', request.user.is_anonymous)
    print('is_auth:', request.user.is_authenticated)
    print('is_staff:', request.user.is_staff)
    print('is_superuser:', request.user.is_superuser)

    # При проверке доступ указывается следующим образом:
    # <приложение>.<право>_<модель>
    # Права: add, change, view, delete

    print('Может ли добавлять товар?', request.user.has_perm('shop.add_product'))
    print('Может ли добавлять и изменять товар?', request.user.has_perms(['shop.add_product', 'shop.change_product']))


    return render(request, 'test/anon.html')

@login_required()
def auth(request):
    return render(request, 'test/auth.html')

@permission_required('shop.add_product')
def is_able_to_add_product(request):
    return render(request, 'test/can_add_product.html')

@permission_required(['shop.add_product', 'shop.change_product'])
def is_able_to_add_and_change_product(request):
    return render(request, 'test/can_add_change_product.html')

@permission_required('shop.change_delivery_type')
def is_able_to_change_delivery_type(request):
    return render(request, 'test/can_change_delivery_type.html')

@login_required()
def buy(request):

    return render(request, 'queries/purchase.html')

class CategoryList(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    extra_context = {
        'title': 'Список категорий'
    }
    allow_empty = True
    # paginate_by = 1
    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список категорий в get_context_data()'
        return context

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category/category_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    extra_context = {
        'action': 'Создать'
    }
    template_name = 'category/category_form.html'
    # success_url = reverse_lazy('category_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    extra_context = {
        'action': 'Изменить'
    }
    template_name = 'category/category_form.html'

    @method_decorator(permission_required('shop.change_category'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    @method_decorator(permission_required('shop.delete_category'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


from django.http import JsonResponse
from shop.serializers import *

# status - пакет со всеми статусными кодами для настройки отчета
from rest_framework import status

from rest_framework.response import Response

# api_view - декоратор, внутри него можно описывать доступные нам методы
from rest_framework.decorators import api_view

# viewsets - generic класс, c CRUD операциями
from rest_framework import viewsets

def test_json(request):
    return JsonResponse({
        'message': 'Данные в виде JSON',
        'api_test':  reverse_lazy('api_test'),
        'order_api_list': reverse_lazy('api_order_list'),
        'order_api_detail': reverse_lazy('api_order_detail'),
    })


@api_view(['GET', 'POST'])
def order_api_list(request, format=None):
    # Проверка запроса
    if request.method == 'GET':

        # Получаем данные из БД
        order_list = Order.objects.all()

        # Преобразуем данные в словарь с помощью сериализатора
        # По умолчанию сериализатор работает с одним объектом, но если у нас
        # список объектов то стоит включить параметр many
        serializer = OrderSerializer(order_list, many=True)
        print(serializer.data)
        return Response({'orders': serializer.data})

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Сохранение
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def order_api_detail(request, pk, format=None):
    order_obj = get_object_or_404(Order, pk=pk)

    if order_obj == None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order_obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Данные успешно обновлены', 'order': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Удаление объекта
        order_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderList(ListView):
    model = Order
    template_name = 'order/order_list.html'

class OrderDetail(DetailView):
    model = Order
    template_name = 'order/order_detail.html'

    @method_decorator(permission_required('shop.view_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    extra_context = {
        'action': 'Создание',
        'action_button': 'Создать'
    }

    @method_decorator(permission_required('shop.add_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    extra_context = {
        'action': 'Изменение',
        'action_button': 'Изменить'
    }

    @method_decorator(permission_required('shop.change_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list_view')
    template_name = 'order/order_confirm_delete.html'

    @method_decorator(permission_required('shop.delete_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class SupplyList(ListView):
    model = Supply
    template_name = 'supply/supply_list.html'

    @method_decorator(permission_required('shop.view_supply'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer