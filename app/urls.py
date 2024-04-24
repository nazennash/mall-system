from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    # path('cart/<int:cart_item_id>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:id>/', views.order_detail, name='order_detail'),
    path('products/<int:product_id>/add_feedback/', views.add_feedback, name='add_feedback'),
    path('forum/', views.forum, name='forum'),
    path('forum/<int:pk>/', views.forum_room, name='forum_room'), 
    path('forum/add_post/', views.add_forum_post, name='add_forum_post'),
    path('forum/<int:post_id>/add_comment/', views.add_forum_comment, name='add_forum_comment'),
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('products/<int:product_id>/add_feedback/', views.add_feedback, name='add_feedback'),
    path('advertisement/create/', views.create_advertisement, name='create_advertisement'),
    path('advertisements/', views.advertisement_list, name='advertisement_list'),
]
