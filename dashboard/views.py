from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, View, UpdateView, DeleteView
from newsletters.forms import NewsletterCreationForm
from newsletters.models import Newsletter
from django.core.mail import EmailMessage, send_mail

class DashboardHomeView(TemplateView):
    template_name = 'dashboard/index.html'

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
        return render(request, 'templates/create.html', context)
    
class NewslettersDashboardHomeView(View):
    def get(self, request, *args, **kwargs):
        newsletters=Newsletter.objects.all()
        context = {
            'newsletters':newsletters
        }
        return render(request, 'dashboard/list.html', context)
    
class NewsletterDetailView(View):
    def get(self, request, pk, *arg, **kwargs):
        newsletter=get_object_or_404(Newsletter, pk=pk)
        context = {
            'newsletter':newsletter
        }
        return render(request, 'dashboard/detail.html', context)
    

class NewsletterUpdateView(UpdateView):
    model =  Newsletter
    form_class = NewsletterCreationForm
    template_name = 'dashboard/update.html'
    success_url = 'dashboard/detail/5/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type':'update'
        })
        return context
    
    
    def post(self, request, pk, *args, **kwarg):
        newsletter = get_object_or_404(Newsletter, pk=pk)
        
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
                return redirect('dashboard:detail', pk=newsletter.id)            
            return redirect('dashboard:detail', pk=newsletter.id)            
        else:
            form = NewsletterCreationForm(instance=newsletter)

        context = {
            'form':form
        }
        return render(request, 'templates/update.html', context)

class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'dashboard/delete.html'
    success_url = '/dashboard/list'