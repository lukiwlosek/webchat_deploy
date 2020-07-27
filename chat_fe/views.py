from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Friend, Client, Message
from django.contrib.auth.models import User
from .forms import RegistrationForm


import stripe

stripe.api_key = "sk_test_51H4RG6FHNlgQ0cmkER7xeXtjcUUdbdLG3J85CGHUpb80NNkcT3nL3uCofsSICJXgzsSvAaZVf1oxkM6uDDe4mWMs00KflZM4Ot"


# Create your views here.
@login_required
def chat(request, room_name):

    user = request.user.get_username()
    user1 = request.user
    client = Client.objects.get(client=user1.id)
    friend_name = Friend.objects.get(current_user=client, room=room_name)
    other_user = friend_name.other_user.client
    acc_number = friend_name.other_user.account_number
    connected = "no"
    if acc_number != "":
        connected = "yes"
    print(connected)
    args = {
        "text": mark_safe(json.dumps(user)),
        "room_name": room_name,
        "friend_name": other_user,
        "connected": connected,
    }
    return render(request, "chat.html", args)


# class ChatClassView(TemplateView):

# 	template_name='enter.html'

# 	def post(self, request):
# 		text = request.POST
# 		userdata = text.get("user")
# 		args = {
# 			'text':mark_safe(json.dumps(userdata)),
# 			'room_name': "room1"
# 		}
# 		return render(request, 'chat.html', args)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = RegistrationForm()

        args = {"form": form}

    return render(request, "register.html", {"form": form})


connected_account_id = ""


@login_required
def dashboard(request):
    # all of this would be so much better in a rest API
    user = request.user
    client = Client.objects.get(client=user)
    users = User.objects.exclude(id=user.id)

    auth_code = request.GET.get("code")
    print(auth_code)
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=auth_code,)
        connected_account_id = response["stripe_user_id"]
        # add clients account number for stripe
        client.account_number = connected_account_id
        client.save()
    except:
        print("error")

    print(client.account_number)

    friends = Friend.objects.all().filter(current_user=client)
    # checking the list of friends and users0
    temp = []
    users_arr = []
    for friend in friends:
        temp.append(friend.other_user.client)

    for user in users:
        if not user in temp:
            users_arr.append(user)
    args = {"friends": friends, "users": users_arr}
    return render(request, "dashboard.html", args)


@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    new_client = Client.objects.get(client=new_friend)
    current_user = User.objects.get(pk=request.user.pk)
    current_client = Client.objects.get(client=current_user)
    if operation == "add":
        # make friends
        Friend.objects.get_or_create(
            current_user=current_client,
            other_user=new_client,
            room=current_user.pk + new_friend.pk,
        )
        Friend.objects.get_or_create(
            current_user=new_client,
            other_user=current_client,
            room=current_user.pk + new_friend.pk,
        )
    elif operation == "remove":
        instance = Friend.objects.filter(other_user_id=new_client)
        instance2 = Friend.objects.filter(other_user_id=current_client)
        instance.delete()
        instance2.delete()

    return redirect("/chat/")


def index(request, user, room):
    args = {"user": user, "room": room}

    return render(request, "index.html", args)


def success(request, user, room):

    if request.method == "POST":
        print("Data: ", request.POST)
        customer = stripe.Customer.create(
            email=request.POST["email"],
            name=request.user.username,
            source=request.POST["stripeToken"],
        )
        amount = int(request.POST["amount"])
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,  # penies
            currency="gbp",
            description="Donation",
            # stripe_account='{{CONNECTED_STRIPE_ACCOUNT_ID}}'
        )
        username = User.objects.get(username=user)
        client = Client.objects.get(client=username)
        account_number = client.account_number
        transfer = stripe.Transfer.create(
            amount=amount * 100, currency="gbp", destination=account_number,
        )

        # send in database a transaction
        user_paying = User.objects.get(username=request.user.username)
        client_paying = Client.objects.get(client=user_paying)
        client_payed = client
        msg = str("Payed " + request.POST["amount"] + "GBP to " + user)
        # need the roomName
        rooms = Friend.objects.filter(room=room)
        message = Message.objects.create(user=request.user, messenger=msg)
        for room in rooms:
            room.messages.add(message)

    return render(request, "success.html")

