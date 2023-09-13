
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2021.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 10852565 # put your student number here as an integer
student_name   = "Ryan Indrananda" # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Choose Your News
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a useful application that allows the user to compare news stories
#  from multiple sources and save them for later perusal.
#
#  See the client's requirements accompanying this file for full
#  details.
#
#--------------------------------------------------------------------#



#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: DON'T import all of the "tkinter.tkk" functions
# using a "*" wildcard because this module includes alternative
# versions of standard widgets like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we do NOT encourage using
#      this option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a Windows 10 computer instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Import additional modules
from html import unescape # Method to convert ascii to html script
from tkinter import messagebox # Method to show errors to user

# Define function to read and decode source
def read_source_page():
    global source_page_contents
    source_page = urlopen(source_address)
    source_page_bytes = source_page.read()
    source_page_contents = source_page_bytes.decode("UTF-8")

# Define function to write source details in article details tab
def write_source_details():
    headline_info.delete("1.0", END)
    article_abstract_textbox.delete("1.0", END)
    details_textbox.delete("1.0", END)
    headline_info.insert(INSERT, source_headline)
    article_abstract_textbox.insert(INSERT, source_abstract)
    details_textbox.insert(INSERT, "Dateline: " + source_dateline + "\n")
    details_textbox.insert(INSERT, "News source: " + source_name + "\n")
    details_textbox.insert(INSERT, "Hostname: "+ name_of_host + "\n")
    details_textbox.insert(INSERT, "URL: " + source_address)

# Define function to handle errors when opening source
def error_handle_open_source():
    source_headline = 'ERROR - Could not obtain headline.'
    source_abstract = 'ERROR - Could not obtain abstract.'
    source_dateline = 'ERROR - Dateline unobtainable.'

# Define function to open source and extract details
def open_news_source():
    global source_name
    global source_headline
    global source_abstract
    global source_dateline
    global source_address
    global source_page_contents
    global name_of_host
    if news_source_options.get() == "Wired": # If block to open and extract Wired news
        try:
            source_name = "Wired"
            source_address = "https://www.wired.com/most-recent"
            name_of_host = "www.wired.com"
            read_source_page()
            source_page_contents = source_page_contents.replace('<em>', '') # Replace common
            source_page_contents = source_page_contents.replace('</em>','') # html tags
            try:
                wired_headline = findall('archive-item-component__title">(.*?)</h2>', \
                    source_page_contents) # Search for headline
                source_headline = unescape(wired_headline[0])
                wired_abstract = findall('archive-item-component__desc">(.*?)</p>', \
                    source_page_contents) # Search for abstract
                source_abstract = unescape(wired_abstract[0])
                wired_dateline = findall('<time>(.*?)</time>', \
                    source_page_contents) # Search for dateline
                source_dateline = wired_dateline[0]
            except:
                error_handle_open_source()
            write_source_details()
        except: # Display error if source cannot be opened
            messagebox.showerror('Error', \
                'Source could not be opened - Please check your internet connection.')
    elif news_source_options.get() == "Ars Technica": # Repeated if block for Ars Technica
        try:
            source_name = "Ars Technica"
            source_address = "https://www.arstechnica.com/gadgets"
            name_of_host = "www.arstechnica.com"
            read_source_page()
            try:
                arstechnica_headline = findall('<h2>.*?">(.*?)</a>', \
                    source_page_contents)
                source_headline = unescape(arstechnica_headline[0])
                arstechnica_abstract = findall('<p class.*?">(.*?)</p>', \
                    source_page_contents)
                source_abstract = unescape(arstechnica_abstract[0])
                arstechnica_dateline = findall('datetime="(.*?)T', \
                    source_page_contents)
                arstechnica_time = findall('datetime=".*?T(.*?)\+00:00"', \
                    source_page_contents)
                source_dateline = arstechnica_dateline[0] + " at " + arstechnica_time[0] + " UTC"
            except:
                error_handle_open_source
            write_source_details()
        except:
            messagebox.showerror('Error', \
                'Source could not be opened - Please check your internet connection.')
    elif news_source_options.get() == "Cnet": # Repeated if block for Cnet
        try:
            source_name = "Cnet"
            source_address = "https://www.cnet.com/news"
            name_of_host = "www.cnet.com"
            read_source_page()
            try:
                cnet_headline = findall('assetHed">\n(.*?)\n', \
                    source_page_contents)
                source_headline = unescape(cnet_headline[0].strip())
                cnet_abstract = findall('assetHed">\n(.*?)\n', \
                    source_page_contents)
                source_abstract = unescape(cnet_abstract[1].strip())
                cnet_dateline = findall('timeCircle.*?>(.*?)</span><span>(.*?)</span>', \
                    source_page_contents)
                source_dateline = cnet_dateline[0][0] + ' ' + cnet_dateline[0][1]
            except:
                error_handle_open_source()
            write_source_details()
        except:
            messagebox.showerror('Error', \
                'Source could not be opened - Please check your internet connection.')
    else: # Else block for last option, Tech Crunch
        try:
            source_name = "Tech Crunch"
            source_address = "https://techcrunch.com"
            name_of_host = "www.techcrunch.com"
            read_source_page()
            try:
                techcrunch_headline = findall('post-block__title__link">\n(.*?)</a>', \
                    source_page_contents)
                source_headline = unescape(techcrunch_headline[0].strip())
                techcrunch_abstract = findall('post-block__content">\n(.*?)</div>', \
                    source_page_contents)
                source_abstract = unescape(techcrunch_abstract[0].strip())
                techcrunch_dateline = findall('datetime="(.*?)T', \
                    source_page_contents)
                techcrunch_time = findall('datetime=".*?T(.*?)-07:00', \
                    source_page_contents)
                source_dateline = techcrunch_dateline[0] + " at " + techcrunch_time[0] + " GMT -7"
            except:
                error_handle_open_source()
            write_source_details()
        except:
            messagebox.showerror('Error', \
                'Source could not be opened - Please check your internet connection.')

# Define function to check source (open in browser)
def check_source():
    try:
        if news_source_options.get() == "Wired":
            source_address = "https://www.wired.com/most-recent"
        elif news_source_options.get() == "Ars Technica":
            source_address = "https://www.arstechnica.com/gadgets"
        elif news_source_options.get() == "Cnet":
            source_address = "https://www.cnet.com/news"
        elif news_source_options.get() == "Tech Crunch":
            source_address = "https://techcrunch.com"
        urldisplay(source_address)
    except UnboundLocalError:
        messagebox.showerror('Error', \
            'Please select a news source before checking source.')
    except:
        messagebox.showerror('Error', \
            'Something went wrong - source could not be opened.')

# Define function to export details to database
def export_selection():
    try:
        connection = connect(database = 'selected_news.db')
        selected_news_db = connection.cursor()
        selected_news_db.execute('''INSERT INTO latest_news(date_or_time, headline, 
                                    abstract, news_source)
                                    VALUES (?, ?, ?, ?)''', \
                                    (source_dateline, source_headline, source_abstract, source_name))
        connection.commit()
        selected_news_db.close()
        connection.close()
        messagebox.showinfo('Export successful', 'Data has been added to database.')
    except NameError:
        messagebox.showerror('Error', \
            'Please select a news source before exporting.')
    except:
        messagebox.showerror('Error', \
            'Something went wrong - source could not be exported.')

# Initialize tkinter window for news application
news_interface = Tk()
news_interface.title("Tech News Today!")
news_interface.configure(bg = "#ADD1FB")

# Initialize images to be used in the application
header_image = PhotoImage(file = "header.png")
wired_logo = PhotoImage(file = "wired.png")
arstechnica_logo = PhotoImage(file = "arstechnica.png")
cnet_logo = PhotoImage(file = "cnet.png")
techcrunch_logo = PhotoImage(file = "crunch.png")

# Paste header image on the top of the window
news_image = Label(news_interface, image = header_image, border = "0")
news_image.grid(row = 0, column = 0, columnspan = 2)

# Create label frame to display news
tech_frame_title = LabelFrame(news_interface, text = "The Latest in Tech", \
    font = 16, bg = "#ADD1FB")
tech_frame_title.grid(row = 1, column = 0)

# Create text box to display article headline 
headline = Label(tech_frame_title, text = "Article headline: ", width = 32, \
                    font = ("TkDefaultFont", 12, "bold"), fg = "white", \
                        bg = "#011625", anchor = "w")
headline.grid(row = 0, column = 0)
headline_info = Text(tech_frame_title, height = 3, width = 46, \
    font = ("TkDefaultFont", 10, "bold"), wrap = WORD)
headline_info.grid(row = 1, column = 0)

# Create text box to display article body
article_abstract_label = Label(tech_frame_title, text = "Article abstract: ", width = 32, \
                    font = ("TkDefaultFont", 12, "bold"), fg = "white", \
                        bg = "#011625", anchor = "w")
article_abstract_label.grid(row = 2, column = 0)
article_abstract_textbox = Text(tech_frame_title, height = 10, width = 40, wrap = WORD)
article_abstract_textbox.grid(row = 3, column = 0)

# Create label to display news details
news_details = Label(tech_frame_title, text = "Article details: ", width = 32, \
                    font = ("TkDefaultFont", 12, "bold"), fg = "white", \
                        bg = "#011625", anchor = "w")
news_details.grid(row = 4, column = 0)
details_textbox = Text(tech_frame_title, height = 4, width = 40, wrap = WORD)
details_textbox.grid(row = 5, column = 0)
details_textbox.insert(INSERT, "Dateline: \nNews source: \nHostname: \nURL: ")

# Create label frame to display news sources
news_sources = LabelFrame(news_interface, text = "Select a tech news source below", \
    font = 16, bg = "#ADD1FB")
news_sources.grid(row = 1, column = 1)

# Initialize radiobutton options
news_source_options = StringVar(news_sources, "1")

# Button to select Wired as source
wired_source = Radiobutton(news_sources, image = wired_logo, bg = "#ADD1FB", \
                    variable = news_source_options, \
                        value = "Wired", command = open_news_source)
wired_source.grid(row = 0, column = 0, sticky = "W")

# Button to select Ars Technica as source
arstechnica_source = Radiobutton(news_sources, image = arstechnica_logo, bg = "#ADD1FB", \
                    variable = news_source_options, \
                        value = "Ars Technica", command = open_news_source)
arstechnica_source.grid(row = 1, column = 0, sticky = "W")

# Button to select Cnet as source
cnet_source = Radiobutton(news_sources, image = cnet_logo, bg = "#ADD1FB", \
                    variable = news_source_options, \
                        value = "Cnet", command = open_news_source)
cnet_source.grid(row = 0, column = 1, sticky = "W")

# Button to select Tech Crunch as source
techcrunch_source = Radiobutton(news_sources, image = techcrunch_logo, bg = "#ADD1FB", \
                    variable = news_source_options, \
                        value = "Tech Crunch", command = open_news_source)
techcrunch_source.grid(row = 1, column = 1, sticky = "W")

# Button to check source
check_source_button = Button(news_sources, text = "Check Source", \
                    fg = "white", bg = "#011625", command = check_source)
check_source_button.grid(row = 2, column = 0)

# Button to export news
export_selection_button = Button(news_sources, text = "Export selection", \
                    fg = "white", bg = "#011625", command = export_selection)
export_selection_button.grid(row = 2, column = 1)

# Executes tkinter application
news_interface.mainloop()