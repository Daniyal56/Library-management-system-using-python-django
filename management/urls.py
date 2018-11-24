"""elevens_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

app_name = 'management'

urlpatterns = [
    
	
	url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^trans/$', views.transaction, name='trans'),
    url(r'^main/$', views.maintenance, name='main'),
    url(r'^repo/$', views.report, name='repo'),
    url(r'^mlmovies/$', views.mlmovies, name='mlmovies'),
    url(r'^mlbooks/$', views.mlbooks, name='mlbooks'),
    url(r'^mlmember/$', views.mlmember, name='mlmember'),
    url(r'^actissues/$', views.actissues, name='actissues'),
    url(r'^overdueslist/$', views.overdueslist, name='overdueslist'),
    url(r'^addmember/$', views.addmember, name='addmember'),
    url(r'^addbook/$', views.addbook, name='addbook'),
    url(r'^addsuperuser/$', views.addsuperuser, name='addsuperuser'),



]
