from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    # Rota de Login e Logout
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('singup/', SingUpView.as_view(), name='singup'),
    
    path('', Index.as_view(), name='index'),
    path('add_local/', AddLocal.as_view(), name='add_local'),
    path('categorias/', Categorias.as_view(), name='categorias'),
    path('favoritos/', Favoritos.as_view(), name='favoritos'),
    path('favoritar/<int:ponto_id>/', FavoritarPonto.as_view(), name='favoritar-ponto'),
]