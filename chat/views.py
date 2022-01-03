from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import GlobalRoom, GlobalMessage

# Create your views here.
def home(request):
    return render(request, 'index.html')

def loginPage(request):
    return render(request,'login.html')

def validate(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/login')

def logoutPage(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create_user(username=username,email=None,password=password,first_name=first_name,last_name=last_name)
        user.save()
        return redirect("/login")
    return render(request,"signup.html")

def connect(request):
    globalrooms = GlobalRoom.objects.all()
    return render(request,'connect.html',{
        'globalrooms':globalrooms,
    })

def globalRoom(request,room):
    return render(request,'room.html',{
        'type':'Global',
        'roomname':room,
    })

def send(request):
    user = User.objects.get(username=request.POST['user'])
    room = GlobalRoom.objects.get(name=request.POST['room'])
    value = request.POST['value']
    print(user,room,value)
    msg = GlobalMessage.objects.create(value=value,room=room,user=user,user_name=user.username+" ("+user.first_name+" "+user.last_name+")")
    msg.save()
    return HttpResponse('success')

def getMessages(request,room):
    roomm = GlobalRoom.objects.get(name=room)
    messages = GlobalMessage.objects.filter(room=roomm)
    return JsonResponse({"messages":list(messages.values())})

def create(request, type):
    if type=="global":
        new_room = GlobalRoom.objects.create(name=request.POST["groom"])
        new_room.save()
        return redirect('/connect/global/'+new_room.name)
