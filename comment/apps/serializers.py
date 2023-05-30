from rest_framework import serializers

from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id', 'content', 'author', 'post_id', 'created_at', 'updated_at',)


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
		# fields = ('id', 'content', 'author', 'created_at', 'updated_at', )
  


