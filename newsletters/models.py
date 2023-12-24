from django.db import models

#este es el modelo del usuario
class NewsletterUser(models.Model):
    #los parametros significan, null:Que si el espcio se deja en blanco,quiere decir que tiene que tener algo,escribir correo
    #unique: que el correo solo se incluya una unica vez,que no se replique
    email = models.EmailField(null=False, unique=True)
    #se agrega la fecha en automatico con el auto_now_add
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
#este es el modelo del newsletter
class Newsletter(models.Model):
    
    EMAIL_STATUS_CHOICES = (
        ('Draft', "Draft"),
        ('Published', "Published")
    )
    
    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    #los parametros indican que puede enviarse el correo aunque se deje en blanco
    body = models.TextField(blank=True, null=True)
    email = models.ManyToManyField(NewsletterUser)
    created = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering=('-created',)

