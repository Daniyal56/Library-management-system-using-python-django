from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import render
from .forms import UserForm
from .models import Book, Memberships, Movies


# Create your views here.
def index(request):
    if not request.user.is_authenticated():

        return render(request, 'management/login.html')
    # else directly enter the website
    else:

        return render(request, 'management/home.html', context={'user': request.user, "product_details":get_range()})


def transaction(request):

    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/trans.html', context={'user': request.user, "product_details": get_range()})

def maintenance(request):

    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/main.html', context={'user': request.user, "product_details": get_range()})

def report(request):

    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/repo.html', context={'user': request.user, "product_details": get_range()})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'management/login.html', context)


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request,'management/home.html', context={'user': user, "product_details":get_range()})
			else:
				return render(request, 'management/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'management/login.html', {'error_message': 'Invalid login'})
	return render(request, 'management/login.html')


	

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                return render(request,'management/home.html', context={'user': user,"product_details":1})
				
    context = {
        "form": form,
    }
    return render(request, 'management/register.html', context)

	


			
			
			
			
			
			
		
	
def get_range():
    cat = {'ECONIMICS': [], 'SCIENCE': [], 'CHILDREN': [], 'FICTION': [], 'PERSONALITY DEVELOPMENT': []}
    for k, v in cat.items():
        q = []
        q += Movies.objects.all()
        q += Book.objects.all()
        a = [a.serial for a in q]
        a.sort()
    for i in a:
        if i[0] == 'E':
            cat['ECONIMICS'].append(i)
        elif i[0] == 'S':
            cat['SCIENCE'].append(i)
        elif i[0] == 'C':
            cat['CHILDREN'].append(i)
        elif i[0] == 'F':
            cat['FICTION'].append(i)
        elif i[0] == 'P':
            cat['PERSONALITY DEVELOPMENT'].append(i)
        else:
            pass
    d={}
    for k,v in cat.items():
        if v==[]:
            d[k]=['NaN','NaN']
        else:
            d[k]=[cat[k][0],cat[k][-1]]
    return d