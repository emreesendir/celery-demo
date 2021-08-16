import json
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

@shared_task
def sum(num1,num2):
    reply = {}
    reply['result'] = int(num1) + int(num2)
    async_to_sync(channel_layer.group_send)('operations', {
        'type': 'result',
        'reply': json.dumps(reply)
        })
    return reply['result']