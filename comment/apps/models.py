from django.db import models
from django.utils import timezone


# Create your models here.


class CreationModificationMixin(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		ordering = ('-created_at',)
		indexes = [models.Index(fields=['-created_at', ])]


class Post(models.Model):
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=255)
	content = models.TextField()
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(editable=True)
	updated_at = models.DateTimeField(editable=True)

	class Meta:
		ordering = ('-created_at',)
		indexes = [models.Index(fields=['-created_at', ])]

	def __str__(self):
		return self.title


class Comment(CreationModificationMixin):
	content = models.CharField(max_length=500)
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.CharField(max_length=255)

	class Meta(CreationModificationMixin.Meta):
		pass

	def __str__(self):
		return self.content[:20]