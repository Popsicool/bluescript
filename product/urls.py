from django.urls import path
from product.views import *

urlpatterns = [
    path("create_product", create_product, name="create_product"),
    path("delete_product/<str:id>", delete_product, name="delete_product"),
    path("edit_product/<str:id>", edit_product, name="edit_product"),
    path("shop_product/<str:id>", shop_product, name="shop_product"),
]
