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
    path('connect/private/indiv/<str:indiv>',views.privateIndivRoom,name="privateIndivRoom"),
    path('connect/private/<str:room>',views.privateRoom,name="privateRoom"),                 
    path('send/<str:type>',views.send,name="send"),                                          
    path('getMessages/<str:type>/<str:room>',views.getMessages,name="getMessages"),          
    path('create/<str:type>',views.create,name="create"),                                    
    path('search/',views.search,name="search"),                                              
    path('addmembers/<str:room>',views.addmembers,name="addmembers"),                        
    path('removemembers/<str:room>',views.removemembers,name="removemembers"),               
    path('connect/private/leavegroup/<str:room>',views.leavegroup,name="leaveGroup"),        
    path('connect/private/terminate/<str:room>',views.terminategroup,name="terminateGroup"), 
]