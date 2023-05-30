import json
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer
from comment.producer import producer

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        producer.produce("django-blog-comment", key="comment-created",
                         value=json.dumps(serializer.data), callback=self.acker
                         )
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        producer.produce("django-blog-comment", key="comment-updated",
                         value=json.dumps(serializer.data), callback=self.acker
                         )
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.serializer_class(instance)
        print(data.data)
        self.perform_destroy(instance)
        producer.produce("django-blog-comment", key="comment-destroyed",
                         value=json.dumps(data.data), callback=self.acker
                         )
        return Response(data=data.data)

    @staticmethod
    def acker(self, err, msg):
        if err is not None:
            print("Failed to delivred message: %s: %s" % str(err), str(msg))
        else:
            print("Message has successfully processed %s" % str(msg))
