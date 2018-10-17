# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# NewsStory
class NewsStory(object):
    def __init__(self,guid,title,description,link,pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# PhraseTrigger
class PharseTrigger(Trigger):
    def __init__(self,pharse):
        self.pharse=pharse.lower()

    def get_pharse(self):
        return self.pharse

    def is_pharse_in(self,text):
        text=text.lower()
        text_space=""
        text_split=[]
        for each in text:
            if each not in string.ascii_letters:
                text_space+=" "
            else:
                text_space+=each
        text_split=text_space.split(" ")
        while '' in text_split:
            text_split.remove('')
        text_length=len(text_split)
        pharse_list=self.get_pharse().split(" ")
        pharse_length=len(pharse_list)
        for i in range(text_length-pharse_length+1):
            match_times=0
            for j in range(pharse_length):
                if pharse_list[j]==text_split[i+j]:
                    match_times+=1
                if match_times==pharse_length:
                    return True
            match_times=0
        return False
# Problem 3
# TitleTrigger
class TitleTrigger(PharseTrigger):

    def evaluate(self,story):
        return self.is_pharse_in(story.get_title())
# Problem 4
# DescriptionTrigger
class DescriptionTrigger(PharseTrigger):

    def evaluate(self,story):
        return self.is_pharse_in(story.get_description())
# TIME TRIGGERS

# Problem 5
# TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):

    def __init__(self,EST):
        self.time=datetime.strptime(EST,"%d %b %Y %H:%M:%S")

# Problem 6
# BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):

    def evaluate(self,story):
        if self.time>story.get_pubdate().replace(tzinfo=None):
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):

    def evaluate(self,story):
        if self.time<story.get_pubdate().replace(tzinfo=None):
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
# NotTrigger
class NotTrigger(Trigger):
    def __init__(self,another_trigger):
        self.trigger=another_trigger

    def evaluate(self,story):
        return not self.trigger.evaluate(story)

# Problem 8
# AndTrigger
class AndTrigger(Trigger):
    def __init__(self,one_trigger,another_trigger):
        self.one_trigger=one_trigger
        self.another_trigger=another_trigger

    def evaluate(self,story):
        return self.one_trigger.evaluate(story) and self.another_trigger.evaluate(story)

# Problem 9
# OrTrigger
class OrTrigger(Trigger):
    def __init__(self,one_trigger,another_trigger):
        self.one_trigger=one_trigger
        self.another_trigger=another_trigger

    def evaluate(self,story):
        return self.one_trigger.evaluate(story) or self.another_trigger.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return_list=[]
    for each_trigger in triggerlist:
        for each_story in stories:
            if each_trigger.evaluate(each_story):
                return_list.append(each_story)
    return_list=list(set(return_list))
    return return_list



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    triggers=[]
    trigger_dict={}
    for each_line in lines:
        line_split=line.split(",")
        if line_split[0]=="ADD":
            for i in range(1,len(line_split)):
                triggers.append(trigger_dict[line_split[i]])
        else:
            trigger_name=line_split[0]
            if line[1]=="TITLE":
                trigger_dict[trigger_name]=TitleTrigger(line_split[2])
            elif line[1]=="DESCRIPTION":
                trigger_dict[trigger_name]=DescriptionTrigger(line_split[2])
            elif line[1]=="AND":
                trigger_dict[trigger_name]=AndTrigger(trigger_dict[line_split[2]],trigger_dict[line_split[3]])
            elif line[1]=="NOT":
                trigger_dict[trigger_name]=NotTrigger(trigger_dict[line_split[2]])
            elif line[1]=="OR":
                trigger_dict[trigger_name]=OrTrigger(trigger_dict[line_split[2]],trigger_dict[line_split[3]])
            elif line[1]=="AFTER":
                trigger_dict[trigger_name]=AfterTrigger(line_split[2])
            elif line[1]=="BEFORE":
                trigger_dict[trigger_name]=BeforeTrigger(line_split[2])
            else:
                pass

    print(lines) # for now, print it so you see what it contains!
    return triggers



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
