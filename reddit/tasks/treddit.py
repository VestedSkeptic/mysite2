from celery import task
from django.core.exceptions import ObjectDoesNotExist
import time
from ..config import clog
from ..models import mcomment
from ..models import msubreddit
from ..models import mthread
from ..models import muser
from .tbase import getBaseP, getBaseC
# import pprint

# --------------------------------------------------------------------------
@task()
def TASK_updateUsersForAllComments(numberToProcess):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()
    countUsersAdded = 0

    qsCount = mcomment.objects.filter(puseradded=False).count()
    clog.logger.info("%s %d comments pending, processing %d" % (getBaseP(mi),  qsCount, numberToProcess))
    while qsCount > 0:
        # Look at first result
        i_mcomment = mcomment.objects.filter(puseradded=False)[0]

        # AddOrUpdate that user
        prawRedditor = prawReddit.redditor(i_mcomment.username)
        i_muser = muser.objects.addOrUpdate(prawRedditor)
        if i_muser.addOrUpdateTempField == "new":
            countUsersAdded += 1

        # set puseradded True for any false comments for that user
        qs2 = mcomment.objects.filter(puseradded=False).filter(username=i_mcomment.username)
        for item in qs2:
            item.puseradded = True
            item.save()

        # are there any puseradded False comments left
        qsCount = mcomment.objects.filter(puseradded=False).count()

        numberToProcess -= 1
        if numberToProcess <= 0:
            break

    clog.logger.info("%s %d comments pending, %d users added" % (getBaseC(mi, ts), qsCount, countUsersAdded))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateThreadCommentsByForest(numberToProcess):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()
    countCommentsAdded = 0

    qs = mthread.objects.filter(pdeleted=False, pforestgot=False).order_by("-rcreated")
    clog.logger.info("%s %d threads pending, processing %d" % (getBaseP(mi),  qs.count(), numberToProcess))

    countNew = 0
    countOldChanged = 0
    countOldUnchanged = 0
    countDeleted = 0

    for i_mthread in qs:
        try:
            params={};
            # params['before'] = i_mthread.getBestCommentBeforeValue(????)

            prawSubmissionObject = prawReddit.submission(id=i_mthread.fullname[3:])
            prawSubmissionObject.comment_sort = "new"

            # prawSubmissionObject.comments.replace_more(limit=None)
            prawSubmissionObject.comments.replace_more(limit=16)

            for prawComment in prawSubmissionObject.comments.list():
                if prawComment.author == None:
                    countDeleted += 1
                else:
                    i_mcomment = mcomment.objects.addOrUpdate(prawComment.author.name, prawComment)
                    if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                    if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                    if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1
        except praw.exceptions.APIException as e:
            clog.logger.info("%s %s PRAW_APIException: error_type = %s, message = %s" % (getBaseP(mi), username, e.error_type, e.message))

        i_mthread.pforestgot = True
        i_mthread.pcount += countNew
        i_mthread.save()

        numberToProcess -= 1
        if numberToProcess <= 0:
            break

    clog.logger.info("%s %d new comments, %d old, %d oldChanged, %d deleted" % (getBaseC(mi, ts), countNew, countOldUnchanged, countOldChanged, countDeleted))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateCommentsForUser(username):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    try:
        i_muser = muser.objects.get(name=username)
        clog.logger.info("%s %s" % (getBaseP(mi), username))

        prawReddit = i_muser.getPrawRedditInstance()

        params={};
        params['before'] = i_muser.getBestCommentBeforeValue(prawReddit)
        # clog.logger.info("before = %s" % (params['before']))

        # Moved below try statement using new i_msubreddit.threadsUpdated() method
        # i_muser.precentlyupdated = True
        # i_muser.save()

        # iterate through submissions saving them
        countNew = 0
        countOldChanged = 0
        countOldUnchanged = 0
        try:
            for prawComment in prawReddit.redditor(i_muser.name).comments.new(limit=None, params=params):
                i_mcomment = mcomment.objects.addOrUpdate(i_muser.name, prawComment)
                if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1
                i_mcomment.puseradded = True
                i_mcomment.save()
        except praw.exceptions.APIException as e:
            clog.logger.info("%s %s PRAW_APIException: error_type = %s, message = %s" % (getBaseC(mi, ts), username, e.error_type, e.message))

        beforeWarningString = ' [before]'
        if countNew == 0 and params['before'] != '':
            beforeWarningString = ' [** %s **]' % (params['before'])
        clog.logger.info("%s %s %d new, %d old, %d oldC %s" % (getBaseC(mi, ts), username, countNew, countOldUnchanged, countOldChanged, beforeWarningString))

        i_muser.commentsUpdated(countNew, countOldUnchanged, countOldChanged)
    except ObjectDoesNotExist:
        clog.logger.info("%s %s %s" % (getBaseC(mi, ts), username, "ERROR does not exist"))
    return ""

# --------------------------------------------------------------------------
@task()
# def TASK_updateCommentsForAllUsers(userCount, forceAllToUpdate):
def TASK_updateCommentsForAllUsers(userCount, priority):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # get userCount number of unprocessed users
    # qs = muser.objects.filter(ppoi=True).filter(precentlyupdated=False)[:userCount]
    qs = muser.objects.filter(ppoi=True).filter(precentlyupdated=False).filter(pprioritylevel=priority).order_by('name','pcommentsupdatetimestamp')[:userCount]


    # If all users have been recently processed
    # if qs.count() == 0 or forceAllToUpdate:
    if qs.count() == 0:
        # clog.logger.info("%s forceAllToUpdate [%d, %r] ================================" % (getBaseP(mi), qs.count(), forceAllToUpdate))
        clog.logger.info("%s forceAllToUpdate ================================, priority = %d" % (getBaseP(mi), priority))

        # set that flag to false for all users
        qs = muser.objects.filter(ppoi=True).filter(pprioritylevel=priority)
        for i_muser in qs:
            i_muser.precentlyupdated = False
            i_muser.save()

        # Call task again
        if qs.count() > 0:
            clog.logger.info("%s all users precentlyupdated reset, priority = %d" % (getBaseC(mi, ts), priority))
            TASK_updateCommentsForAllUsers.delay(userCount, priority)
        else:
            clog.logger.info("%s zero users precentlyupdated reset, priority = %d" % (getBaseC(mi, ts), priority))


    # otherwise process returned users
    else:
        clog.logger.info("%s %d users being processed, priority = %d" % (getBaseP(mi), qs.count(), priority))
        countOfTasksSpawned = 0
        for i_muser in qs:
            TASK_updateCommentsForUser.delay(i_muser.name)
            countOfTasksSpawned += 1
        clog.logger.info("%s %d tasks spawned" % (getBaseC(mi, ts), countOfTasksSpawned))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateThreadsForSubreddit(subredditName):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        clog.logger.info("%s %s" % (getBaseP(mi), subredditName))

        prawReddit = i_msubreddit.getPrawRedditInstance()

        params={};
        params['before'] = i_msubreddit.getThreadsBestBeforeValue(prawReddit)
        # clog.logger.info("before = %s" % (params['before']))

        # Moved below try statement using new i_msubreddit.threadsUpdated() method
        # i_msubreddit.precentlyupdated =True
        # i_msubreddit.save()

        countNew = 0
        countOldUnchanged = 0
        countOldChanged = 0
        try:
            for prawThread in prawReddit.subreddit(i_msubreddit.name).new(limit=None, params=params):
                i_mthread = mthread.objects.addOrUpdate(i_msubreddit, prawThread)
                if i_mthread.addOrUpdateTempField == "new":             countNew += 1
                if i_mthread.addOrUpdateTempField == "oldUnchanged":    countOldUnchanged += 1
                if i_mthread.addOrUpdateTempField == "oldChanged":      countOldChanged += 1
        except praw.exceptions.APIException as e:
            clog.logger.info("%s %s PRAW_APIException: error_type = %s, message = %s" % (getBaseC(mi, ts), subredditName, e.error_type, e.message))
        clog.logger.info("%s %s: %d new, %d old, %d oldChanged" % (getBaseC(mi, ts), subredditName, countNew, countOldUnchanged, countOldChanged))

        i_msubreddit.threadsUpdated(countNew, countOldUnchanged, countOldChanged)
    except ObjectDoesNotExist:
        clog.logger.info("%s %s, %s" % (getBaseC(mi, ts), subredditName, "ERROR does not exist"))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateThreadsForAllSubreddits(subredditCount, priority):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    qs = msubreddit.objects.filter(ppoi=True).filter(precentlyupdated=False).filter(pprioritylevel=priority).order_by('name','pthreadupdatetimestamp')[:subredditCount]

    # If all subreddits have been recently processed
    if qs.count() == 0:
        clog.logger.info("%s forceAllToUpdate ================================, priority = %d" % (getBaseP(mi), priority))

        # set that flag to false for all subreddits
        qs = msubreddit.objects.filter(ppoi=True).filter(pprioritylevel=priority)
        for i_msubreddit in qs:
            i_msubreddit.precentlyupdated = False
            i_msubreddit.save()

        # Call task again
        if qs.count() > 0:
            clog.logger.info("%s %d subreddits precentlyupdated reset, priority = %d" % (getBaseC(mi, ts), qs.count(), priority))
            TASK_updateThreadsForAllSubreddits.delay(subredditCount, priority)
        else:
            clog.logger.info("%s zero subreddits precentlyupdated reset, priority = %d" % (getBaseC(mi, ts), priority))

    # otherwise process returned subreddits
    else:
        clog.logger.info("%s %d subreddits being processed, priority = %d" % (getBaseP(mi), qs.count(), priority))
        countOfTasksSpawned = 0
        for i_msubreddit in qs:
            TASK_updateThreadsForSubreddit.delay(i_msubreddit.name)
            countOfTasksSpawned += 1
        clog.logger.info("%s %d tasks spawned" % (getBaseC(mi, ts), countOfTasksSpawned))
    return ""
