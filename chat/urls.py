from django.urls.conf import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.loginPage,name="login"),
    path('validate',views.validate,name="validate"),
    path('logout',views.logoutPage,name="logout"),
    path('signup',views.signup,name="signup"),
    path('connect',views.connect,name="connect"),
    path('connect/global/<str:room>',views.globalRoom,name="globalRoom"),
    path('connect/private/<str:room>',views.privateRoom,name="privateRoom"),
    path('send/<str:type>',views.send,name="send"),
    path('getMessages/<str:type>/<str:room>',views.getMessages,name="getMessages"),
    path('create/<str:type>',views.create,name="create"),
    path('search/',views.search,name="search"),
]