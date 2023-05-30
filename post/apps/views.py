import json

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Post
from post.producer import producer


# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        producer.produce('django-blog-post', key="post-created",
                         value=json.dumps(serializer.data),
                         callback=self.acker)
        producer.poll(1)
        print(serializer.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance,
                                           data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        producer.produce('django-blog-post', key="post-updated",
                         value=json.dumps(serializer.data),
                         callback=self.acker)
        producer.poll(1)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.serializer_class(instance)
        print(data.data)
        self.perform_destroy(instance)
        producer.produce('django-blog-post', key="post-destroyed",
                         value=json.dumps(data.data),
                         callback=self.acker)
        producer.poll(1)
        return Response(data=data.data)

    @staticmethod
    def acker(err, msg):
        if err is not None:
            print("Failled to delivre message: %s: %s " % (str(err), str(msg)))
        else:
            print("Messsage processed: %s " % str(msg))
