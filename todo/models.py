from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Todo(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(blank=True)
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField(default=False, verbose_name='is done?')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    class Meta:
        db_table = 'todos'

    def __str__(self) -> str:
        return self.title
