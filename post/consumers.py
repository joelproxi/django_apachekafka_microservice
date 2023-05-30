import json
import os
from datetime import datetime

import django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'post.settings')
django.setup()

from apps.models import Comment
from apps.serializers import CommentSerializer


conf = {
	'bootstrap.servers': 'localhost:8000',
	'group.id': 'blog',
	'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["django-blog-comment"])

while True:
	msg = consumer.poll(1.0)
	if msg is None:
		continue

	if msg.error():
		print("Consuming error %s" % str(msg.error()))
		continue

	print(msg.key())
	if msg.key() == b'comment-created':
		print('Reception du message {} '.format(json.loads(msg.value().decode("utf-8"))))
		data = json.loads(msg.value().decode('utf-8'))
		serializer = CommentSerializer(data={
			"id": data["id"],
			'content': data['content'],
			'author': data['author'],
			'created_at': datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:'),
			'updated_at': data['updated_at']
		})
		serializer.is_valid(raise_exception=True)
		serializer.save()

	if msg.key() == b'comment-updated':
		print('Reception du message {} '.format(json.loads(msg.value().decode("utf-8"))))
		data = json.loads(msg.value().decode('utf-8'))
		try:
			instance = Comment.objects.get(id=data['id'])
			serializer = CommentSerializer(instance=instance, data={
				"id": data["id"],
				'content': data['content'],
				'author': data['author'],
				'created_at': datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:'),
				'updated_at': data['updated_at']
			})
			serializer.is_valid(raise_exception=True)
			serializer.save()
		except Comment.DoesNotExist:
			print("Error, Comment not found")

	if msg.key() == b'comment-destroyed':
		print('Reception du message {} '.format(json.loads(msg.value().decode("utf-8"))))
		data = json.loads(msg.value().decode('utf-8'))
		try:
			instance = Comment.objects.get(id=data['id'])
			instance.delete()
		except Comment.DoesNotExist:
			print("Error, Comment not found")
