# from django.shortcuts import render
from django.http import HttpResponse
from redditusers.models import reddituser
import requests, json

# def index(request):
#     r = requests.get('https://www.reddit.com/user/BeneficEvil/comments/.json')
#     d = r.json()
#     # return HttpResponse(d.keys())     # works
#     # return HttpResponse(d['kind'])    # works
#     # return HttpResponse(d['data']['modhash'])     #fails
#     # return HttpResponse(r, content_type="application/json") # works
#     # return HttpResponse(d['data']['children'][0]['kind'])     # works
#     # return HttpResponse(d['data']['children'][0]['data']['link_id']) #works
#     return HttpResponse(d['data']['children'][0]['data']['body']) #works

# *****************************************************************************
def getCommentQuery(redditusername, after):
    rv = 'https://www.reddit.com/user/'
    rv += redditusername
    rv += '/comments/.json'
    if after is not None:
        rv += '?after='
        rv += after
    return rv
    
# *****************************************************************************
def displayMessageFromDict(d):
    rv = "MESSAGE: " + d['message']
    if 'error' in d:
        rv += ", " + "ERROR: " + str(d['error'])
    return rv
    
# *****************************************************************************
def displayUnknownDict(d):
    rv = "UNKNOWN: " + json.dumps(d)
    return rv
    
# *****************************************************************************
def returnStringValueOrNoneIfNone(v):
    if v is not None: return v
    else:             return "None"
    
# *****************************************************************************
def displayCommentListingDictMeta(d):
    rv = "KIND: " 
    if 'kind' in d: rv += d['kind']
    else:           rv += "ERROR kind NOT FOUND"
    
    if 'data' in d: 
        rv += ", DATA: "
        if 'after' in d['data']:    rv += "AFTER: "       + returnStringValueOrNoneIfNone(d['data']['after'])   + ", "
        if 'before' in d['data']:   rv += "BEFORE: "      + returnStringValueOrNoneIfNone(d['data']['before'])  + ", "
        if 'modhash' in d['data']:  rv += "MODHASH: "     + returnStringValueOrNoneIfNone(d['data']['modhash']) + ", "
        if 'children' in d['data']: rv += "CHILDREN: "    + str(len(d['data']['children']))
    else:
        rv += "ERROR data NOT FOUND"    
    return rv    
        
# *****************************************************************************
def processCommentListingDataChildren(d, after):
    rv = ""
    if 'children' in d['data']:
        for cd in d['data']['children']:
        	rv += cd['kind']
    
    if 'after' in d['data']: after = d['data']['after']
    else:                    after = None
    
    return rv;    
        
        
        # s += "<br>" + 
        # 
        # 
        # validToContinue = False
        # 
        # s += "<br>  "
        # 
        # 
        # if 'kind' in d:
        #     s += "KIND: " + d['kind'] + ", "
        #     validToContinue = True
        #     
        # if validToContinue:
        #     
        #     
        # # if 'error' in d:
        # #     s += "ERROR: " + d['ERROR'] + ", "
        # #     
        # # if 'error' in d:
        # #     s += "ERROR: " + d['ERROR'] + ", "
        # #     
        # # if 'error' in d:
        # #     s += "ERROR: " + d['ERROR'] + ", "
        # #     
        # # if 'error' in d:
        # #     s += "ERROR: " + d['ERROR'] + ", "
        # #     
        # # if 'error' in d:
        # #     s += "ERROR: " + d['ERROR'] + ", "                                                
        #                         
        # # 
        # # d_string = json.dumps(d);
        # # s += d_string
        
        
        
  
# *****************************************************************************
def index(request):
    all_entries = reddituser.objects.all()
        
    rv = ""
    for entry in all_entries:
        after = None
        commentQuery = getCommentQuery(entry.username, after)
        r = requests.get(commentQuery)
        d = r.json()
        
        if 'message' in d:
            rv += displayMessageFromDict(d)
        elif 'data' in d:
            rv += displayCommentListingDictMeta(d)
            rv += processCommentListingDataChildren(d, after)
            # after = processCommentListingDict(d)
            # while after is not None:
            #     after = BLUEBLUEBLUE
            # move all this processing inside for entry in all_entries: into method which canb e called recursively
        else:
            rv += displayUnknownDict(d)
    return HttpResponse(rv)         

    
    
# TOO MANY REQUESTS ERROR format
# {"message": "Too Many Requests", "error": 429}
    
    
# Three queries to get user comments using after value from previous    
# https://www.reddit.com/user/stp2007/comments/.json    
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d8fi1ll
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d6b14um    
        
# DATA RETURNED EXAMPLE: 
# Ref: https://www.reddit.com/user/stp2007/comments/.json
# 
# {
# 
#     "kind": "Listing",
#     "data": {
#         "modhash": "hj77s0ibuhebaad32541010db610a61628b19de76615967c14",
#         "children": [
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2cneq",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5uwglj",
#                     "link_author": "tomwoods55",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "ddxet17",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 18,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5uwglj",
#                     "subreddit_name_prefixed": "r/politics",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "[Here is the text for e-411](https://petitions.parl.gc.ca/en/Petition/Details?Petition=e-411) which M-103 references. It is a short 3 bullet points. It points out that Islam has 1.5 billion followers and only a very small number of them are performing or promoting extremist actions.\n\n[Here is the text for M-103](http://www.parl.gc.ca/Parliamentarians/en/members/Iqra-Khalid\\(88849\\)/Motions). It is one paragraph in length. It points out the rising climate of hate and fear against Islam and the Islamophobia that results in racism and religious discrimination. Its goal is a study to recognize and reduce Islamophobia.\n\nNeither mention or promote Sharia law.\n\nNeither are proposing laws which would prevent criticism of Islam.\n\n\n\n\n",
#                     "link_title": "M103 first step for Sharia in Canada must be stopped!",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;&lt;a href=\"https://petitions.parl.gc.ca/en/Petition/Details?Petition=e-411\"&gt;Here is the text for e-411&lt;/a&gt; which M-103 references. It is a short 3 bullet points. It points out that Islam has 1.5 billion followers and only a very small number of them are performing or promoting extremist actions.&lt;/p&gt;\n\n&lt;p&gt;&lt;a href=\"http://www.parl.gc.ca/Parliamentarians/en/members/Iqra-Khalid(88849)/Motions\"&gt;Here is the text for M-103&lt;/a&gt;. It is one paragraph in length. It points out the rising climate of hate and fear against Islam and the Islamophobia that results in racism and religious discrimination. Its goal is a study to recognize and reduce Islamophobia.&lt;/p&gt;\n\n&lt;p&gt;Neither mention or promote Sharia law.&lt;/p&gt;\n\n&lt;p&gt;Neither are proposing laws which would prevent criticism of Islam.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "politics",
#                     "name": "t1_ddxet17",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1487506340.0,
#                     "author_flair_text": null,
#                     "link_url": "https://cdnpoli.net/links/m103-first-step-for-sharia-in-canada-must-be-stopped-456546",
#                     "created_utc": 1487477540.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 18
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2qhx3",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5sulcq",
#                     "link_author": "Doomsy_",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "ddibo97",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 5,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5sulcq",
#                     "subreddit_name_prefixed": "r/climate",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Something like 99.9 percent of all species that have ever lived are now extinct. We may be the first intelligent enough to know this. We don't seem wise enough to act accordingly to prevent it happening to us. ",
#                     "link_title": "Is the human race doomed?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Something like 99.9 percent of all species that have ever lived are now extinct. We may be the first intelligent enough to know this. We don&amp;#39;t seem wise enough to act accordingly to prevent it happening to us. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "climate",
#                     "name": "t1_ddibo97",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1486625407.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/climate/comments/5sulcq/is_the_human_race_doomed/",
#                     "created_utc": 1486596607.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 5
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2qh49",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5r43td",
#                     "link_author": "kn0thing",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dd4ayee",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 1,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5r43td",
#                     "subreddit_name_prefixed": "r/blog",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "/u/kn0thing how about implementing ways to prevent Reddit from being used as a tool against what you hold dear? Such as allowing sub-reddits (or individual users) to create a minimum barrier of entry filter for posts or comments. Filter factors could be age of account, percentage of link posts vs comment posts, etc. This would go a long way towards combating new accounts set up to post bias articles and troll in various sub-reddits.  ",
#                     "link_title": "An Open Letter to the Reddit Community",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;&lt;a href=\"/u/kn0thing\"&gt;/u/kn0thing&lt;/a&gt; how about implementing ways to prevent Reddit from being used as a tool against what you hold dear? Such as allowing sub-reddits (or individual users) to create a minimum barrier of entry filter for posts or comments. Filter factors could be age of account, percentage of link posts vs comment posts, etc. This would go a long way towards combating new accounts set up to post bias articles and troll in various sub-reddits.  &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "blog",
#                     "name": "t1_dd4ayee",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1485846559.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/blog/comments/5r43td/an_open_letter_to_the_reddit_community/",
#                     "created_utc": 1485817759.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "restricted",
#                     "ups": 1
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2cneq",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5qcnlp",
#                     "link_author": "alchemyi",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dcy7a7z",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 3,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5qcnlp",
#                     "subreddit_name_prefixed": "r/politics",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Thank goodness 'the left' isn't defined by the actions of a small number of dumb people. This is only applicable when the dumb people are in charge. ",
#                     "link_title": "Leftist student physically attacks conservatives after botched debate meeting",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Thank goodness &amp;#39;the left&amp;#39; isn&amp;#39;t defined by the actions of a small number of dumb people. This is only applicable when the dumb people are in charge. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "politics",
#                     "name": "t1_dcy7a7z",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1485494290.0,
#                     "author_flair_text": null,
#                     "link_url": "http://www.thecollegefix.com/post/30907/",
#                     "created_utc": 1485465490.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 3
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2qyt6",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5pay4o",
#                     "link_author": "speckz",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dcpybv9",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 58,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_dcpw4k1",
#                     "subreddit_name_prefixed": "r/TrueReddit",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Few believe sexual assault is okay.\n\nA larger number redefine or excuse sexual assault as a lesser action thereby accepting it. ",
#                     "link_title": "Man Boasts Of Sexual Assault, Later Inaugurated 45th President Of United States",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Few believe sexual assault is okay.&lt;/p&gt;\n\n&lt;p&gt;A larger number redefine or excuse sexual assault as a lesser action thereby accepting it. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "TrueReddit",
#                     "name": "t1_dcpybv9",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1485050897.0,
#                     "author_flair_text": null,
#                     "link_url": "http://www.forbes.com/sites/tarahaelle/2017/01/20/man-commits-sexual-assault-later-inaugurated-45th-president-of-united-states/#482ef1876310",
#                     "created_utc": 1485022097.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 58
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ndpn5",
#                     "link_author": "approachingreality",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dcan357",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 14,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5ndpn5",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Organized religion has more bad effects on society then good and should be criticized appropriately. ",
#                     "link_title": "Why do atheists have such a strong desire to spread their beliefs like missionaries?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Organized religion has more bad effects on society then good and should be criticized appropriately. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_dcan357",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1484187010.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/5ndpn5/why_do_atheists_have_such_a_strong_desire_to/",
#                     "created_utc": 1484158210.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 14
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2cneq",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ncx10",
#                     "link_author": "likeafox",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dcahd5b",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 2,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5ncx10",
#                     "subreddit_name_prefixed": "r/politics",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "The Poles saw a similar movement in 1939.",
#                     "link_title": "Discussion: President Election Trump Press Conference, 1-11-2017",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;The Poles saw a similar movement in 1939.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "politics",
#                     "name": "t1_dcahd5b",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1484180812.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/politics/comments/5ncx10/discussion_president_election_trump_press/",
#                     "created_utc": 1484152012.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 2
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2qh2p",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5mzl9f",
#                     "link_author": "BoJackdHorseman",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dc7lx9f",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 1,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5mzl9f",
#                     "subreddit_name_prefixed": "r/atheism",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Why are you doing this in an atheist forum?",
#                     "link_title": "So I wrote a post yesterday about /r/atheism reading the Bible in a year. Here's my plan",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Why are you doing this in an atheist forum?&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "atheism",
#                     "name": "t1_dc7lx9f",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1484021922.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/atheism/comments/5mzl9f/so_i_wrote_a_post_yesterday_about_ratheism/",
#                     "created_utc": 1483993122.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 1
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2soy6",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5mzv93",
#                     "link_author": "BoJackdHorseman",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dc7l0qa",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 1,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5mzv93",
#                     "subreddit_name_prefixed": "r/TrueAtheism",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Why are you doing this in an atheist forum?",
#                     "link_title": "Hello /r/TrueAtheism, I'm trying to get a Bible reading started in /r/atheism",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Why are you doing this in an atheist forum?&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "TrueAtheism",
#                     "name": "t1_dc7l0qa",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1484020906.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/TrueAtheism/comments/5mzv93/hello_rtrueatheism_im_trying_to_get_a_bible/",
#                     "created_utc": 1483992106.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 1
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2r0za",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ljbr1",
#                     "link_author": "Name2522",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dc2vf94",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 1,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_dc2ueg6",
#                     "subreddit_name_prefixed": "r/simpleliving",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "I'll accept that.",
#                     "link_title": "I'm giving myself a panic attack trying to plan my move to a guesthouse",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;I&amp;#39;ll accept that.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "simpleliving",
#                     "name": "t1_dc2vf94",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1483747538.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/simpleliving/comments/5ljbr1/im_giving_myself_a_panic_attack_trying_to_plan_my/",
#                     "created_utc": 1483718738.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 1
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2snuc",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ljgau",
#                     "link_author": "F2I7W",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dbw77kp",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 8,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_dbw761v",
#                     "subreddit_name_prefixed": "r/DebateReligion",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "But there are. Many. Why speculate about a situation that isn't.",
#                     "link_title": "Why is it that the \"most stringent\" atheists were also believers of God in the past?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;But there are. Many. Why speculate about a situation that isn&amp;#39;t.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateReligion",
#                     "name": "t1_dbw77kp",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1483363241.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateReligion/comments/5ljgau/why_is_it_that_the_most_stringent_atheists_were/",
#                     "created_utc": 1483334441.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 8
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2snuc",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ljgau",
#                     "link_author": "F2I7W",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dbw6igw",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 12,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5ljgau",
#                     "subreddit_name_prefixed": "r/DebateReligion",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Alternate theory: As theists they read the Bible (or other appropriate holy book) and couldn't rationalize the contradictions and other errors contained within it.",
#                     "link_title": "Why is it that the \"most stringent\" atheists were also believers of God in the past?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Alternate theory: As theists they read the Bible (or other appropriate holy book) and couldn&amp;#39;t rationalize the contradictions and other errors contained within it.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateReligion",
#                     "name": "t1_dbw6igw",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1483362049.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateReligion/comments/5ljgau/why_is_it_that_the_most_stringent_atheists_were/",
#                     "created_utc": 1483333249.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 12
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2r0za",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5ljbr1",
#                     "link_author": "Name2522",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dbw5hwx",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 32,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5ljbr1",
#                     "subreddit_name_prefixed": "r/simpleliving",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "[How to sew on a button](https://www.google.ca/search?q=how+to+sew+on+a+button&amp;ie=utf-8&amp;oe=utf-8&amp;client=ubuntu&amp;channel=fs&amp;gfe_rd=cr&amp;ei=xddpWLJawYLxB_CSkKgK&amp;gws_rd=ssl).\n\n[How to take care of a suit](https://www.google.ca/search?q=how+to+take+care+of+a+suit&amp;ie=utf-8&amp;oe=utf-8&amp;client=ubuntu&amp;channel=fs&amp;gfe_rd=cr&amp;ei=y9dpWM_8JMGC8QfwkpCoCg&amp;gws_rd=ssl).\n\n[How to cook](https://www.google.ca/search?q=how+to+cook&amp;ie=utf-8&amp;oe=utf-8&amp;client=ubuntu&amp;channel=fs&amp;gfe_rd=cr&amp;ei=09dpWLHPBcGC8QfwkpCoCg&amp;gws_rd=ssl).\n\nEtc. It's likely someone else has had the same problem and has already provided an answer.",
#                     "link_title": "I'm giving myself a panic attack trying to plan my move to a guesthouse",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;&lt;a href=\"https://www.google.ca/search?q=how+to+sew+on+a+button&amp;amp;ie=utf-8&amp;amp;oe=utf-8&amp;amp;client=ubuntu&amp;amp;channel=fs&amp;amp;gfe_rd=cr&amp;amp;ei=xddpWLJawYLxB_CSkKgK&amp;amp;gws_rd=ssl\"&gt;How to sew on a button&lt;/a&gt;.&lt;/p&gt;\n\n&lt;p&gt;&lt;a href=\"https://www.google.ca/search?q=how+to+take+care+of+a+suit&amp;amp;ie=utf-8&amp;amp;oe=utf-8&amp;amp;client=ubuntu&amp;amp;channel=fs&amp;amp;gfe_rd=cr&amp;amp;ei=y9dpWM_8JMGC8QfwkpCoCg&amp;amp;gws_rd=ssl\"&gt;How to take care of a suit&lt;/a&gt;.&lt;/p&gt;\n\n&lt;p&gt;&lt;a href=\"https://www.google.ca/search?q=how+to+cook&amp;amp;ie=utf-8&amp;amp;oe=utf-8&amp;amp;client=ubuntu&amp;amp;channel=fs&amp;amp;gfe_rd=cr&amp;amp;ei=09dpWLHPBcGC8QfwkpCoCg&amp;amp;gws_rd=ssl\"&gt;How to cook&lt;/a&gt;.&lt;/p&gt;\n\n&lt;p&gt;Etc. It&amp;#39;s likely someone else has had the same problem and has already provided an answer.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "simpleliving",
#                     "name": "t1_dbw5hwx",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1483360498.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/simpleliving/comments/5ljbr1/im_giving_myself_a_panic_attack_trying_to_plan_my/",
#                     "created_utc": 1483331698.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 32
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5lg7t1",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "dbvet0m",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 2,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5lg7t1",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "To a being that I don't think exists? No.",
#                     "link_title": "If you knew you were going to die in a certain situation, would you reach out to God?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;To a being that I don&amp;#39;t think exists? No.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_dbvet0m",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1483323099.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/5lg7t1/if_you_knew_you_were_going_to_die_in_a_certain/",
#                     "created_utc": 1483294299.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 2
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2soy6",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5hxpxs",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "db3sfp1",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 20,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_db3salj",
#                     "subreddit_name_prefixed": "r/TrueAtheism",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "I'm an atheist and an anti-theist. Your claim that anti-theism is about removal not reform doesn't match my view of anti-theism. Maybe you should stop projecting your views of anti-theism onto anti-theists?",
#                     "link_title": "How does Atheism become Anti-theism?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;I&amp;#39;m an atheist and an anti-theist. Your claim that anti-theism is about removal not reform doesn&amp;#39;t match my view of anti-theism. Maybe you should stop projecting your views of anti-theism onto anti-theists?&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "TrueAtheism",
#                     "name": "t1_db3sfp1",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1481593084.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/TrueAtheism/comments/5hxpxs/how_does_atheism_become_antitheism/",
#                     "created_utc": 1481564284.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 20
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2soy6",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5hxpxs",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "db3s744",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 14,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_db3rblg",
#                     "subreddit_name_prefixed": "r/TrueAtheism",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "All anti-theists aren't the same. Some (a minority at the extremes) will be as vitriolic as you suggest. However most anti-theists have sound and valid criticisms of religion and its practices. Voicing these criticisms isn't hatred but a starting point to identifying and changing those practices. ",
#                     "link_title": "How does Atheism become Anti-theism?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;All anti-theists aren&amp;#39;t the same. Some (a minority at the extremes) will be as vitriolic as you suggest. However most anti-theists have sound and valid criticisms of religion and its practices. Voicing these criticisms isn&amp;#39;t hatred but a starting point to identifying and changing those practices. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "TrueAtheism",
#                     "name": "t1_db3s744",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1481592802.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/TrueAtheism/comments/5hxpxs/how_does_atheism_become_antitheism/",
#                     "created_utc": 1481564002.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 14
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2soy6",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5hxpxs",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "db3qvsy",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 115,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5hxpxs",
#                     "subreddit_name_prefixed": "r/TrueAtheism",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Atheism becomes anti-theism due to the observable harmful effects religion has on society.",
#                     "link_title": "How does Atheism become Anti-theism?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Atheism becomes anti-theism due to the observable harmful effects religion has on society.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "TrueAtheism",
#                     "name": "t1_db3qvsy",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1481591223.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/TrueAtheism/comments/5hxpxs/how_does_atheism_become_antitheism/",
#                     "created_utc": 1481562423.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 115
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_38unr",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5bdfvs",
#                     "link_author": "SkywardSword20",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d9nqkco",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 0,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5bdfvs",
#                     "subreddit_name_prefixed": "r/The_Donald",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "This wasn't an assassination attempt.",
#                     "link_title": "Trump continues rally after a credible assassination attempt .Hillary cut her rally to 7 minutes because of RAIN.VOTE THIS MADMAN IN AMERICA",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;This wasn&amp;#39;t an assassination attempt.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "The_Donald",
#                     "name": "t1_d9nqkco",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1478431542.0,
#                     "author_flair_text": null,
#                     "link_url": "https://twitter.com/CBSNews/status/795071257943404544",
#                     "created_utc": 1478402742.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 0
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5a72cd",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d9e4yhp",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 1,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5a72cd",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "The purpose an individual finds for their life is valuable to them. \n\nChildren dying is a horror because we have empathy and could imagine the same happening to others.\n\nSome theists considering a life without God as worthless. Some atheists consider a life with god as wasted.",
#                     "link_title": "Do you believe life has objective value absent god?",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;The purpose an individual finds for their life is valuable to them. &lt;/p&gt;\n\n&lt;p&gt;Children dying is a horror because we have empathy and could imagine the same happening to others.&lt;/p&gt;\n\n&lt;p&gt;Some theists considering a life without God as worthless. Some atheists consider a life with god as wasted.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d9e4yhp",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1477877203.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/5a72cd/do_you_believe_life_has_objective_value_absent_god/",
#                     "created_utc": 1477848403.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 1
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5a1qbc",
#                     "link_author": "OliviaMark",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d9d2m1f",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 16,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_d9d2jo9",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Your reply isn't evidence FOR your ability to rationally debate. ",
#                     "link_title": "Its time for a new debate. WARNING... THIS IS A TRICK... that means, do not fall for what i'm going to post because its to get you to go by your knee jerk reaction and use some sound thinking. Good luck, you've been warned.. Please, I pray to the laws of probability, let someone get this.",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Your reply isn&amp;#39;t evidence FOR your ability to rationally debate. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d9d2m1f",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1477798138.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/5a1qbc/its_time_for_a_new_debate_warning_this_is_a_trick/",
#                     "created_utc": 1477769338.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 16
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_5a1qbc",
#                     "link_author": "OliviaMark",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d9d2gp9",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 18,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_5a1qbc",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "/u/OliviaMark based on your replies in this thread I don't think you can rationally debate.",
#                     "link_title": "Its time for a new debate. WARNING... THIS IS A TRICK... that means, do not fall for what i'm going to post because its to get you to go by your knee jerk reaction and use some sound thinking. Good luck, you've been warned.. Please, I pray to the laws of probability, let someone get this.",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;&lt;a href=\"/u/OliviaMark\"&gt;/u/OliviaMark&lt;/a&gt; based on your replies in this thread I don&amp;#39;t think you can rationally debate.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d9d2gp9",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1477797909.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/5a1qbc/its_time_for_a_new_debate_warning_this_is_a_trick/",
#                     "created_utc": 1477769109.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 18
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_561j9k",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d8ftxrz",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 5,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_d8fnjqn",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Your dishonesty is obvious and noted.",
#                     "link_title": "What I've learned from posting here under two accounts",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Your dishonesty is obvious and noted.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d8ftxrz",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1475744269.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/561j9k/what_ive_learned_from_posting_here_under_two/",
#                     "created_utc": 1475715469.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 5
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_561j9k",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d8fn92g",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 13,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_d8fn1j4",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Your dishonesty is obvious and noted.",
#                     "link_title": "What I've learned from posting here under two accounts",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Your dishonesty is obvious and noted.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d8fn92g",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1475734367.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/561j9k/what_ive_learned_from_posting_here_under_two/",
#                     "created_utc": 1475705567.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 13
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": false,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_561j9k",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d8fmcpy",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 15,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t1_d8flzs5",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "Your failure to provide evidence and back up your claim is noted. RES 'dishonest' tag added to your account.",
#                     "link_title": "What I've learned from posting here under two accounts",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Your failure to provide evidence and back up your claim is noted. RES &amp;#39;dishonest&amp;#39; tag added to your account.&lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d8fmcpy",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1475733125.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/561j9k/what_ive_learned_from_posting_here_under_two/",
#                     "created_utc": 1475704325.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 15
#                 }
#             },
#             {
#                 "kind": "t1",
#                 "data": {
#                     "subreddit_id": "t5_2ryfy",
#                     "edited": 1475757561.0,
#                     "banned_by": null,
#                     "removal_reason": null,
#                     "link_id": "t3_561j9k",
#                     "link_author": "[deleted]",
#                     "likes": null,
#                     "replies": "",
#                     "user_reports": [ ],
#                     "saved": false,
#                     "id": "d8fi1ll",
#                     "gilded": 0,
#                     "archived": false,
#                     "score": 6,
#                     "report_reasons": null,
#                     "author": "stp2007",
#                     "parent_id": "t3_561j9k",
#                     "subreddit_name_prefixed": "r/DebateAnAtheist",
#                     "approved_by": null,
#                     "over_18": false,
#                     "controversiality": 0,
#                     "body": "If your claim has merit post the other \"atheist\" account so others can compare the two.\n\nEdit: Adding OP's name for future reference (/u/MyIQhigherthanU) after they deleted their posts in this thread. More dishonesty there. ",
#                     "link_title": "What I've learned from posting here under two accounts",
#                     "author_flair_css_class": null,
#                     "downs": 0,
#                     "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;If your claim has merit post the other &amp;quot;atheist&amp;quot; account so others can compare the two.&lt;/p&gt;\n\n&lt;p&gt;Edit: Adding OP&amp;#39;s name for future reference (&lt;a href=\"/u/MyIQhigherthanU\"&gt;/u/MyIQhigherthanU&lt;/a&gt;) after they deleted their posts in this thread. More dishonesty there. &lt;/p&gt;\n&lt;/div&gt;",
#                     "quarantine": false,
#                     "subreddit": "DebateAnAtheist",
#                     "name": "t1_d8fi1ll",
#                     "score_hidden": false,
#                     "num_reports": null,
#                     "stickied": false,
#                     "created": 1475727638.0,
#                     "author_flair_text": null,
#                     "link_url": "https://www.reddit.com/r/DebateAnAtheist/comments/561j9k/what_ive_learned_from_posting_here_under_two/",
#                     "created_utc": 1475698838.0,
#                     "distinguished": null,
#                     "mod_reports": [ ],
#                     "subreddit_type": "public",
#                     "ups": 6
#                 }
#             }
#         ],
#         "after": "t1_d8fi1ll",
#         "before": null
#     }
# 
# }    