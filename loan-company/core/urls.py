from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name = 'core'

dev_settings = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG == True else []

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/sign_up/', views.RegisterUser.as_view(), name='sign_up'),
    path('accounts/user/<int:id>', views.UserProfileView.as_view(), name='user_profile'),
    path('accounts/user/<int:id>/edit', views.UserProfileEditView.as_view(), name='user_profile_edit'),
    path('accounts/user/<int:id>/edit/password_change', views.UserChangePassword.as_view(), name='user_password'),
    path('accounts/user/<int:id>/edit/password_change_done', views.UserChangePasswordDone.as_view(), name='user_password_done'),
    path('accounts/user_password_reset', views.UserResetPassword.as_view(), name='user_password_reset'),
    path('accounts/user_password_reset_form/<uidb64>/<token>/', views.UserResetPasswordForm.as_view(), name='user_password_reset_form'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_customer/add', views.CustomerCreateView.as_view(), name='add_customer'),
    path('custom_create', views.custom_customer, name='custom_create'),
    path('my_customers_list', views.CustomerListView.as_view(), name='customer_list'),
    path('my_customers_list/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    # path('my_customers_list/<int:pk>/update', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('my_customers_list/<int:id>/add_prod', views.AddNewProductView.as_view(), name='add_product'),
    path('test/', views.jsonTestView.as_view(), name='json_test'),

    
] + dev_settings