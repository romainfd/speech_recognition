# -*- coding: UTF-8 -*-

from fbchat import Client
from fbchat.models import *

client = Client('terre.ferme91@gmail.com', 'mdpmaurice')

print('Own id: {}'.format(client.uid))
romain_uid = "100005420857065"
group_uid = "1938896156193853"

# client.send(Message(text='Hi Romain!'), thread_id=romain_uid, thread_type=ThreadType.USER)
# client.send(Message(text='Salut tout le monde!'), thread_id=group_uid, thread_type=ThreadType.GROUP)
# client.sendLocalFiles("audio/Deadbolt_Lock.mp3", message="Coucou", thread_id=romain_uid, thread_type=ThreadType.USER)
# client.logout()


def send(filepath, message, dest, dest_type):
    if dest_type == "user":
        dest_type = ThreadType.USER
    else:
        dest_type = ThreadType.GROUP
    client.sendLocalFiles(filepath, message=message, thread_id=dest, thread_type=dest_type)
