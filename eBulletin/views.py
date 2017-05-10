from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User 
from .models import Bulletin, Message, Comment, Profile
from .forms import UserRegForm
from django.contrib import messages

#from models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# Create your views here.
def userLogin(request):
    if request.user.is_authenticated():
        return redirect('userindex')
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        login_user = authenticate(username=user_name, password=pass_word)
        if login_user is not None:
            login(request, login_user)
            return redirect('userindex')
        else:
            return render(request, "login.html" )

    elif request.method == "GET":
        return render(request, "login.html", {}) 

def userLogout(request):
    logout(request)
    return render(request, "login.html", {})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        return render(request, "login.html", {})
    else:
        return render(request, "login.html")



# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             profile = Profile.objects.create(user=new_user)
#             # messages.success(request, 'Register completed.')
#             return render(request, "login.html", {})
#     else:
#         user_form = UserRegForm()
#     return render(request, 'register.html',
#                   {'user_form': user_form})


def userindex(request):
    if not request.user.is_authenticated():  
        return redirect('userlogin')
    login_user=request.user
    created_bulletins=Bulletin.objects.filter(creator=login_user)
    followed_bulletins=Bulletin.objects.filter(follower=login_user)    
    
    return render(request,'base.html',{'created_bulletins':created_bulletins,'followed_bulletins':followed_bulletins,
                    'login_user':login_user})




#message_list with comment_list
def message_list(request, bulletin_id):
    if not request.user.is_authenticated():  
        return redirect('userlogin')
    login_user = request.user
    created_bulletins=Bulletin.objects.filter(creator=login_user)
    followed_bulletins=Bulletin.objects.filter(follower=login_user)
    flag = 0
    bulletin=Bulletin.objects.get(pk=bulletin_id)
    messages=Message.objects.filter(bulletin=bulletin)
    for fo in bulletin.follower.all():
        if fo == login_user:
            flag = 1
    message_comments=[]
    for message in messages:
        comments=Comment.objects.filter(message=message)
        message_comments.append((message.id,comments))
    message_comments=dict(message_comments)

    return render(request,'message_list.html',{'created_bulletins':created_bulletins,'followed_bulletins':followed_bulletins,
                    'login_user':login_user,'messages':messages,'bulletin':bulletin,'message_comments':message_comments, 'flag': flag})

def message_detail(request, message_id):
    if not request.user.is_authenticated():  
        return redirect('userlogin')
    login_user = request.user
    created_bulletins=Bulletin.objects.filter(creator=login_user)
    followed_bulletins=Bulletin.objects.filter(follower=login_user)

    message=Message.objects.get(pk=message_id)
    return render(request,'message_detail.html',{'created_bulletins':created_bulletins,'followed_bulletins':followed_bulletins,
                    'login_user':login_user,'message':message})

def create_bulletin(request):
    if not request.user.is_authenticated():
        return redirect('userlogin')
    if request.method == 'POST':
        bulletin_name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        creator = request.user
        bulletin = Bulletin.objects.create(creator=creator, name=bulletin_name, description=description)
        bulletin.save()
        return redirect('userindex')
    else:
        login_user = request.user
        created_bulletins = Bulletin.objects.filter(creator=login_user)
        followed_bulletins = Bulletin.objects.filter(follower=login_user)
        return render(request, 'create_bulletin.html', {'created_bulletins': created_bulletins, 'followed_bulletins': followed_bulletins})

def search_bulletin(request):
    if request.method == 'POST':
        keyword = request.POST.get("keyword", "")
        bulletin_search_result = Bulletin.objects.filter(name__contains=keyword)
        return render(request, "result.html", {'result': bulletin_search_result})


def del_bulletin(request, bulletin_id):
    Bulletin.objects.get(pk=bulletin_id).delete()
    return redirect('userindex')

def follow_bulletin(request, bulletin_id):
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    bulletin.follower.add(request.user)
    bulletin.save()
    return redirect('userindex')

def post_message(request, bulletin_id):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        bulletin = Bulletin.objects.get(pk=bulletin_id)
        publisher = request.user
        message = Message.objects.create(title=title, bulletin=bulletin, message_content=content, publisher=publisher)
        message.save()
        return redirect('userindex')