from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router object
router = DefaultRouter()

# Register your viewset with the router
router.register(r'todos', ToDoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    #path("login/", login, name="login1"),
    #path("login2/", Login.as_view(), name="login2"),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout')
    
    

]







