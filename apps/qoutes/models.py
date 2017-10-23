# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {
            'error': []
        }
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errors['error'].append('Your name and alias must be longer than 1 character')
        if postData['password'] != postData['confirm_password']:
            errors['error'].append('Your password does not match the confim password')
        if EMAIL_REGEX.match(postData['email']) is None:
            errors['error'].append('Invalid email format')
        if User.objects.filter(email=postData['email']):
            errors['error'].append('Email already registered')
        if postData['birthday']:
            if datetime.now() < datetime.strptime(postData['birthday'],'%Y-%m-%d'):
                errors['error'].append('Your birthday can not be in the future.')
        else:
            errors['error'].append('Please enter in your birthday')
        try:
            validate_password(postData['password'])
        except Exception as e:
            errors['password'] = e
        return errors

    def password_hasher(self, pw):
        hashed_password = make_password(pw)
        return hashed_password

    def password_checker(self, pw, encoded_pw):
        return check_password(pw, encoded_pw)

class QouteManager(models.Manager):
    def qouteValidator(self, postData):
        errors = []
        if len(postData['qoute_by']) < 4:
            errors.append('Qouted By must be longer than 3 characters')
        if len(postData['message']) < 11:
            errors.append('Message must be longer than 10 characters')
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Qoute(models.Model):
    qoute_by = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(User, related_name='posted_qoutes')
    followed_by = models.ManyToManyField(User, related_name='followed_qoutes')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = QouteManager()
