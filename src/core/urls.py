from django.urls import path
from .views import last_two_categories_with_products_view, category_products_view, review_view, product_view, email_view

app_name = 'core'

urlpatterns = [
    path('home-categories/', last_two_categories_with_products_view, name='home-categories'),
    path('category-products/<int:id>/', category_products_view, name='category-products'),
    path('reviews/', review_view, name='reviews'),
    path('products/', product_view, name='products'),
    path('email/', email_view, name='email'),
]
