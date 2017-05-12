from __future__ import unicode_literals
from django.db import models
# from .constants import *

# *****************************************************************************
class user(models.Model):
    name            = models.CharField(max_length=30)
    poi             = models.BooleanField(default=False)
    cHistoryGot     = models.BooleanField(default=False)
    def __str__(self):
        s = self.name
        if self.poi:
            s += " (poi)"
        if self.cHistoryGot: s += " (cHistoryGot = True)"
        else:                s += " (cHistoryGot = False)"
        return format(s)

# *****************************************************************************
class userCommentsIndex(models.Model):
    user            = models.ForeignKey(user, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    parent_id       = models.CharField(max_length=12)
    submission_id   = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    def __str__(self):
        s = self.user.name
        s += " [" + self.name + "]"
        s += " [submisson_id=" + self.submission_id + "]"
        s += " [parent_id=" + self.parent_id + "]"
        return format(s)

# *****************************************************************************
class userCommentsRaw(models.Model):
    uci             = models.OneToOneField(userCommentsIndex, primary_key=True)
    data            = models.TextField()
    def __str__(self):
        s = self.uci.user.name
        s += " [" + self.data + "]"
        return format(s)

# *****************************************************************************
class subreddit(models.Model):
    name            = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class subredditSubmissionIndex(models.Model):
    subreddit       = models.ForeignKey(subreddit, on_delete=models.CASCADE,)
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
class subredditSubmissionRaw(models.Model):
    ssi             = models.OneToOneField(subredditSubmissionIndex, primary_key=True)
    data            = models.TextField()
    def __str__(self):
        s = self.ssi.subreddit.name
        s += ": " + self.data
        return format(s)

# *****************************************************************************
class subredditSubmissionFieldsExtracted(models.Model):
    ssi             = models.OneToOneField(subredditSubmissionIndex, primary_key=True)

    author          = models.CharField(max_length=21)
    created_utc     = models.DateTimeField()
    is_self         = models.BooleanField()
    title           = models.CharField(max_length=301)
    selftext        = models.TextField()

    def __str__(self):
        s = self.ssi.subreddit.name
        s += ": " + self.title
        return format(s)

# *****************************************************************************
def getDictOfClassModelFieldNames(classModel):
    rvDict = {}
    fields = classModel._meta.get_fields()
    for field in fields:
        rvDict[field.name] = None
    return rvDict

# *****************************************************************************
def getFieldValueFromRawData(fieldName, rawData):
    rv = None
    return rv



# , 'subreddit': Subreddit(display_name='molw')
# , 'author': Redditor(name='OldDevLearningLinux')
# , '_reddit': <praw.reddit.Reddit object at 0x7f13453b1ad0>









