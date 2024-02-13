from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import *
from shop.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'queries/index.html')

def query_all(request):
    products = Product.objects.all()

    context = {
        'list': products # list - ключ, который будет использоваться как переменная в HTML
    }
    return render(request, 'queries/query_all.html', context)

def get_one_product(request,id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'queries/query_one.html', {'obj': product})


def detail_product(request,id):
    if request.method == "POST":
        messages.success(request, 'Успешная покупка')
        return redirect('catalog_products_page')
    product = get_object_or_404(Product, pk=id)
    return render(request, 'queries/detail.html', {'obj': product})

def create_product(request):
    category = get_object_or_404(Category, pk=1)
    parameter = get_object_or_404(Parameter, pk=1)
    product = Product()
    product.name = 'Яблоко'
    product.price = 60
    product.category = category

    product.save()
    return render(request, 'queries/message.html', context={'message': 'Товар добавлен!'})

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


from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

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

# View Generic
# ListView - Список объектов
# DetailView - Полная информация выбранного объекта
# UpdateView - Изменение
# CreateView - Создание
# DeleteView - Удаление

from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

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