#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author        : Victor Calderon
# Created       : 2017-09-01
# Last Modified : 2019-10-28
# Affiliation   : Vanderbilt University
from __future__ import print_function, division, absolute_import
__author__     =['Victor Calderon']
__copyright__  =["Copyright 2017 Victor Calderon, "]
__email__      =['victor.calderon@vanderbilt.edu']
__maintainer__ =['Victor Calderon']
"""

"""
# Importing Modules
import numpy as np
import os
import sys
import sys
# sys.setdefaultencoding('utf8')
import pandas as pd

# Extra-modules
import ads
import arxiv
import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Main functions

#### ------------------------- Datetime Extraction ---------------------- #####

def datetime_dict():
    """
    Produces dictionary with necessary time information

    Returns
    -------
    now_dict: `dict`
        dictionary with `year`, `weekday`, `month`, `day` entries
    """
    ## Determining today's date
    now     = datetime.datetime.now()
    year    = now.strftime("%Y")
    weekday = now.strftime("%a")
    month   = now.strftime("%m")
    day     = now.strftime("%d")
    now_dict = {'year':year, 'weekday':weekday, 'month':month, 'day':day}

    return now_dict

def ajc_url_creator(now_dict):
    """
    Creates the `ajc_url` string

    Parameters
    ----------
    now_dict : `dict`
        Dictionary with the information of today's date.

    Parameters
    -----------
    ajc_url : `str`
        URL of the current AJC schedule page.
    """
    # Months in academic semesters
    spring_months = np.arange(1, 6, 1)
    fall_months   = np.arange(8, 13, 1)
    # Months in the academic year, i.e. Fall + Spring semester
    academic_year_arr = np.concatenate((fall_months, spring_months))
    # Determining the URL for the current AJC schedule
    if (int(now_dict['month']) in fall_months):
        fall_year   = int(now_dict['year'])
        spring_year = fall_year + 1
    elif (int(now_dict['month']) in spring_months):
        spring_year = int(now_dict['year'])
        fall_year   = spring_year - 1
    else:
        spring_year = ""
        fall_year   = ""
    # Defaults for semester string
    sem_str = 'fall'
    sem_num = '08'
    # Parsing together AJC URL
    ajc_list = ['https://as.vanderbilt.edu/astronomy']
    ajc_list.append(f"{fall_year}")
    ajc_list.append(f"{sem_num}")
    ajc_list.append(f"journal-club-fall-{fall_year}-spring-{spring_year}")
    ajc_url = '/'.join(ajc_list)
    # Checking URL
    url_checker(ajc_url)

    return ajc_url

def people_info_extractor(people_type='graduate'):
    """
    This function extracts the info for `people_type` from specified URL.

    Parameters
    ------------
    people_type : `str`, optional
        Option for which type of info to extract. This variable is set to
        `graduate` by default.

        Options:
            - 'graduate' : Extracts information about graduate students.
            - 'faculty' : Extracts information about faculty.

    Returns
    -------------
    people_pd : `pandas.DataFrame`
        DataFrame with names and emails of the current students or
        faculty of the Astronomy Department at Vanderbilt University.
    """
    ## Checking info parameters
    # `people_type` - Type
    people_type_type_arr = (str)
    if not isinstance(people_type, people_type_type_arr):
        msg = '>> `people_type` ({0}) is not a valid input type ({0})! Exit!'
        msg = msg.format(type(people_type), people_type_type_arr)
        raise TypeError(msg)
    # `people_type` - Value
    people_type_value_arr = ['graduate', 'faculty']
    if not (people_type in people_type_value_arr):
        msg = '>> `people_type` ({0}) is not a valid input value ({1})! Exit!'
        msg = msg.format(people_type, people_type_value_arr)
        raise ValueError(msg)
    #
    #
    url_base = "https://as.vanderbilt.edu/astronomy/people/"
    people_type_url_dict = {
        'graduate' : '{0}/graduate-students/'.format(url_base),
        'faculty'  : '{0}/faculty'.format(url_base)
    }
    # Checking chosen url
    url_chosen = people_type_url_dict[people_type]
    url_checker(url_chosen)
    # Reading in table
    people_table = pd.read_html(url_chosen)
    # Looping over elements in `people_table`
    for ii, people_ii in enumerate(people_table):
        if (ii == 0):
            people_pd_temp = people_ii[1]
        else:
            people_pd_temp = people_pd_temp.append(people_ii[1],
                ignore_index=True)
    # Dropping NaN's
    people_pd_temp = people_pd_temp.dropna().reset_index(drop=True)
    n_people       = people_pd_temp.shape[0]
    # Parsing fields
    list_st = [[] for x in range(n_people)]
    people_dict = { 'full_name' : list(list_st),
                    'first_name': list(list_st),
                    'last_name' : list(list_st),
                    'email'     : list(list_st)}
    # Populating dictionary
    for ii, elem in enumerate(people_pd_temp):
        elem_split = elem.split()
        people_dict['first_name'][ii] = elem_split[0]
        people_dict['last_name'][ii]  = elem_split[1]
        people_dict['full_name'][ii]  = '_'.join(elem_split[:2][::-1])
        jj = 0
        # Splitting for email
        elem_state = False
        while (elem_state == False):
            for jj, elem_jj in enumerate(elem_split):
                if ('Email:' in elem_jj):
                    elem_state = True
                    zz = jj
        email = elem_split[zz+1].strip()
        people_dict['email'][ii] = email
    # Converting to DataFrame
    people_pd = pd.DataFrame(people_dict)
    people_pd_cols = people_pd.columns.tolist()
    people_pd_cols = people_pd_cols[::-1]
    people_pd = people_pd[people_pd_cols]
    # Sorting by name
    people_pd.sort_values('full_name', inplace=True)
    people_pd.reset_index(inplace=True, drop=True)
    # Making `name` the Index
    people_pd = people_pd.set_index('full_name')
    # Adding columns that indicates type of person
    people_pd.loc[:, 'people_type'] = people_type

    return people_pd

def ajc_parser(ajc_url, reminder_day=2, physajc_day=1):
    """
    Parses the information from `ajc_url`

    Parameters
    ----------
    ajc_url: string
        URL of the current AJC string

    reminder_day: int, optional (default = 2)
        number of days `prior` to AJC to send email reminder to speaker

    physajc_day: int, optional (default = 1)
        number of days `prior` to AJC to send email to PHYS_AJC mailing list.

    Return
    ----------
    ajc_pd: pandas DataFrame
        DataFrame containing info about 1) AJC date, 2) Title, 3) Speaker,
        4) Reminder date, 5) Date to send email to mailing list.
    """
    # Reading URL
    ajc_pd = pd.read_html(ajc_url, header=0)[0]
    # Parsind - Date
    ajc_pd['Date'] = pd.to_datetime(ajc_pd['Date'])
    # Removing Dates with no Speaker
    ajc_pd = ajc_pd.dropna(subset=['Speaker'])
    ajc_pd.reset_index(inplace=True, drop=True)
    n_speakers = ajc_pd.shape[0]
    # Parsing Speaker
    speaker_arr = [[] for x in range(n_speakers)]
    for jj, speaker_jj in enumerate(ajc_pd['Speaker'].values):
        speaker_arr[jj] = '_'.join(speaker_jj.split()[::-1])
    ajc_pd['Speaker'] = speaker_arr
    # Adding Date for Reminders
    ajc_pd['Reminders']  = ajc_pd['Date'] - pd.Timedelta(reminder_day, 'D')
    # Send email dates
    ajc_pd['Send_email'] = ajc_pd['Date'] - pd.Timedelta(physajc_day, 'D')
    # Making Speaker the index
    ajc_pd = ajc_pd.set_index('Speaker')

    return ajc_pd

def ajc_gs_merge(ajc_pd):
    """
    Merges the DataFrames `ajc_pd` and `gs_pd`
    
    Parameters
    ----------
    ajc_pd: pandas DataFrame
        DataFrame with information on the AJC table

    Returns
    --------
    ajd_gs_pd: pandas DataFrame
        merged DataFrame between `ajc_pd` and `gs_pd`
        Keys: `email`, `Date`, `Reminders`.
        Index is set to `firstname_lastname` of student.
    """
    # Graduate Students List
    gs_pd = people_info_extractor('graduate')
    # Faculty
    fac_pd = people_info_extractor('faculty')
    # Joining both DataFrames
    gs_fac_pd = pd.concat([gs_pd, fac_pd])
    # Merging
    ajc_gs_pd = pd.merge(gs_fac_pd, ajc_pd, left_index=True, right_index=True,
        how='right')
    # Sort by Date
    ajc_gs_pd = ajc_gs_pd.sort_values('Date')

    return ajc_gs_pd

def send_email_reminder(ajc_gs_pd, now_dict):
    """
    Sends email reminders 2 days before AJC date to the specified student

    Parameters
    -----------
    ajc_gs_pd: pandas DataFrame
        merged DataFrame between `ajc_pd` and `gs_pd`
        Keys: `email`, `Date`, `Reminders`.
        Index is set to `firstname_lastname` of student.

    now_dict: python dictionary
        dictionary with `year`, `weekday`, `month`, `day` entries
    """
    ## Today's Timestamp
    today_pd = pd.Timestamp('{0}/{1}/{2}'.format(now_dict['month'],
                                                 now_dict['day'],
                                                 now_dict['year']))
    # Checking if today's date is in `ajc_gs_pd`
    today_ajc_pd = ajc_gs_pd.loc[ajc_gs_pd['Reminders'] == today_pd]
    # Checking if there is an 
    if (today_ajc_pd.shape[0] == 1):
        # If email belongs to a student / faculty at Vanderbilt
        if (isinstance(today_ajc_pd['email'][0], str)) and ('vanderbilt.edu' in today_ajc_pd['email'][0]):
            ## Student's Details
            today_info_pd  = today_ajc_pd.iloc[0]
            ## Email details
            to_email = today_info_pd['email']
            ## Logging in to Server
            smtpserver, my_email = email_init(email_type='vandy')
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Astronomy Journal Club'
            msg['From'   ] = my_email
            msg['To'     ] = to_email
            msg.add_header('reply-to', my_email)
            ## Writing Message - HTML
            msg_html  = '<html>'
            msg_html += '<head></head>'
            msg_html += '<body>'
            msg_html += '<p>'
            msg_html += 'Hi {0},<br /><br />'.format(today_info_pd.first_name)
            msg_html += 'Could you please send me the name and arXiv link to the '
            msg_html += 'paper that you will be presenting at AJC by today at 8pm?'
            msg_html += ' <br /><br />'
            msg_html += 'Thanks!<br />'
            msg_html += '-'*130 + '<br />'
            msg_html += '{0}<br />'.format(os.environ.get('ajc_name'))
            msg_html += "Email: <a href='mailto:{0}'>{0}</a><br />".format(os.environ.get('ajc_email'))
            msg_html += "Website: <a href='{0}' target='_blank'>{0}</a><br />".format(os.environ.get('ajc_website'))
            msg_html += "</p>"
            msg_html += '</body>'
            msg_html += '</html>'
            ## Writing Message - Text
            msg_html_2  = 'Hi {0},\r\n\r\n'.format(today_info_pd.first_name)
            msg_html_2 += 'Could you please send me the name and arXiv link to the '
            msg_html_2 += 'paper that you will be presenting at AJC by today at 8pm?\r\n\r\n'
            msg_html_2 += 'Thanks!\r\n'
            msg_html_2 += '-'*100 + '\r\n'
            msg_html_2 += '{0}\r\n'.format(os.environ.get('ajc_name'))
            msg_html_2 += "Email: {0}\r\n".format(os.environ.get('ajc_email'))
            msg_html_2 += "Website: {0}\r\n".format(os.environ.get('ajc_website'))
            ## Adding to `msg`
            part1=MIMEText(msg_html  , 'html')
            part2=MIMEText(msg_html_2, 'text')
            msg.attach(part1)
            msg.attach(part2)
            # Sending email
            smtpserver.sendmail(my_email, [to_email, my_email], msg.as_string())
            smtpserver.quit()
            ## Updating Log
            now = datetime.datetime.now()
            sys.stderr.write('{0}\t Successfully sent out `Reminder` email!\n'.format(
                now.strftime("%x %a %X")))
        else:
            # Speaker is not a Faculty / Graduate Student
            ## Student's Details
            today_info_pd  = today_ajc_pd.iloc[0]
            ## Email details
            to_email = os.environ.get('vandy_email')
            ## Logging in to Server
            smtpserver, my_email = email_init(email_type='vandy')
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Astronomy Journal Club - Speaker not Faculty / Grad Student'
            msg['From'   ] = my_email
            msg['To'     ] = to_email
            msg.add_header('reply-to', my_email)
            ## Writing Message - HTML
            msg_html  = '<html>'
            msg_html += '<head></head>'
            msg_html += '<body>'
            msg_html += '<p>'
            msg_html += 'The speaker for `{0}` could not be found! <br /><br />'.format(today_info_pd.to_frame().columns[0])
            msg_html += 'Please email them directly today to obtain their title before 8pm today!'
            msg_html += ' <br /><br />'
            msg_html += 'Thanks!<br />'
            msg_html += '-'*130 + '<br />'
            msg_html += "</p>"
            msg_html += '</body>'
            msg_html += '</html>'
            ## Writing Message - Text
            msg_html_2  = 'Hi {0},\r\n\r\n'.format(today_info_pd.first_name)
            msg_html_2  = 'The speaker for `{0}` could not be found!\r\n\r\n'.format(today_info_pd.to_frame().columns[0])
            msg_html_2 += 'Please email them directly today to obtain their title before 8pm today!\r\n\r\n'
            msg_html_2 += 'Thanks!\r\n'
            msg_html_2 += '-'*100 + '\r\n'
            msg_html_2 += '{0} \r\n'.format(os.environ.get('ajc_name'))
            msg_html_2 += "Email: {0}\r\n".format(os.environ.get('ajc_email'))
            msg_html_2 += "Website: {0}\r\n".format(os.environ.get('ajc_website'))
            ## Adding to `msg`
            part1=MIMEText(msg_html  , 'html')
            part2=MIMEText(msg_html_2, 'text')
            msg.attach(part1)
            msg.attach(part2)
            # Sending email
            smtpserver.sendmail(my_email, [to_email, my_email], msg.as_string())
            smtpserver.quit()
            ## Updating Log
            now = datetime.datetime.now()
            sys.stderr.write('{0}\t Successfully sent out `Reminder` email!\n'.format(
                now.strftime("%x %a %X")))
    else:
        # No reminders for today
        # Updating Log
        now = datetime.datetime.now()
        sys.stderr.write('{0}\t No email reminders today!\n'.format(
            now.strftime("%x %a %X")))

def send_email_PHYS_AJC(ajc_gs_pd, now_dict):
    """
    Sends email to the `PHYS_ASTRO` mailing list

    Parameters
    -----------
    ajd_gs_pd: pandas DataFrame
        merged DataFrame between `ajc_pd` and `gs_pd`
        Keys: `email`, `Date`, `Reminders`.
        Index is set to `firstname_lastname` of student.

    now_dict: python dictionary
        dictionary with `year`, `weekday`, `month`, `day` entries

    Warnings
    ---------
    Note: The `username` and `passwords` are hardcoded into the script.

    To Do: Make these variables `Environment Variables`
    """
    ## Today's Timestamp
    today_pd = pd.Timestamp('{0}/{1}/{2}'.format(now_dict['month'],
                                                 now_dict['day'],
                                                 now_dict['year']))
    # Checking if today's date is in `ajc_gs_pd`
    today_ajc_pd = ajc_gs_pd.loc[ajc_gs_pd['Send_email']==today_pd]
    # AJC Location
    ajc_zoom_url = "https://vanderbilt.zoom.us/j/970017245"
    # Checking if value exists:
    if today_ajc_pd.shape[0] == 1:
        ## Logging in to Server
        smtpserver, my_email = email_init(email_type='vandy')
        to_email = 'PHYS_AJC@LIST.VANDERBILT.EDU'
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Astronomy Journal Club'
        msg['From'   ] = my_email
        msg['To'     ] = to_email
        msg.add_header('reply-to', my_email)
        # Sending email
        today_info_pd   = today_ajc_pd.iloc[0]
        ##
        try:
            title, author   = today_info_pd['Title'].split('by')
            title           = title.strip().replace('“',"").replace('”',"")
            author, year_id = author.strip().split(' et al. ')
            year, arxiv_id  = year_id.split(" ")
            year            = int(year.replace('(','').replace(')',''))
            arxiv_id        = arxiv_id.replace('[','').replace(']','')
            ## ADS Query
            ads_link, ads_link_match = ADS_Query(author, year, arxiv_id)
        except AttributeError:
            title = ""
            author = ""
            year = ""
            arxiv_id = ""
            ads_link = ""
            ads_link_match = 0
        # Date
        today_datetime = datetime.datetime.date(today_info_pd['Date'])
        today_month    = today_datetime.strftime("%B")
        today_date     = today_datetime.strftime("%d")
        today_year     = today_datetime.strftime("%Y")
        today_weekday  = today_datetime.strftime("%A")
        today_date_str = '{0}, {1} {2}, {3}'.format(today_weekday,
                                                      today_month,
                                                      today_date,
                                                      today_year)
        ## Composing message
        msg_html  = '<html>'
        msg_html += '<head></head>'
        msg_html += '<body>'
        msg_html += '<p>'
        msg_html += 'Hello AJCers,<br/><br/>'
        msg_html += "This week's AJC will be: <br /><br />"
        msg_html += 'Title            : "{0}"<br />'.format(title)
        msg_html += 'Author  : {0} et al. ({1})<br />'.format(author, year)
        if ads_link_match == 1:
            msg_html += 'Link    : {0}<br/>'.format(ads_link)
        msg_html += 'Speaker : {0} {1}<br />'.format( today_info_pd['first_name'],
                                            today_info_pd['last_name'])
        msg_html += 'Time    : {0} @ 12pm<br />'.format(today_date_str)
        # msg_html += 'Location: SC 6333<br /><br />'
        msg_html += "Location: <a href='{0}'>{0}</a><br />".format(ajc_zoom_url)
        msg_html += 'See you all there!<br /><br />'
        msg_html += 'Thanks!<br />'
        msg_html += '-'*130 + '<br />'
        msg_html += '{0}<br />'.format(os.environ.get('ajc_name'))
        msg_html += "Email: <a href='mailto:{0}'>{0}</a><br />".format(os.environ.get('ajc_email'))
        msg_html += "Website: <a href='{0}' target='_blank'>{0}</a><br />".format(os.environ.get('ajc_website'))
        msg_html += "</p>"
        msg_html += '</body>'
        msg_html += '</html>'
        ## Msg - Text
        # msg_html_2  = 'Hello AJCers (Text),\r\n\r\n'
        # msg_html_2 += "This week's AJC will be:\r\n\r\n"
        # if ads_link_match == 1:
        #     msg_html_2 += 'Title   : "{0}"\r\n'.format(title)
        #     msg_html_2 += 'Author  : {0} et al. ({1})\r\n'.format(author, year)
        #     msg_html_2 += 'Link    : {0}\r\n'.format(ads_link)
        # msg_html_2 += 'Speaker : {0} {1}\r\n'.format(today_info_pd['first_name'],
        #                                      today_info_pd['last_name'])
        # msg_html_2 += 'Time    : {0} @ 12pm\r\n'.format(today_date_str)
        # msg_html_2 += 'Location: SC 6333\r\n\r\n'
        # msg_html_2 += 'See you all there!\r\n\r\n'
        # msg_html_2 += 'Thanks!\r\n'
        # msg_html_2 += '-'*100 + '\r\n'
        # msg_html_2 += 'Victor Calderon Arrivillaga\r\n'
        # msg_html_2 += 'Ph.D. Candidate in Physics\r\n'
        # msg_html_2 += "Email: victor.calderon@vanderbilt.edu\r\n"
        # msg_html_2 += "Website: http://vcalderon.me\r\n"
        ## Adding to `msg`
        part1=MIMEText(msg_html  , 'html')
        # part2=MIMEText(msg_html_2, 'text')
        msg.attach(part1)
        # msg.attach(part2)
        # Sending email
        smtpserver.sendmail(my_email, [to_email, my_email], msg.as_string())
        smtpserver.quit()
        ## Updating Log
        now = datetime.datetime.now()
        sys.stderr.write('{0}\t Successfully sent out `PHYS_AJC` email!\n'.format(
            now.strftime("%x %a %X")))
    else:
        ## Updating Log
        now = datetime.datetime.now()
        sys.stderr.write('{0}\t No posts for `PHYS_AJC` today!\n'.format(
            now.strftime("%x %a %X")))

def ADS_Query(author, year, arxiv_id):
    """
    Function that performs an ADS query on the `title` for the AJC topic.

    Parameters
    ----------
    author : `str`
        First author (last name) of the paper of choice.

    year : `str`
        Year of the paper to be looked for on ADS.

    arxiv_id : `int`
        ArXiv ID of the paper to be looked at.

    Returns
    -------
    paper_dict: `dict`
        Dictionary with the information about the AJC paper.
    """
    # Token form 'https://ui.adsabs.harvard.edu/#user/settings/token'
    ADS_token = os.environ.get('ads_token')
    # Configuring Token
    ads.config.token = ADS_token
    # Searching for Paper
    try:
        papers = list(ads.SearchQuery(arXiv=arxiv_id, first_author=author, year=year,
                    fl=['title','author','year','doi','identifier',
                        'first_author']))
        ## Which platform to use
        ads_opt = True
    except:
        ads_opt = False
        papers  = []
    ##
    ## Getting paper info
    if arxiv_id != '':
        if ads_opt and (len(papers) == 1):
            paper = papers[0]
            # Adding link
            arXiv_identifier = np.unique([s for s in paper.identifier if 'arXiv' in s])
            paper_link = 'http://adsabs.harvard.edu/abs/' + arXiv_identifier[0]
        else:
            ## Using arxiv API instead
            papers = arxiv.query(id_list=[arxiv_id])
            paper  = papers[0]
            paper_link = paper['arxiv_url']
        ## Checking if URL exists
        try:
            # url_checker(paper_link)
            paper_link_match = 1
        except:
            paper_link_match = 0
    else:
        paper_link_match = 0
        paper_link       = ''

    return paper_link, paper_link_match

def url_checker(url_str):
    """
    Checks if the `url_str` is a valid URL

    Parameters
    ----------
    url_str: string
        url of the website to probe
    """
    request = requests.get(url_str)
    if request.status_code != 200:
        msg = '`url_str` ({0}) does not exist'.format(url_str)
        raise ValueError(msg)
    else:
        pass

def email_init(email_type='vandy'):
    """
    Initializes the SMTP server

    Parameter
    ----------
    email_type: string, optional (default = 'vandy')
        type of email settings to use
        Options:
            - 'vandy': Sends email from the Vanderbilt Email Address

    Returns
    --------
    smtpserver: `smtplib` object
        email server being used
    """
    if email_type == 'vandy':
        smtp_server = 'smtpauth.vanderbilt.edu'
        smtp_port   = 587
        smtp_user   = os.environ['ajc_user']
        smtp_pswd   = os.environ['ajc_pswd']
        my_email    = os.environ['ajc_email']
    else:
        msg = 'Wrong `email_type` ({0})'.format(email_type)
        raise ValueError(msg)
    smtpserver = smtplib.SMTP(smtp_server, smtp_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(smtp_user, smtp_pswd)

    return smtpserver, my_email

def ADS_Testing(ajc_gs_pd, now_dict):
    """
    Tests if paper can be obtain from each paper in AJC

    Parameters
    -----------
    ajc_gs_pd: pandas DataFrame
        merged DataFrame between `ajc_pd` and `gs_pd`
        Keys: `email`, `Date`, `Reminders`.
        Index is set to `firstname_lastname` of student.

    now_dict: python dictionary
        dictionary with `year`, `weekday`, `month`, `day` entries
    """
    ## Today's Timestamp
    today_pd = pd.Timestamp('{0}/{1}/{2}'.format(now_dict['month'],
                                                 now_dict['day'],
                                                 now_dict['year']))

def main():
    """
    Grabs information for AJC and sends out email reminders before the 
    AJC date
    """
    ## Datetime dictionary
    now_dict = datetime_dict()
    ## Defining HTML URL'S
    # AJC Website
    ajc_url = ajc_url_creator(now_dict)
    ## Obtaining Tables
    # AJC Table
    ajc_pd = ajc_parser(ajc_url)
    ## Merging `ajc_pd` DataFrames
    ajc_gs_pd = ajc_gs_merge(ajc_pd)
    ## Sending email reminders to Speaker
    send_email_reminder(ajc_gs_pd, now_dict)
    ## Sending email to `PHYS_AJC`
    send_email_PHYS_AJC(ajc_gs_pd, now_dict)

# Main function
if __name__=='__main__':
    main()
