

from django.urls import path
# from django.contrib.auth.views import LogoutView
from .views import userhome, account_settings, upload_blog, edit_blog, view_blog,deactivate_account
from .views import  my_blogs, blog_list, reset, user_profile, edit_profile, logout, delete_blog

urlpatterns = [
    path('', userhome, name='userhome'),
    path('account-settings/', account_settings, name = 'account_settings'),
    path('upload_blog/', upload_blog, name = 'upload_blog'),
    path('edit_blog/<int:blog_id>', edit_blog, name = 'edit_blog'),
    path('view_blog/<int:blog_id>/', view_blog, name = 'view_blog'),
    path('my_blogs/', my_blogs, name = 'my_blogs'),
    path('delete_blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('user_blog_list/', blog_list, name = 'user_blog_list'),
    path('reset_password/', reset, name = 'reset_password'),
    path('user_profile/', user_profile, name = 'user_profile'),
    path('deactivate_account/', deactivate_account, name='deactivate_account'),
    path('edit_profile/', edit_profile, name = 'edit_profile'),
    path('logout/', logout, name='logout'),
    
    
]


