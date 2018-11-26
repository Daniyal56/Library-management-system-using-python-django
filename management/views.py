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
import datetime
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
        if not request.user.is_superuser:
            return HttpResponse('Woah! only superusers Allowed!!!')

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
        return HttpResponse('Woah! only superusers Allowed!!!')
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
        return HttpResponse('Woah! only superusers Allowed!!!')
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













def payfine(request):

    if not request.user.is_authenticated():
        return render(request, 'management/login.html')

    elif request.method == 'POST':



            radio = request.POST['radio']
            member = request.POST['member']
            serial = request.POST['serial'].upper()
            radio2 = request.POST['radio2']
            rdate = request.POST['date']
            try:

                if radio =="0":
                    o=Memberships.objects.get(id=member)
                    keep_id=member
                    if radio2 == "3":
                        #current date
                        days_diff=abs((datetime.date.today() - (o.if_issue_date+datetime.timedelta(days=15))).days)


                    else:
                        #date
                        ry, rm, rd = rdate.split("-")
                        days_diff=abs((datetime.date(ry, rm, rd)- (o.if_issue_date+datetime.timedelta(days=15))).days)






                elif radio == '1':
                    #serial
                    for i in Memberships.objects.filter(Q(if_having_book='') ^ Q(if_having_movie='')):
                        if i.if_having_book == serial:
                            if radio2 == "3":
                                keep_id=i.id
                                days_diff = abs((datetime.date.today() - (i.if_issue_date+datetime.timedelta(days=15))).days)
                            else:
                                keep_id = i.id
                                ry, rm, rd = rdate.split("-")
                                days_diff = abs((datetime.date(ry, rm, rd) - (i.if_issue_date+datetime.timedelta(days=15))).days)
                        elif i.if_having_movie == serial:
                            if radio2 == "3":
                                keep_id = i.id
                                days_diff = abs((datetime.date.today() - (i.if_issue_date+datetime.timedelta(days=15))).days)
                            else:
                                keep_id = i.id
                                ry, rm, rd = rdate.split("-")
                                days_diff = abs((datetime.date(ry, rm, rd) - (i.if_issue_date+datetime.timedelta(days=15))).days)
                        else:
                            pass
                else:
                    pass

                o = Memberships.objects.get(id=keep_id)
                o.status = 'inactive'
                o.fine = '0'
                o.if_having_book = ''
                o.if_having_movie = ''
                o.if_issue_date = '1990-01-01'
                o.if_return_date = '1990-01-01'
                o.save()

                return render(request, 'management/trans.html',context={'payfine':[o.name, days_diff*10,days_diff]})
            except Exception as error_message:
                return render(request, 'management/trans.html', context={'error_message': error_message})
    else:

        #get method
        return render(request, 'management/trans.html',context={'pay_fine':'pay_fine'})


def retbook(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    else:
        return render(request, 'management/trans.html', context={'retbook': 'retbook'} )


def letsretbook(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')
    elif request.method == 'POST':
        try:

            serial = request.POST['serial'].upper()
            remarks = request.POST['remarks']

            for i in Memberships.objects.filter(Q(if_having_book='') ^ Q(if_having_movie='')):
                if i.if_having_book == serial:
                    keep_id = i.id

                elif i.if_having_movie == serial:
                    keep_id = i.id
                else:
                    pass
            try:
                b = Book.objects.filter(serial=serial)[0]
            except:
                b = Movies.objects.filter(serial=serial)[0]
            m = Memberships.objects.get(id=keep_id)
            name = b.name
            author = b.author
            idate = m.if_issue_date
            rdate = m.if_return_date

            return render(request, 'management/trans.html', context={'letsretbook': [name, author, serial, idate, rdate, remarks, 'payfine']})

        except Exception as error_message:
            return render(request, 'management/trans.html', context={'error_message': error_message})


    else:
        return render(request, 'management/trans.html', context={'error_message': 'something went wrong'} )


def isbookavail(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')


    elif request.method == 'POST':

        try:


            name = request.POST['name']
            author = request.POST['author']
            book_index = request.POST.get('drop_downb', False)
            #book_index = request.POST['drop_downb']
            movie_index = request.POST.get('drop_downm', False)
            #movie_index = request.POST['drop_downm']

            if name !="":
                temp_obj = list(Book.objects.filter(name=name))
                temp_obj += list(Movies.objects.filter(name=name))
                try:
                    author = temp_obj[0].author
                    return render(request, 'management/trans.html',context={'letsissue': [name,author]})

                except:
                    return render(request, 'management/trans.html', context={'error_message': "No movie with such name found :("})

            elif author !="":
                temp_obj = list(Book.objects.filter(name=author))
                temp_obj += list(Movies.objects.filter(name=author))
                try:
                    name=temp_obj[0].name
                    return render(request, 'management/trans.html', context={'letsissue': [name, author]})
                except:
                    return render(request, 'management/trans.html',
                                  context={'error_message': "No such name of Author/movie maker found :("})

            elif book_index !="":
                temp_obj =  [i.name for i in Book.objects.all()]
                try:
                    name = temp_obj[book_index]
                    author = list(Book.objects.filter(name=name))[0].author
                    return render(request, 'management/trans.html', context={'letsissue': [name, author]})
                except:
                    return render(request, 'management/trans.html',
                                  context={'error_message': "Something went wrong:("})

            elif movie_index !="":
                temp_obj = [i.name for i in Movies.objects.all()]
                try:
                    name = temp_obj[movie_index]
                    author = list(Movies.objects.filter(name=name))[0].author
                    return render(request, 'management/trans.html', context={'letsissue': [name, author]})
                except:
                    return render(request, 'management/trans.html',
                                  context={'error_message': "Something went wrong:("})


            else:
                return render(request, 'management/trans.html', context={'error_message': "Please Choose 1 option"})

        except Exception as error_message:
            return render(request, 'management/trans.html', context={'error_message': error_message})


    else:
        #get
        try:
            bobject = [i.name for i in Book.objects.all()]
            mobject = [i.name for i in Movies.objects.all()]
            return render(request, 'management/trans.html', context={'isbookavail': bobject, 'isbookavail2': mobject})
        except Exception as error_message:
            return render(request, 'management/trans.html', context={'error_message': error_message})

def letsissue(request):
    if not request.user.is_authenticated():
        return render(request, 'management/login.html')

    #get
    return render(request, 'management/trans.html', context={'letsissue': 'issue_happened'})