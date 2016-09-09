#!/bin/env python
# courses information downloader for ugc courses
# author: graceshirts
# created: 

import urllib2
import os
import re
from bs4 import BeautifulSoup

DL = "*"
COURSES = []
COURSE_INDEX = "http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_index.htm"
COURSE_BASE = "http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_{}.htm"
COURSE_PDF_BASE = "https://www.cityu.edu.hk/ug/201617/course/{}.pdf"

def get_all_links(url):
    response = urllib2.urlopen(url)
    web_page = response.read()
    soup = BeautifulSoup(web_page, "html.parser")
    c_links = soup.find_all("a")
    return c_links

def get_all_courses():
    try: 
        c_links = get_all_links(COURSE_INDEX)

        for c_link in c_links:
            href = c_link.get("href")
            c_doc = href.split("/")[1]
            c_doc_name = c_doc.split(".")[0]
            c_name = c_doc_name.split("_")[2]

            if c_name not in COURSES:
                COURSES.append(c_name)
                print "{}: {}".format(c_name, c_link.get_text())

    except IOError:
        print "ioerror"


def dl_course_pdf(c_doc_name, c_folder):
    try:
        c_pdf_url = COURSE_PDF_BASE.format(c_doc_name)
        response = urllib2.urlopen(c_pdf_url)
        pdf = response.read()
        filename = c_doc_name + ".pdf"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(current_dir, "output", c_folder)

        try:
            os.makedirs(dest_dir)
        except OSError:
            pass

        path = os.path.join(dest_dir, filename)
        
        with open(path, "wb") as stream:
            stream.write(pdf)

    except:
        print "error"


def dl_course_info(c_name):
    try:
        c_url = COURSE_BASE.format(c_name)
        c_links = get_all_links(c_url)
        
        for c_link in c_links:
            href = c_link.get("href")
            c_doc = href.split("/")[2]
            c_doc_name = c_doc.split(".")[0]
            dl_course_pdf(c_doc_name, c_name)
            
        print "{} information is downloaded.".format(c_name)
    except:
        print "error"


def dl_course_doc(c_name):
    try:
        response = urllib2.urlopen(COURSE_BASE.format(c_name))
        web_page = response.read()
        filename = c_name + ".htm"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(current_dir, "output")

        try:
            os.makedirs(dest_dir)
        except OSError:
            pass

        path = os.path.join(dest_dir, filename)
        
        with open(path, "w") as stream:
            stream.write(web_page)

    except:
        print "dl_course_doc error."

if __name__ == "__main__":
    get_all_courses()
    c_input = raw_input("Which course(s) information do you want to download? separate with ',' and no spaces between each courses.\n")
    
    c_input_list = c_input.split(",")
    c_dl = []

    for c_item in c_input_list:
        c_dl.append(c_item.upper())

    if c_input_list[0] == "*":
        for c_name in COURSES:
            dl_course_info(c_name)
            dl_course_doc(c_name)
    else:
        for c_name in c_dl:
            if c_name in COURSES:
                dl_course_info(c_name)
                dl_course_doc(c_name)
