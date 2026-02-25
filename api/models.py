from django.db import models
from django.contrib.auth.models import User


class DateTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Task(DateTimeStamp):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    

class UserProfile(DateTimeStamp):
    USER_ROLE = (
        ('admin','Admin'),
        ('user','Regular User')
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role = models.CharField(max_length=10,choices=USER_ROLE,default='user')

    def __str__(self):
        return f"Username-->{self.user.username}, Role-->{self.role}"