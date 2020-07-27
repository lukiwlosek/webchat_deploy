from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


User = get_user_model()


class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, blank=True)


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        client_profile = Client.objects.create(client=kwargs["instance"])


post_save.connect(create_profile, sender=User)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messenger = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    # representation of an object as string
    def __str__(self):
        return self.user.username

    def last_10():
        return Message.objects.order_by("-timestamp").all()[:10]


class Friend(models.Model):
    current_user = models.ForeignKey(
        Client, related_name="other_user", on_delete=models.CASCADE
    )
    other_user = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    room = models.CharField(max_length=20, default=0)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return self.current_user.client.username

    def get_pk(self):
        return self.pk

    def get_messages(self):
        return self.messages.order_by("-timestamp").all()[:10]

