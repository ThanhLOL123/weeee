
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('blog/',views.blog, name='blog'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('contact/', views.contact,name='contact'),
    path('shop/',views.shop,name='shop'),
    path('detail',views.detail,name='detail'),
    path('index',views.index,name='index'),
    path('manage_cart/',views.manage_cart,name='manage_cart'),
   path('logout/', views.logoutPage, name = 'logout'),
   path('search/', views.search, name = 'search'),
   path('buy/',views.processOrder, name ='buy'),
    path('category/',views.category, name ='category'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('category/<slug:slug>/', views.category, name='category-detail'),
    path('community',views.community,name='community'),
    path('search1', views.search1, name= 'search1'),
    path('shop_cart',views.shop_cart,name ='shop_cart'),
    path('check_out',views.shop_checkout,name='check_out'),
    path('addCart',views.addCart,name='addCart')
    
    
]
