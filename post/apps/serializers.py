from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'

