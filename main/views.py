from django.shortcuts import render
from main.forms import ContactForm, NewsletterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def index_view(request):
    return render(request, 'main/index.html')

def about_view(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #obj = form.save(commit=False)
            #obj.name = 'unknown'
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Ticket sent successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Ticket could not send')
    form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

def projects_view(request):
    return render(request, 'main/projects.html')

def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your email added successfully')
            return HttpResponseRedirect('/')
            
        else:
            messages.add_message(request, messages.ERROR, 'Something failed')
            return HttpResponseRedirect('/')
            

