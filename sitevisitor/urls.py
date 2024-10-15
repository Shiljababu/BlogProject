from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import sitehome, site_login, register, forgot, forgot_phone, site_otp, reset, error_page

urlpatterns = [
    path('', sitehome, name = 'sitehome'),
    path('site_login/', site_login, name = 'site_login'),
    path('register/', register, name = 'register'),
    path('forgot_password/', forgot, name = 'forgot'),
    path('reset/', reset, name = 'reset'),
    path('forgot_phone/', forgot_phone, name = 'forgot_phone'),
    path('site_otp/', site_otp, name = 'site_otp'),
    path('404/', error_page)
]   
