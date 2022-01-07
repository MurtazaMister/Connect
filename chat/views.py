from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from chat.models import GlobalRoom, GlobalMessage, PrivateMessage, PrivateRoom
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'index.html')

def loginPage(request):
    if request.user.is_anonymous:
        return render(request,'login.html')
    else:
        return redirect('/')

def validate(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request, User.objects.filter(username="annar").password)
            return redirect('/login')
    return redirect('/')

def logoutPage(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('/')

def signup(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            username = (request.POST['username']).strip()
            password = (request.POST['password']).strip()
            first_name = (request.POST['first_name']).strip()
            last_name = (request.POST['last_name']).strip()

            if len(username)>0 and len(password)>0 and len(first_name)>0 and len(last_name)>0:
                if len(username.split()) == 1:
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(username=username,email=None,password=password,first_name=first_name,last_name=last_name)
                        user.save()
                        return redirect("/login")
                    else:
                        messages.error(request, 'Username is taken.')
                        return redirect('/signup')
                else:
                    messages.error(request, 'INVALID USERNAME!')
                    return redirect('/signup')
            else:
                messages.error(request, 'Fill up all the fields.')
                return redirect('/signup')
        else:
            return render(request,"signup.html")
    else:
        return redirect('/')
    
def connect(request):
    if not request.user.is_anonymous:
        globalrooms = GlobalRoom.objects.all()
        privaterooms = request.user.privateroom_set.filter(type="GROUP")
        indivrooms = request.user.privateroom_set.filter(type="INDIV")
        return render(request,'connect.html',{
            'globalrooms':globalrooms,
            'privaterooms':privaterooms,
            'indivrooms':indivrooms,
        })
    else:
        return redirect('/login')

def globalRoom(request,room):
    if not request.user.is_anonymous:
        return render(request,'room.html',{
            'type':'Global',
            'roomname':room,
        })
    else:
        return redirect('/login')

def privateRoom(request,room):
    if not request.user.is_anonymous:
        if PrivateRoom.objects.filter(name=room).exists():
            if PrivateRoom.objects.get(name=room).users.filter(username=request.user.username).exists():
                pvtRoom = PrivateRoom.objects.get(name=room)
                pvtUsers = ""
                for k in pvtRoom.users.all():
                    pvtUsers = pvtUsers + "," + k.username
                return render(request,'room.html',{
                    'type':'Private',
                    'roomname':room,
                    'pvtRoom':pvtRoom,
                    'pvtUsers':pvtUsers,
                })
        return redirect('/connect')
    else:
        return redirect('/login')

def send(request, type):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            user = User.objects.get(username=request.POST['user'])
            value = request.POST['value']
            if type=="Global":
                room = GlobalRoom.objects.get(name=request.POST['room'])
                msg = GlobalMessage.objects.create(value=value,room=room,user=user,user_name=user.username+" ("+user.first_name+" "+user.last_name+")")
                msg.save()
                return HttpResponse('Success')
            elif PrivateRoom.objects.filter(name=request.POST['room']).exists() and PrivateRoom.objects.get(name=request.POST['room']).users.filter(username=request.user.username).exists() and type=="Private":
                room = PrivateRoom.objects.get(name=request.POST['room'])
                msg = PrivateMessage.objects.create(value=value,room=room,user=user,user_name=user.username+" ("+user.first_name+" "+user.last_name+")")
                msg.save()
                return HttpResponse('Success')
            else:
                return HttpResponse('Unauthorized request!')
        else:
            return redirect('/')
    else:
        return redirect('/login')

def getMessages(request,type,room):
    if not request.user.is_anonymous:
        if type=='Global':
            roomm = GlobalRoom.objects.get(name=room)
            messages = GlobalMessage.objects.filter(room=roomm)
            return JsonResponse({"messages":list(messages.values())})
        elif PrivateRoom.objects.filter(name=room).exists() and PrivateRoom.objects.get(name=room).users.filter(username=request.user.username).exists() and type=="Private":
            roomm = PrivateRoom.objects.get(name=room)
            messages = PrivateMessage.objects.filter(room=roomm)
            return JsonResponse({"messages":list(messages.values())})
        else:
            return HttpResponse("Unauthorized request!")
    else:
        return redirect('/login')

def create(request, type):
    if not request.user.is_anonymous:
        if type=="global":
            if not GlobalRoom.objects.filter(name=request.POST["groom"]).exists():
                new_room = GlobalRoom.objects.create(name=request.POST["groom"])
                new_room.save()
                return redirect('/connect/global/'+new_room.name)
            else:
                return redirect('/connect/global/'+request.POST["groom"])
        elif type=="private":
            if not PrivateRoom.objects.filter(name=request.POST["proom"]).exists():
                new_room = PrivateRoom.objects.create(name=request.POST["proom"],admin=request.user)
                new_room.save()
                new_room.users.add(request.user)
                new_room.save()
                return redirect('/connect/private/'+new_room.name)
            else:
                messages.error(request, 'Roomname '+request.POST["proom"]+' is already taken.')
                return redirect('/connect')
    else:
        return redirect('/login')

def search(request):
    if not request.user.is_anonymous:
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
        else:
            u = User.objects.all()
            payMax = len(u)
            for i in range(payMax):
                payload.add(u[i].username + " (" + u[i].first_name + " " + u[i].last_name + ")")

        payload.add('admin (Admin )')
        payload.remove('admin (Admin )')
        if request.user.username != "admin":
            payload.add(request.user.username + " (" + request.user.first_name + " " + request.user.last_name + ")")
            payload.remove(request.user.username + " (" + request.user.first_name + " " + request.user.last_name + ")")
        return JsonResponse({'data':list(payload)})
    else:
        return redirect('/login')

def addmembers(request,room):
    if not request.user.is_anonymous:
        if request.user.privateroom_set.all().filter(name=room).exists():
            z = request.POST['value']
            z = z[1:-1]
            if z:
                z = z.split(',')
                for k in z:
                    k = k[1:k.find('(')-1]
                    user = User.objects.get(username=k)
                    pvt = PrivateRoom.objects.get(name=room)
                    pvt.users.add(user)
            pvtRoom = PrivateRoom.objects.get(name=room)
            pvtUsers = ""
            for k in pvtRoom.users.all():
                pvtUsers = pvtUsers + "," + k.username
            return HttpResponse(pvtUsers)
        else:
            return HttpResponse("Invalid request!")
    else:
        return redirect('/login')

def removemembers(request,room):
    if not request.user.is_anonymous:
        if PrivateRoom.objects.filter(name=room).exists() and request.user.username == PrivateRoom.objects.get(name=room).admin.username:
            z = request.POST['value']
            z = z[1:-1]
            if z:
                z = z.split(',')
                for k in z:
                    pvt = PrivateRoom.objects.get(name=room)
                    user = User.objects.get(username=k[1:-1])
                    pvt.users.remove(user.id)
            pvtRoom = PrivateRoom.objects.get(name=room)
            pvtUsers = ""
            for k in pvtRoom.users.all():
                pvtUsers = pvtUsers + "," + k.username
            return HttpResponse(pvtUsers)
    else:
        return redirect('/login')

def privateIndivRoom(request, indiv):
    if not request.user.is_anonymous:
        if request.user.username == indiv.split('_')[0] or request.user.username == indiv.split('_')[1]:
            if PrivateRoom.objects.filter(name=indiv).exists():
                pvtRoom = PrivateRoom.objects.get(name=indiv)
                return render(request,'room.html',{
                'type':'Private',
                'roomname':indiv,
                'pvtRoom':pvtRoom,
                })
            else:
                name = ''
                if indiv.split('_')[0]<indiv.split('_')[1]:
                    name = indiv.split('_')[0]+'_'+indiv.split('_')[1]
                else:
                    name = indiv.split('_')[1]+'_'+indiv.split('_')[0]
                newRoom = PrivateRoom.objects.create(name=name,type="INDIV")
                newRoom.users.add(User.objects.get(username=indiv.split('_')[0]),User.objects.get(username=indiv.split('_')[1]))
                newRoom.save()
                return render(request,'room.html',{
                    'type':'Private',
                    'roomname':indiv,
                    'pvtRoom':newRoom,
                })
        else:
            return redirect('/connect')
    else:
        return redirect('/login')

def leavegroup(request, room):
    if not request.user.is_anonymous:
        if PrivateRoom.objects.filter(name=room).exists() and PrivateRoom.objects.get(name=room).users.filter(username=request.user.username).exists():
            PrivateRoom.objects.get(name=room).users.remove(request.user)
            if PrivateRoom.objects.get(name=room).admin.username == request.user.username:
                if len(PrivateRoom.objects.get(name=room).users.all()) == 0:
                    PrivateRoom.objects.get(name=room).delete()
                else:
                    a = PrivateRoom.objects.get(name=room)
                    a.admin = a.users.all()[0]
                    a.save()
            return redirect('/connect')
        else:
            return HttpResponse("Invalid request!")
    else:
        return redirect('/login')

def terminategroup(request, room):
    if not request.user.is_anonymous:
        if PrivateRoom.objects.filter(name=room).exists():
            if PrivateRoom.objects.get(name=room).admin.username == request.user.username:
                PrivateRoom.objects.get(name=room).delete()
            else:
                return HttpResponse("Invalid request!")
        return redirect('/connect')
    else:
        return redirect('/login')