#!/usr/bin/env python

"""
This script is for automatically updating the 'Events' section on the Vanderbilt
Astronomy Group wordpress site.

'Events' section contains the latest post in the category 'Events', so updating
the section is the same as adding new posts with the category set to 'Events'.

This script use python module 'xmlrpc' to communicate the XML-RPC protocol of
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
import string
import datetime
import time
import xmlrpc.client as client
import xmlrpc
import sys
import os

## Functions
def now_dict_calc():
    """
    Produces python dictionary with datetime information
    
    Returns
    --------
    now_dict: python dictionary
        dictionary with datetime information
        Keys: 'weekday', 'month', 'day', 'now', 'now_str'
    """
    # Get date and time
    now = datetime.datetime.now()
    # Format date and time as needed
    weekday = now.strftime("%a")
    month   = now.strftime("%b")
    day     = now.strftime("%d")
    now_str = now.strftime("%x %a %X")
    # Converting to dictionary
    now_dict = {'weekday':weekday, 'month':month, 'day':day, 'now_str':now_str,
                'now':now}

    return now_dict

def assert_env_vars():
    """
    Asserts that the existence of the necessary environment variables
    """
    try:
        wp_username = os.environ['wp_username']
        wp_password = os.environ['wp_username']
    except KeyError:
        msg = '>> `Keyerror`'
        raise ValueError(msg)

def sendpost(blog_content):
    """
    Use XML-RPC protocol to post to the Astro wordpress site.
    Use python module xmlrpc to communicate with wordpress XML-RPC.  
    """
    # Verifying environment keys
    assert_env_vars()
    # Wordpress URL and Account
    wp_url      = "https://as.vanderbilt.edu/astronomy/manage/xmlrpc.php"
    wp_username = os.environ['wp_username']
    wp_password = os.environ['wp_password']
    # Blog ID - Wordpress doesn't use this ID, so it can be anything
    wp_blogid = ""
    # Status
    status_draft = 0
    status_published = 1
    # Initializing server

    server = client.ServerProxy(wp_url)
    # Posing to Wordpress
    post_id = server.metaWeblog.newPost(wp_blogid,
                                        wp_username,
                                        wp_password,
                                        blog_content,
                                        status_published)

def sendAstroLunchNotice(now_dict):
    """
    Sends notice about `AstroLunch`

    Parameters
    ----------
    now_dict: python dictionary
        dictionary with datetime information
        Keys: 'weekday', 'month', 'day', 'now', 'now_str'
    """
    # Blog - Title
    title = 'AstroLunch, {0}. {1}. {2} at noon, sc 6333'.format(
                    now_dict['weekday'],
                    now_dict['month'],
                    now_dict['day'])
    # Blog - Content
    content = "\r\n".join((
        'AstroLunch meets every Tuesday at noon in Stevenson Center 6333. ', 
        '<a href="http://vanderbiltastro.pbworks.com/w/page/12546270/AstroLunch"> Check here for the schedule.</a>'
        ))
    # content = string.join((
    #     'AstroLunch meets every Tuesday at noon in Stevenson Center 6333. ', 
    #     '<a href="http://vanderbiltastro.pbworks.com/w/page/12546270/AstroLunch"> Check here for the schedule.</a>'
    #     ), "\r\n")
    # Blog - Details
    categories = ["Events"]
    blog_content = {'title': title, 'description': content, 'categories': categories}
    # Posting Post
    sendpost(blog_content)

def sendAJCNotice(now_dict):
    """
    Sends notice about `Astronomy Journal Club`

    Parameters
    ----------
    now_dict: python dictionary
        dictionary with datetime information
        Keys: 'weekday', 'month', 'day', 'now', 'now_str'
    """
    # Blog - Title
    title = 'Astronomy Journal Club, {0}. {1}. {2} at noon, SC 6333'.format(
                    now_dict['weekday'],
                    now_dict['month'],
                    now_dict['day'])
    # Blog - Content
    content = "\r\n".join((
        'Astronomy Journal Club meets every Wednesday at noon in Stevenson Center 6333. ', 
        '<a href="http://as.vanderbilt.edu/astronomy/category/journal-club/"> Check here for the full schedule.</a>'
        ))
    # Blog - Details
    categories   = ["Events"]
    blog_content = {'title': title, 'description': content, 'categories': categories}
    # Posting Post
    sendpost(blog_content)

def sendAstroBrewNotice(now_dict):
    """
    Sends notice about `AstroBrew`

    Parameters
    ----------
    now_dict: python dictionary
        dictionary with datetime information
        Keys: 'weekday', 'month', 'day', 'now', 'now_str'
    """
    # Blog - Title
    title = 'AstroBrew, {0}. {1}. {2} at 11am, SC 6333'.format(
                    now_dict['weekday'],
                    now_dict['month'],
                    now_dict['day'])
    # Blog - Content
    content = "\r\n".join((
            "AstroBrew is a variant of the AstroCoffee related meetings that the department has had in the past.\n", 
            "The guideline of the AstroBrew are:\n1) 30 min. Maximum.\n2) Agenda is clear: 2-3 papers will be discussed.\n",
            "3) Initially, each paper will be presented by a postdoc. ", 
            "Soon, we will open up opportunities for Graduate Students once the meeting has momentum.\n", 
            "4) The goal here is simple: maximum information dissemination. The short talks will be 10-15 min presentations of interesting papers.\n", 
            "5) Conversation will be kept on topic. We will get through the main points of the paper quickly.\n6) We will cover a variety of topics.\n"
            ))
    # Blog - Details
    categories   = ["Events"]
    blog_content = {'title': title, 'description': content, 'categories': categories}
    # Posting Post
    sendpost(blog_content)

def sendVinoNotice(now_dict):
    """
    Sends notice about `Vino de Vida`

    Parameters
    ----------
    now_dict: python dictionary
        dictionary with datetime information
        Keys: 'weekday', 'month', 'day', 'now', 'now_str'
    """
    # Blog - Title
    title = 'Vino de Vida, {0}. {1}. {2} at 4pm, 9th floor hallway'.format(
                    now_dict['weekday'],
                    now_dict['month'],
                    now_dict['day'])
    # Blog - Content
    content = string.join((
        'Vino da Vida happens every Friday at 4pm in the 9th floor hallway. ', 
        'We have casual discussion over a glass of wine, beer, or soda to unwind and celebrate the end of the week.'
        ), "\r\n")
    # Blog - Details
    categories   = ["Events"]
    blog_content = {'title': title, 'description': content, 'categories': categories}
    # Posting Post
    sendpost(blog_content)

def main():
    """
    Determines current date and sends the expected notice

    """
    ## Defining `now_dict` dictionary
    now_dict = now_dict_calc()
    ## Defining `post` strings
    post_success = '{0}\t Successfully poster. :D\n'.format(now_dict['now_str'])
    post_ran     = '{0}\t Successfully ran but no post today'.format(
                        now_dict['now_str'])
    # Special Holidays
    post_thanksg = '{0}\t Thanksgiving Break. No Post today. :|\n'.format(
                        now_dict['now_str'])
    post_spring  = '{0}\t Spring Break. No Post today. :|\n'.format(
                        now_dict['now_str'])

    ## EDIT THIS ONCE PER YEAR
    thanksg_dates = list(range(20,25))
    spring_dates  = list(range( 5,10))
    # Thanksgiving
    if (now_dict['weekday'] in thanksg_dates) and now_dict['month']=='Nov':
        sys.stderr.write(post_thanksg)
        sys.exit(0)
    # Spring Break
    if (now_dict['weekday'] in spring_dates) and now_dict['month']=='Mar':
        sys.stderr.write(post_spring)
        sys.exit(0)

    ## Defining Weekday and deciding which notice to send
    if now_dict['weekday'] == 'Tue':
        sendAstroLunchNotice(now_dict)
        sys.stderr.write(post_success)
    elif now_dict['weekday'] == 'Wed':
        sendAJCNotice(now_dict)
        sys.stderr.write(post_success)
    elif now_dict['weekday'] == 'Thu':
        sendAstroBrewNotice(now_dict)
        sys.stderr.write(post_success)
    elif now_dict['weekday'] == 'Fri':
        sendVinoNotice(now_dict)
        sys.stderr.write(post_success)
    else:
        sys.stderr.write(post_ran)

if __name__ == '__main__':
    main()

