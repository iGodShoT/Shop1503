from django.contrib import admin
from django.urls import path, include
from shop.views import *

urlpatterns = [
    path('', index, name='home_page'),
    path('products/', ProductList.as_view(), name='catalog_products_page'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/<int:pk>/detail/', ProductDetail.as_view(), name='detail_page'),
    path('product/create/', ProductCreate.as_view(), name='create_product'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='update_product'),
    path('getSuppliers/', get_suppliers, name='suppliers_page'),
    path('createSupplier', create_supplier, name='create_supplier_page'),
    path('supplier/<int:id>', detail_supplier, name='detail_supplier_page'),
    path('register/', user_registration, name='registration_page'),
    path('auth/', user_login, name='user_login_page'),
    path('logout/', user_logout, name='logout'),
    path('anon/', anon, name='anon'),
    path('auth/', auth, name='auth'),
    path('can_add/', is_able_to_add_product, name='add'),
    path('can_add_change/', is_able_to_add_and_change_product, name='add_change'),
    path('can_change_delivery_type', is_able_to_change_delivery_type, name='change_delivery_type'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/create', CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>/detail/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update/', CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category_delete'),
    path('api/', test_json, name='api_test'),
    path('api/orders/', order_api_list, name='api_order_list'),
    path('api/orders/<int:pk>/', order_api_detail, name='api_order_detail'),
    path('orders/', OrderList.as_view(), name='order_list_view'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order_detail_view'),
    path('orders/create/', OrderCreate.as_view(), name='order_create_view'),
    path('orders/<int:pk>/update/', OrderUpdate.as_view(), name='order_update_view'),
    path('orders/<int:pk>/delete/', OrderDelete.as_view(), name='order_delete_view'),
    path('supplies/', SupplyList.as_view(), name='supplies_list_view')

]
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/products', ProductViewSet, basename='product')
router.register(r'api/suppliers', SupplierViewSet, basename='supplier')
router.register(r'api/supplies', SupplyViewSet, basename='supplies')
urlpatterns += router.urls