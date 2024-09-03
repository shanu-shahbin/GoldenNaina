from django.urls import path, include
from . import views
from .views import CategoryDetailView

urlpatterns = [
  
  # products paths
    
  path('', views.Products, name='Products'),
  path('product_list', views.ProductList, name='ProductList'),
  path('product/<int:pk>/', views.Product_Detail, name="product_detail"),

  # navbar categories paths
  
  path('women/', views.womens, name='women_products'),
  path('men/', views.mens, name='men_products'),
  path('watches/', views.watches, name='watch_products'),
  path('accessories/', views.accessories, name='accessories_products'),
  path('Beauty_products/', views.Beauty, name='Beauty_products'),

  # product review paths

  path('product_list/tag/<slug:tag_slug>/', views.tag_list, name='tags'),
  path('product_detail/<pk>/reviews', views.reviews, name="reviews"),
  path('ajax-add-review/<int:pk>/', views.ajax_add_review, name="ajax_add_review"),

  # search paths

  path("search/", views.search, name="search"),
  

  # wishlist paths

  path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
  path('wishlist/', views.wishlist_view, name='wishlist_view'),
  path('remove-from-wishlist/', views.remove_from_wishlist, name='remove-from-wishlist'),

  # category paths not in navbar and other all

  path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
  path('size-chart/', views.size_chart, name='size-chart'),

  
   
]
