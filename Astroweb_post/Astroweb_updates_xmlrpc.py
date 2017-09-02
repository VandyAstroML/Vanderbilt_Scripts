#!/usr/bin/env python

"""
This script is for automatically updating the 'Events' section on the Vanderbilt
Astronomy Group wordpress site.

'Events' section contains the latest post in the category 'Events', so updating
the section is the same as adding new posts with the category set to 'Events'.

This script use python module 'xmlrpclib' to communicate the XML-RPC protocol of
wordpress. Please make sure the XML-RPC option is on in the wordpress setting.
You can find it at 'Settings - Writing - Remote Publishing - XML-RPC'.

Python module 'datetime' is used to get the time and date, then the script
decides which notices to send based on the date.

Each kind of notice has a individual function. You can edit the contents as
needed. 

This script is supposed to be used together with crontab. Set the crontab with
great care to automatically run this scrip. 

!!Please set the permission of this script to be readable only by the owner (700),
because the wordpress editor's password is in plain text in the script!!

"""



import string, datetime, time, xmlrpclib, sys, os

# get date and time
now = datetime.datetime.now()

# format date and time as needed
weekday = now.strftime("%a")
month = now.strftime("%b")
day = now.strftime("%d")


#-----------------------------------------------------------------------------#
def sendpost(blog_content):
    """
    Use XML-RPC protocol to post to the Astro wordpress site.
    Use python module xmlrpclib to communicate with wordpress XML-RPC.  
    """
    
    # wordpress url and accout
    wp_url      = "https://as.vanderbilt.edu/astronomy/manage/xmlrpc.php"
    wp_username = os.environ['wp_username']
    wp_password = os.environ['wp_password']

    wp_blogid = "" # wordpress doesn't use this id, so it can be anything. 

    status_draft = 0
    status_published = 1
    
    server = xmlrpclib.ServerProxy(wp_url)


    post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password,
                                        blog_content, status_published)

#-----------------------------------------------------------------------------#
def sendAstroLunchNotice():

    title = ("AstroLunch, "
             + weekday + ". " + month + "." + day
             + " at noon, SC 6333"
             )

    content = string.join((
        'AstroLunch meets every Tuesday at noon in Stevenson Center 6333. ', 
        '<a href="http://vanderbiltastro.pbworks.com/w/page/12546270/AstroLunch"> Check here for the schedule.</a>'
        ), "\r\n")

    categories = ["Events"]

    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)

#-----------------------------------------------------------------------------#
def sendAJCNotice():

    title = ("Astronomy Journal Club, "
             + weekday + ". " + month + "." + day
             + " at noon, SC 6333"
             )

    content = string.join((
        'Astronomy Journal Club meets every Wednesday at noon in Stevenson Center 6333. ', 
        '<a href="http://as.vanderbilt.edu/astronomy/category/journal-club/"> Check here for the full schedule.</a>'
        ), "\r\n")

    categories = ["Events"]


    #######################################
    # This part use the ajc.cron file to automatically put updated info of AJC into the blog.
    # If it gets weird, feel free to comment out or delete the whole part between "#####"
    filename = "/home/maoq/www/astro/ajc.cron"

    if os.path.isfile(filename): # check if the file exists
        # get the time difference between the last modified time and now, in hours
        timediff = (time.time() - os.path.getmtime(filename)) / 60 / 60
        # only do this if the file was edited less than 6 days ago
        if timediff < 24*6: 
            # read the ajc.cron file and get this week's content
            file = open(filename, "r")
            tmpstr = file.readlines()[1:12]
            new_content = string.join(tmpstr) 
            content = new_content + content
    ###########################################
    
    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)
    

#-----------------------------------------------------------------------------# 
def sendVinoNotice():

    title = ("Vino de Vida, "
             + weekday + ". " + month + "." + day
             + " at 4pm, 9th floor hallway"
             )

    content = string.join((
        'Vino da Vida happens every Friday at 4pm in the 9th floor hallway. ', 
        'We have casual discussion over a glass of wine, beer, or soda to unwind and celebrate the end of the week.'
        ), "\r\n")

    categories = ["Events"]
    
    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)

#-----------------------------------------------------------------------------#
def sendAstroRWNotice():

    title = ("AstroRW, "
             + weekday + ". " + month + "." + day
             + " at 2pm, SC Library"
             )

    content = string.join((
            'Once a week, we meet in the study room SC3210, and read/write papers for one hour. \n', 
            'This is a time for us to get together and do the reading and writing of papers that are often "deprioritized" if left to one\'s own devices at their desk. Collectively, we can focus and get ourselves over whatever "hump" lies in from of us. Note that there will be NO presentations; you read/write the material you bring to yourself. '
            ), '\r\n')

    categories = ["Events"]

    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)
#-----------------------------------------------------------------------------#
def sendAstroBrewNotice():

    title = ("AstroBrew, "
             + weekday + ". " + month + "." + day
             + " at 11am, 9th floor conference room"
             )

    content = string.join((
            "AstroBrew is a variant of the AstroCoffee related meetings that the department has had in the past.\n", 
            "The guideline of the AstroBrew are:\n1) 30 min. Maximum.\n2) Agenda is clear: 2-3 papers will be discussed.\n",
            "3) Initially, each paper will be presented by a postdoc. ", 
            "Soon, we will open up opportunities for Graduate Students once the meeting has momentum.\n", 
            "4) The goal here is simple: maximum information dissemination. The short talks will be 10-15 min presentations of interesting papers.\n", 
            "5) Conversation will be kept on topic. We will get through the main points of the paper quickly.\n6) We will cover a variety of topics.\n"
            ), "\r\n")

    categories = ["Events"]

    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)
#-----------------------------------------------------------------------------#
def sendAstroChatNotice():

    title = ("AstroChat, "
             + weekday + ". " + month + "." + day
             + " at 11am, 9th floor conference room"
             )

    content = string.join((
        'AstroChat meets weekly on Friday at 11am in the 9th floor conference room. \n', 
        'AstroChat is tailored to the grad students, especially junior grad students.  We can come together and chat about the things we learned that week in the other Astro-events. Feel free to bring any question you may have about astronomy and the business of doing astronomy research.  We most likely will not answer every question during AstroChat, but instead we will point you towards someone with whom you can discuss your question offline.\n',
        'There will be 10min slots available for you to practice presenting a paper you may be thinking of giving to a larger audience at AstroLunch, AJC, or AstroBrew.  Announcements of particular milestones/achievements (no matter how small) in your research or coursework are welcome. Any problems you run into in said areas can be brought up and we can reason together about how to begin to address them.\n', 
        'In short, this will be a very friendly environment where we are all open about our areas of expertise as well as our areas of ignorance, and thus, no one needs to be shy about not knowing something. The goal is to keep you inspired and motivated as you find yourself trudging through some of the more tedious and perhaps de-moralizing aspects of publishing awesome research!\n'
        ), "\r\n")
    
    categories = ["Events"]

    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)
#-----------------------------------------------------------------------------#
def sendSpecialNotice():

    title = ("Special Talk by , "
             + weekday + ". " + month + "." + day
             + " at 11am, SC6501"
             )

    content = string.join(" ", "\r\n\n")

    categories = ["Events"]
    
    blog_content = {'title': title, 'description': content, 'categories': categories}

    sendpost(blog_content)

#-----------------------------------------------------------------------------#
def main():


    # Special Events, edit the dates here, and edit the content in the
    # function sendSpecialNotice()
    # Caution! Use double digits for the day, e.g. '05' for 5th.
    #if month == 'Nov' and day == '05':
    #    sendSpecialNotice()
    #    sys.stderr.write("%s\t Special Event posted. :D\n"
    #                     % now.strftime("%x %a %X"))
    

    # quit for the Spring Break
    #if month == 'Mar' and day in ['02', '03', '04', '05', '06']:
    #    sys.stderr.write("%s\t Spring break. No post today. :|\n"
    #                     % now.strftime("%x %a %X"))
    #    sys.exit(0)

    # quit for Thanksgiving
    # if month == 'Nov' and day in ['24', '25', '26', '27', '28']:
    #     sys.stderr.write("%s\t Thanksgiving Break. No post today. :|\n"
    #                      % now.strftime("%x %a %X"))
    #     sys.exit(0)


    # use weekday to decide which notices to send 
    if weekday == 'Mon':
        #sendAstroRWNotice()
        sys.stderr.write("%s\t Successfully posted. :D\n"
                         % now.strftime("%x %a %X"))
    elif weekday == 'Tue':
        sendAstroLunchNotice()
        sys.stderr.write("%s\t Successfully posted. :D\n"
                         % now.strftime("%x %a %X"))
    elif weekday == 'Wed':
        sendAJCNotice()
        sys.stderr.write("%s\t Successfully posted. :D\n"
                         % now.strftime("%x %a %X"))
    elif weekday == 'Thu':
        sendAstroBrewNotice()
        sys.stderr.write("%s\t Successfully posted. :D\n"
                         % now.strftime("%x %a %X"))
    elif weekday == 'Fri':
        #sendAstroChatNotice()
        sendVinoNotice()
        sys.stderr.write("%s\t Successfully posted. :D\n"
                         % now.strftime("%x %a %X"))
    else:
        sys.stderr.write("%s\t Successfully ran but no post today. :|\n"
                         % now.strftime("%x %a %X"))


    
if __name__ == '__main__':
    main()


        



### --- Archived notices --- ####################################################

# #-----------------------------------------------------------------------------#
# def sendAstroChatsMonNotice():

#     title = ("AstroChats, "
#              + weekday + ". " + month + "." + day
#              + " at 3pm, 9th floor conference room"
#              )

#     content = string.join((
#         'AstroChats meets Monday at 3pm and Thursday at 11am in the 9th floor conference room. ', 
#         '<a href="http://vanderbiltastro.pbworks.com/w/page/57836824/AstroChats"> Check here for the schedule.</a>'
#         ), "\r\n")
    
#     categories = ["Events"]

#     blog_content = {'title': title, 'description': content, 'categories': categories}

#     sendpost(blog_content)

# #-----------------------------------------------------------------------------#
# def sendAstroChatsThuNotice():

#     title = ("AstroChats, "
#              + weekday + ". " + month + "." + day
#              + " at 11am, 9th floor conference room"
#              )

#     content = string.join((
#         'AstroChats meets Monday at 3pm and Thursday at 11am in the 9th floor conference room. ', 
#         '<a href="http://vanderbiltastro.pbworks.com/w/page/57836824/AstroChats"> Check here for the schedule.</a>'
#         ), "\r\n")
    
#     categories = ["Events"]

#     blog_content = {'title': title, 'description': content, 'categories': categories}

#     sendpost(blog_content)

