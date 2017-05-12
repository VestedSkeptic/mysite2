from __future__ import unicode_literals
from django.db import models
from .mBase import mBase
from .mSubreddit import mSubreddit

# *****************************************************************************
class mSubmission(mBase, models.Model):
    subreddit       = models.ForeignKey(mSubreddit, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    cForestGot      = models.BooleanField(default=False)
    count           = models.PositiveIntegerField(default=0)
    def __str__(self):
        s = self.subreddit.name
        s += " [" + self.name + "]"
        s += " [" + str(self.count) + "]"
        if self.cForestGot: s += " (cForestGot = True)"
        else:               s += " (cForestGot = False)"
        return format(s)

# *****************************************************************************
# class subredditSubmissionRaw(models.Model):
class mSubmissionRaw(models.Model):
    index           = models.OneToOneField(mSubmission, primary_key=True)
    data            = models.TextField()
    def __str__(self):
        s = self.index.subreddit.name
        s += ": " + self.data
        return format(s)

# *****************************************************************************
# class subredditSubmissionFieldsExtracted(models.Model):
class mSubmissionExtracted(models.Model):
    index           = models.OneToOneField(mSubmission, primary_key=True)

    author          = models.CharField(max_length=21)
    created_utc     = models.DateTimeField()
    is_self         = models.BooleanField()
    title           = models.CharField(max_length=301)
    selftext        = models.TextField()

    def __str__(self):
        s = self.index.subreddit.name
        s += ": " + self.title
        return format(s)
