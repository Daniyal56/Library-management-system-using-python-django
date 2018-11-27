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
    url(r'^payfine/$', views.payfine, name='payfine'),
    url(r'^retbook/$', views.retbook, name='retbook'),
    url(r'^letsretbook/$', views.letsretbook, name='letsretbook'),
    url(r'^isbookavail/$', views.isbookavail, name='isbookavail'),
    url(r'^letsissue/$', views.letsissue, name='letsissue'),
    url(r'^letsissuedirectly/$', views.letsissue, name='letsissuedirectly'),
    url(r'^updatemember/$', views.updatemember, name='updatemember'),
    url(r'^updatebook/$', views.updatebook, name='updatebook'),



]
