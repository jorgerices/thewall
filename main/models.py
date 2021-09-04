from django.db import models
import re

# Create your models here.
class UsersManager(models.Manager):
    def user_validator(self, postData):
        
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')
        
        errors = {}
        emails = Users.objects.all().values('email')

        if len(postData['first_name'].strip()) < 2:
            errors['first_name_len'] = "El nombre debe tener al menos 2 letras de largo"
        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "El nombre contiene caracteres no válidos"
        if len(postData['last_name'].strip()) < 2:
            errors['last_name_len'] = "El apellido debe tener al menos 2 letras de largo"
        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras'] = "El apellido contiene caracteres no válidos"
        if postData['email'] in emails:
            errors['email'] = f'El email ingresado ya existe'
        if len(postData['password']) < 6:
            errors['password'] = "La contraseña debe tener al menos 6 caracteres"
        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "Las contraseñas no coinciden"
        
        return errors

class MessagesManager(models.Manager):
    def message_validator(self, postData):
        errors = {}

        if len(postData['message'].strip()) < 1 or len(postData['message'][0].strip()) > 500:
            errors['message_len'] = "El mensaje debe contener entre 1 y 500 caracteres"
        
        return errors

class CommentsManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}

        if len(postData['comment'].strip()) < 1 or len(postData['comment'].strip()) > 500:
            errors['comment_len'] = "El comentario debe tener entre 1 y 500 caracteres"
        
        return errors

class Users(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=255)
    allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

    def __repr__(self) -> str:
        return f'{self.id}: {self.first_name} {self.last_name}'

class Messages(models.Model):
    text_message = models.CharField(max_length=500)
    author_message = models.ForeignKey(Users, related_name='messages', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessagesManager()

    def __repr__(self) -> str:
        return f'{self.id}: {self.text_message}'
    
class Comments(models.Model):
    comment = models.CharField(max_length=500)
    user_id = models.ForeignKey(Users, related_name='comments', on_delete=models.CASCADE)
    message_id = models.ForeignKey(Messages, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentsManager()

    def __repr__(self) -> str:
        return f'{self.id}: {self.comment}'