from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    return render(request, "index.html")

def createUser(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            print("User's password entered was " + request.POST['password'])
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],date_of_birth=request.POST['dob'], password=hashed_pw)
            print("User's password has been changed to " + user.password)
            print("User's First Name:" + user.first_name)
            print("User's Last Name:" + user.last_name)
            print("User's Email:" + user.email)
            print("Date of Birth: " + user.date_of_birth)
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]                    
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id #IMPORTANT!!!
                return redirect('/homepage')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Name not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def homepage(request):
    if request.method == "GET":
        if "user_id" in request.session:
            context = {
                "user": User.objects.get(id=request.session['user_id']),
                "allmessages": Message.objects.all().order_by('-created_at'),
                "comments": Comment.objects.all().order_by('-created_at'),
                "age": int((datetime.now().date() - (datetime.strptime(str(User.objects.get(id=request.session['user_id']).date_of_birth), "%Y-%m-%d").date())).days / 365),
            }
            return render(request, "homepage.html", context)
        else:
            return redirect('/')

def postMessage(request):
    if request.method == "POST":
        errors = Message.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            id = request.session['user_id']
            message = Message.objects.create(message = request.POST['message'], poster = User.objects.get(id = request.session['user_id']))
    return redirect('/homepage')

def deleteMessage(request, id):
    if request.method == "POST":
        MessagetoDelete = Message.objects.filter(id=id)
        if MessagetoDelete:
            delmessage = MessagetoDelete[0]
            user = User.objects.get(id=request.session['user_id'])
            if delmessage.poster == user:
                delmessage.delete()
    return redirect('/homepage')

def postComment(request, id):
    if request.method == "POST":
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            commentnew = Comment.objects.create(comment = request.POST['comment'], commenter = User.objects.get(id = request.session['user_id']), message_commented = Message.objects.get(id=id))
    return redirect('/homepage')

def deleteComment(request, id):
    if request.method == "POST":
        CommenttoDelete = Comment.objects.filter(id=id)
        if CommenttoDelete:
            delcomment = CommenttoDelete[0]
            user = User.objects.get(id=request.session['user_id'])
            if delcomment.commenter == user:
                delcomment.delete()
    return redirect('/homepage')

def logout(request):
    if request.method == "POST":
        request.session.clear()
    return redirect('/')