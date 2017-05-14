from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser

# *****************************************************************************
def displayDatabaseModelCounts():
    users_poi               = muser.objects.filter(poi=True).count()
    users_notPoi            = muser.objects.filter(poi=False).count()

    users_ci                = mcomment.objects.filter(deleted=False).count()
    users_ci_deleted        = mcomment.objects.filter(deleted=True).count()

    subreddits              = msubreddit.objects.all().count()

    subreddits_si           = mthread.objects.filter(deleted=False).count()
    subreddits_si_deleted   = mthread.objects.filter(deleted=True).count()

    s = ''
    s += '<BR>==========================='
    s += '<BR>musers poi = ' + str(users_poi)
    s += '<BR>musers !poi = ' + str(users_notPoi)
    s += '<BR>'
    s += '<BR>mcomments = ' + str(users_ci)
    s += '<BR>mcomments deleted = ' + str(users_ci_deleted)
    s += '<BR>'
    s += '<BR>msubreddits = ' + str(subreddits)
    s += '<BR>'
    s += '<BR>mthreads = ' + str(subreddits_si)
    s += '<BR>mthreads deleted = ' + str(subreddits_si_deleted)
    s += '<BR>==========================='
    s += '<BR>'
    return s

# *****************************************************************************
def main(request, xData=None):
    clog.dumpMethodInfo()

    vs  = 'vbase.main:'
    moreData = request.session.get(xData, '')
    vs += moreData


    vs += '<br><b>vuser</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vuser/add/OldDevLearningLinux">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'

    vs += '<br><b>vsubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/add/Molw">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/update">update</a>'

    vs += '<br><b>vthread</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vthread/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'

    vs += '<br>' + displayDatabaseModelCounts()

    return HttpResponse(vs)



