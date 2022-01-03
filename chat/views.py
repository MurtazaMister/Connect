from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import GlobalRoom, GlobalMessage, PrivateMessage, PrivateRoom

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
    privaterooms = request.user.privateroom_set.all()
    return render(request,'connect.html',{
        'globalrooms':globalrooms,
        'privaterooms':privaterooms,
    })

def globalRoom(request,room):
    return render(request,'room.html',{
        'type':'Global',
        'roomname':room,
    })

def privateRoom(request,room):
    return render(request,'room.html',{
        'type':'Private',
        'roomname':room,
    })

def send(request, type):
    user = User.objects.get(username=request.POST['user'])
    value = request.POST['value']
    if type=="Global":
        room = GlobalRoom.objects.get(name=request.POST['room'])
        msg = GlobalMessage.objects.create(value=value,room=room,user=user,user_name=user.username+" ("+user.first_name+" "+user.last_name+")")
    elif type=="Private":
        room = PrivateRoom.objects.get(name=request.POST['room'])
        msg = PrivateMessage.objects.create(value=value,room=room,user=user,user_name=user.username+" ("+user.first_name+" "+user.last_name+")")
    msg.save()
    return HttpResponse('success')

def getMessages(request,type,room):
    if type=='Global':
        roomm = GlobalRoom.objects.get(name=room)
        messages = GlobalMessage.objects.filter(room=roomm)
    elif type=="Private":
        roomm = PrivateRoom.objects.get(name=room)
        messages = PrivateMessage.objects.filter(room=roomm)
    return JsonResponse({"messages":list(messages.values())})

def create(request, type):
    if type=="global":
        new_room = GlobalRoom.objects.create(name=request.POST["groom"])
        new_room.save()
        return redirect('/connect/global/'+new_room.name)
    elif type=="private":
        new_room = PrivateRoom.objects.create(name=request.POST["proom"])
        new_room.save()
        new_room.users.add(request.user)
        new_room.save()
        return redirect('/connect/private/'+new_room.name)

def search(request):
    q = request.GET.get('query')
    payload = set()
    if q:
        users = User.objects.filter(username__icontains=q)
        for user in users:
            payload.add(user.username + " (" + user.first_name + " " + user.last_name + ")")
        users = User.objects.filter(first_name__icontains=q)
        for user in users:
            payload.add(user.username + " (" + user.first_name + " " + user.last_name + ")")
        users = User.objects.filter(last_name__icontains = q)
        for user in users:
            payload.add(user.username + " (" + user.first_name + " " + user.last_name + ")")
        payload.add('admin (Admin )')
        payload.add(request.user.username + " (" + request.user.first_name + " " + request.user.last_name + ")")
        payload.remove('admin (Admin )')
        payload.remove(request.user.username + " (" + request.user.first_name + " " + request.user.last_name + ")")
    return JsonResponse({'data':list(payload)})