from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import NewsletterUserSignUpForm, NewsletterUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Newsletter
from newsletters.forms import NewsletterCreationForm

def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'El correo ya existe')
        else:
            instance.save()
            messages.success(request, 'Hemos enviado un correo electronico a su correo, ¡ABRALO! , para continuar con su entrenamiento')
            subject="Libro de cocina"
            from_email=settings.EMAIL_HOST_USER
            to_email=[instance.email]
            
            html_templates='newsletters/email_templates/welcome.html'
            html_message= render_to_string(html_templates)        
            message = EmailMessage(subject, html_message, from_email, to_email)
            message.content_subtype='html'
            message.send()
        
    context = {
        'form':form
    }
    return render(request, 'start-here.html', context)
            
def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'El email ha sido removido')
        else:
            print('Email no encontrado')
            messages.warning(request, 'Email no encontrado')
    
    context = {
        'form':form
    }
    
    return render(request, 'unsubscribe.html', context)

class NewsletterCreateView(View):
    def get(self, request, *args, **kwarg):
        form = NewsletterCreationForm()
        context = {
            'form':form
        }
        return render(request, 'dashboard/create.html', context)
    
    def post(self, request, *args, **kwarg):
        if request.method=="POST":
            form = NewsletterCreationForm(request.POST or None)

            if form.is_valid():
                instance = form.save()
                newsletter=Newsletter.objects.get(id=instance.id)
                
                if newsletter.status=="Published":
                    subject = newsletter.subject
                    body = newsletter.body
                    from_email = settings.EMAIL_HOST_USER
                    
                    for email in newsletter.email.all():
                        send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
                return redirect('dashboard:list')            

        context = {
            'form':form
        }
        return render(request, 'dashboard/create.html', context)

