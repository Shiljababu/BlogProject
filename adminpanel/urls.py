
from django.urls import path
from .views import adminhome, user_list, blog_list, blog_view, reset_password,user_profile, user_list, admin_login, logout


urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('adminhome/', adminhome, name = 'adminhome'),
    path('user-list/', user_list, name='user_list'),
    path('blog-list/', blog_list, name='blog_list'),
    path('blog-view/<int:blog_id>/', blog_view, name='blog_view'),
    path('reset-password/', reset_password, name='reset_password1'),
    path('user-profile/<int:user_id>/', user_profile, name='user_profile'),
    path('user-detail/<int:user_id>/', user_list, name='user_detail'), 
    path('logout/', logout, name='logout'),
    
]

