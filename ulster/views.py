import json, time
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.template import RequestContext
from django.core.mail import mail_admins
from django.conf import settings
from django.http import JsonResponse
from .forms import UploadFileForm, ContactForm
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
        form = ContactForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            answer = 'Thank you for your feedback!'

            recipients = ['oksana.dereza@gmail.com']

            if name and message and sender:
                try:
                    send_mail(name, message + '\n' + sender, sender, recipients, fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header')

        return HttpResponse(json.dumps({'message': answer}))
            # return HttpResponseRedirect('/thanks/')
    else:
      form = ContactForm()
    return render(request, 'ulster/contacts.html', {'form': form})

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
        
# def download_file(request):
    # if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        # format = request.POST.get('format')
        # if form.is_valid():
            # file = request.FILES['file']
            # result = lemmatize(file.read().decode('utf-8'), format)
            # response = HttpResponse(result, content_type='text/txt')
            # response['Content-Disposition'] = 'attachment; filename="result.txt"'
            # return response
    # else:
        # form = UploadFileForm()
    # return render('ulster/lemmatizer.html', {'form': form}, context_instance=RequestContext(request))

