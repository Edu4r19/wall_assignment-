from django.db import models
import re
from datetime import datetime

class UserManager(models.Manager):
    def create_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 3:
            errors['first_name'] = "First Name is too short"
        # users_with_fname = User.objects.filter(name=requestPOST['first_name'])
        # if len(users_with_fname) > 0:
        #     errors['dupfirst'] = "First Name already taken"
        FNAME_REGEX = re.compile(r'^[a-zA-Z-]+$')
        if len(requestPOST['first_name']) > 0:
            if not FNAME_REGEX.match(requestPOST['first_name']):
                errors['first_name_format'] = "First Name must not contain numbers or especial characters"
        if len(requestPOST['last_name']) < 3:
            errors['last_name'] = "Last Name is too short"
        # users_with_lname = User.objects.filter(name=requestPOST['last_name'])
        # if len(users_with_lname) > 0:
        #     errors['duplast'] = "Last Name already taken"
        LNAME_REGEX = re.compile(r'^[a-zA-Z-]+$')
        if len(requestPOST['last_name']) > 0:
            if not LNAME_REGEX.match(requestPOST['last_name']):
                errors['last_name_format'] = "Last Name must not contain numbers or especial characters"
        if len(requestPOST['email'])< 5:
            errors['email'] = "Email too short"
        users_with_email_dup = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email_dup) > 0:
            errors['dupemail'] = "Email already in use in another account"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(requestPOST['email']) > 0:                                         
            if not EMAIL_REGEX.match(requestPOST['email']):
                errors['email_format'] = "Email is not in correct format"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['password_conf']:
            errors['no_match'] = "Password and Password Confirmation must match"
        if len(requestPOST['dob']) <8:
            errors['date'] = "Enter a valid Date"
        else:
            date1 = datetime.strptime(requestPOST['dob'], "%Y-%m-%d").date()
            if date1 >= datetime.now().date():
                errors['future_date'] = "Birth Date must be in the Past" 
            age = int((datetime.now().date() - date1).days / 365)
            print(age)
            if age<13:
                errors['minor'] = "You Should be at least 13 years old to continue (COPPA Compliant)"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.TextField()
    date_of_birth = models.DateField(default=2000-1-1)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class MessageManager(models.Manager):
    def message_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['message']) < 1:
            errors['message_short']= "Message too short"
        return errors


class Message(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User, related_name='messages', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def comment_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['comment']) < 1:
            errors['comment_short']= "Comment too short"
        return errors

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, related_name='comments', on_delete= models.CASCADE)
    message_commented = models.ForeignKey(Message, related_name='comments_on_message', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()