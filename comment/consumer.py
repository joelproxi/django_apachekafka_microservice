import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comment.settings')
django.setup()

from datetime import datetime

from confluent_kafka import Consumer

from apps.serializers import PostSerializer
from apps.models import Post


consumer = Consumer({
	'bootstrap.servers': 'localhost:9092',
	'group.id': 'blog',
	'auto.offset.reset': 'earliest'
})

consumer.subscribe(['django-blog-post'])

while True:
	msg = consumer.poll(1.0)
	if msg is None:
		continue

	if msg.error():
		print("Consuming Error %s" % msg.error())
		continue

	print(str(msg.key()))
	if msg.key() == b"post-created":
		print(msg.key() == b"post-created")
		print("Reception du message {}".format(json.loads(msg.value().decode('utf-8'))))
		data = json.loads(msg.value())
		serializer = PostSerializer(data={
			'id': data['id'],
			'title': data['title'],
			'content': data['content'],
			'author': data['author'],
			'created_at': data['created_at'],
			'updated_at': data['updated_at']
		})
		serializer.is_valid(raise_exception=True)
		serializer.save()

	if msg.key() == b"post-updated":
		print(msg.key() == b"post-updated")
		data = json.loads(msg.value())
		try:
			post = Post.objects.get(id=data['id'])
			serializer = PostSerializer(instance=post, data={
							'id': data['id'],
                            'title': data['title'],
                            'content': data['content'],
                            'author': data['author'],
                            'created_at': data['created_at'],
                            'updated_at': data['updated_at']
						})
			serializer.is_valid(raise_exception=True)
			serializer.save()
		except Post.DoesNotExist:
			print("Error")

	if msg.key() == b"post-destroyed":
		data = json.loads(msg.values())
		try:
			post = Post.objects.get(id=data['id'])
			post.delete()
		except Post.DoesNotExist:
			print("Error")


consumer.close()