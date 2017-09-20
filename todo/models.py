# -*-coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User)
    todo = models.CharField(max_length=50)
    flag = models.CharField(max_length=2)
    priority = models.CharField(max_length=2)
    pubtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%d %s %s' % (self.id, self.todo, self.flag)

    @property
    def priority_text(self):
        priority_text = ''
        if self.priority == '1':
            priority_text = 'High'
        elif self.priority == '2':
            priority_text = 'Medium'
        elif self.priority == '3':
            priority_text = 'Low'
        return priority_text

    class Meta:
        ordering = ['priority', 'pubtime']

# Create your models here.
