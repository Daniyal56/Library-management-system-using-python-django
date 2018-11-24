from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import render
from .forms import UserForm
from .models import Book, Movies, Memberships
from django.db.models import Q
from django.http import HttpResponse
from datetime import date
from django.contrib.auth import get_user_model

# Create your views here.

class QQ:
    def __xor__(self, other):
        not_self = self.clone()
        not_other = other.clone()
        not_self.negate()
        not_other.negate()

        x = self & not_other
        y = not_self & other

        return x | y

Q.__bases__ += (QQ, )

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

    return render(request, 'management/register.html', context= {"form": form})


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


def mlmovies(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/repo.html', context={'user': request.user, 'mlmovies': Movies.objects.all().order_by('serial')} )


def mlbooks(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/repo.html', context={'user': request.user, 'mlbooks': Book.objects.all().order_by('serial')} )


def mlmember(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')

    else:
        return render(request, 'management/repo.html', context={'user': request.user, 'mlmember': Memberships.objects.all().order_by('id')} )


def actissues(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        actissues={'serial':[],'name':[],'id':[],'idate':[],'rdate':[]}

        for i in Memberships.objects.filter(Q(if_having_book='') ^ Q(if_having_movie='')):
            actissues['id'].append(i.id)
            actissues['idate'].append(i.if_issue_date)
            actissues['rdate'].append(i.if_return_date)
            if i.if_having_book=='':
                actissues['serial'].append(i.if_having_movie)
                actissues['name'].append(Movies.objects.filter(serial=i.if_having_movie)[0].name)
            else:
                actissues['serial'].append(i.if_having_book)
                actissues['name'].append(Book.objects.filter(serial=i.if_having_book)[0].name)

        matrix=[]
        transposed = []

        for k in actissues:
            matrix.append(actissues[k])

        for i in range(len(actissues['serial'])):
            transposed_row=[]

            for row in matrix:
                transposed_row.append(row[i])
            transposed.append(transposed_row)

        context = {'user': request.user, 'actissues': len(actissues.keys()), 'actissues_data': sum(transposed, [])}

        return render(request, 'management/repo.html',context)


def overdueslist(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        overdueslist={'serial':[],'name':[],'id':[],'idate':[],'rdate':[],'fine':[]}

        for i in Memberships.objects.filter(Q(if_having_book='') ^ Q(if_having_movie='')):
            overdueslist['id'].append(i.id)
            overdueslist['idate'].append(i.if_issue_date)
            overdueslist['rdate'].append(i.if_return_date)
            if i.if_having_book=='':
                overdueslist['serial'].append(i.if_having_movie)
                overdueslist['name'].append(Movies.objects.filter(serial=i.if_having_movie)[0].name)
            else:
                overdueslist['serial'].append(i.if_having_book)
                overdueslist['name'].append(Book.objects.filter(serial=i.if_having_book)[0].name)

            if (i.if_return_date - i.if_issue_date).days - 15 > 0 :
                overdueslist['fine'].append(((i.if_return_date - i.if_issue_date).days - 15)*10)
            else:
                overdueslist['fine'].append('Nil')
        matrix=[]
        transposed = []

        for k in overdueslist:
            matrix.append(overdueslist[k])

        for i in range(len(overdueslist['serial'])):
            transposed_row=[]

            for row in matrix:
                transposed_row.append(row[i])
            transposed.append(transposed_row)
        context = {'user': request.user, 'overdueslist': len(overdueslist.keys()), 'overdueslist_data': sum(transposed, [])}

        return render(request, 'management/repo.html',context)


def addmember(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    elif not request.user.is_superuser:
        return HttpResponse('The user is not superuser')
    elif request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        contact = request.POST['contact']
        address = request.POST['address']
        aadhar = request.POST['aadhar']
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        membership = request.POST['membership']
        name=fname+" "+lname

        try:

            row=Memberships(name=name,contact=contact,address=address,aadhar=aadhar,start_date=sdate,end_date=edate,status='inactive',fine='0',if_having_book='',if_having_movie='',if_issue_date='1990-01-01',if_return_date='1990-01-01')
            row.save()
            return render(request, 'management/main.html',context={'adduser':fname})
        except Exception as error_message:
            return render(request, 'management/main.html', context={'error_message': error_message})
    else:
        return render(request, 'management/main.html',context={'add_user':'add_user'})


def addbook(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    elif not request.user.is_superuser:
        return HttpResponse('The user is not superuser')
    elif request.method == 'POST':

        choice = request.POST['choice']
        bname = request.POST['bname']
        date = request.POST['date']
        quanity = request.POST['quanity']
        cat = (request.POST['cat']).upper()
        author= request.POST['author']
        cost = request.POST['cost']

        try:
            category={'FCM':'FICTION','FCB':'FICTION','SCM':'SCIENCE','SCB':'SCIENCE','ECM':'ECONOMICS','ECB':'ECONOMICS','PDM':'PERSONALITY DEVELOPMENT','PDB':'PERSONALITY DEVELOPMENT','CHM':'CHILDREN','CHB':'CHILDREN'}

            if int(choice)==0:
                serial = cat + format(len(Book.objects.all()), "06")
                cat = category[cat]
                a=Book(serial=serial,name=bname,author=author,category=cat,status='available',cost=cost,procurement=date,quantity=quanity)
                a.save()
            else:
                serial = cat + format(len(Movies.objects.all()), "06")
                cat = category[cat]
                a = Movies(serial=serial,name=bname,author=author,category=cat,status='available',cost=cost,procurement=date,quantity=quanity)
                a.save()

            return render(request, 'management/main.html',context={'addbook':bname})
        except Exception as error_message:
            return render(request, 'management/main.html', context={'error_message': error_message})
    else:
        return render(request, 'management/main.html',context={'add_book':'add_book'})


def addsuperuser(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    elif not request.user.is_superuser:
        return HttpResponse('Woah! only superusers Allowed!!!')
    elif request.method == 'POST':
        sname = request.POST['name']
        spassword = request.POST['pass']
        semail = request.POST['email']

        try:
            User = get_user_model()
            User.objects.create_superuser(sname, semail, spassword)

            return render(request, 'management/main.html',context={'addsuperuser':sname})
        except Exception as error_message:
            return render(request, 'management/main.html', context={'error_message': error_message})
    else:
        return render(request, 'management/main.html',context={'add_superuser':'add_superuser'})

