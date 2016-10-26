from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import UploadFileForm
from .models import Feedback
from .lemmatizer.lemmatizer import *

# Auxiliary functions

def lemmatize(string, par='text'):
    lem = Lemmatizer(string)
    return lem.lemmaText

# URLs

def index(request):
    return render(request, "ulster/index.html", context_instance=RequestContext(request))

def contacts(request):
    return render(request, "ulster/contacts.html", context_instance=RequestContext(request))
    
def send_feedback(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_comment = request.POST.get('message')
        feed = Feedback(username=user_name, email=user_email, message = user_comment )
        feed.save()
        thank = "Thank you for your feedback!"
        return render(request, "ulster/contacts.html", {'thankyou':thank}, context_instance=RequestContext(request))

def graph(request):
    return render(request, "ulster/graph.html", context_instance=RequestContext(request))
    
def info(request):
    return render(request, "ulster/info.html", context_instance=RequestContext(request))

def lemmatizer(request):
    return render(request, "ulster/lemmatizer.html", context_instance=RequestContext(request))
    
def corpus(request):
    return render(request, "ulster/corpus.html", context_instance=RequestContext(request))

def send_results(request):
    if request.method == 'POST':
        form = UploadFileForm()
        usertext = request.POST.get('usertext')
        par = request.POST.get('format')
        output = lemmatize(usertext, par)
        return render(request, "ulster/lemmatizer.html", {"usertext": usertext, "output_text": output, "form":form}, context_instance=RequestContext(request))
    else:
        return render(request, "ulster/lemmatizer.html", context_instance=RequestContext(request))
        
def download_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        format = request.POST.get('format')
        if form.is_valid():
            file = request.FILES['file']
            result = lemmatize(file.read().decode('utf-8'), format)
            response = HttpResponse(result, content_type='text/txt')
            response['Content-Disposition'] = 'attachment; filename="result.txt"'
            return response
    else:
        form = UploadFileForm()
    return render('ulster/lemmatizer.html', {'form': form}, context_instance=RequestContext(request))

