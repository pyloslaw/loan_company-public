from django.urls import path
from . import views


urlpatterns = [
    path('rest_api/', views.restApi.as_view(), name='rest_api'),
    path('my_customers_list/<int:pk>/update/api_home/', views.api_home, name='api_home'),
    path('my_customers_list/<int:pk>/update/api_home_cbv', views.CustomerUpdateApiView.as_view(), name='api_home_cbv'),
    path('my_customers_list/<int:pk>/api_update', views.CustomerUpdateFetchApiView.as_view(), name='customer_update'),

]

