import os
from slackclient import SlackClient

slack_token = os.environ["504848792676.506069341879"]
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="CEU87RR2L",
  text="Hello from Python! :tada:"
)