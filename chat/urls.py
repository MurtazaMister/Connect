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
    path('send',views.send,name="send"),
    path('getMessages/<str:room>',views.getMessages,name="getMessages"),
    path('create/<str:type>',views.create,name="create"),
]