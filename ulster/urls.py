from django.conf.urls import url

from . import views

app_name = 'ulster'
urlpatterns = [
        url(r'^$', views.index, name='index'),
		url(r'^home', views.index, name='index'),
        url(r'^graph$', views.graph, name='graph'),
		url(r'^info$', views.info, name='info'),
		url(r'^lemmatizer', views.send_results, name='lemmatizer'),
		url(r'^lemmatizer/download', views.download_file, name="download"),
		url(r'^contacts', views.contacts, name='contacts'),
		url(r'^thanks/$', views.send_feedback, name='feedback'),
		url(r'^corpus', views.corpus, name='corpus'),
]