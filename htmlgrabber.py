#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  written/tested using python 2.7.12

import urllib2, sys
from bs4 import BeautifulSoup

# fix utf8 - related encoding errors
reload(sys)
sys.setdefaultencoding("utf8")

def grabHTML(year, outputfile, appendToExisting):
    """Collects all HTML-based agendas from sanjoseca.gov from the specified year and outputs the raw HTML of those agendas in a single file.
    
    Args:
        year: the year from which to gather Agendas.
        outputfile: the name/path of the file in which you want to save the raw HTML
        appendToExisting: (boolean) whether to overwrite outputfile, or append newly-scraped agendas. Useful if you want one file with all available years' agendas
    Returns:
        void
    Raises:
        ValueError: if year is out of range (2015-2017)
    
    """
    agendaURLs = {2017:"http://www.sanjoseca.gov/index.aspx?NID=5322", 2016:"http://www.sanjoseca.gov/index.aspx?NID=4858", 2015:"http://www.sanjoseca.gov/index.aspx?NID=4535"}
    if year not in agendaURLs:
        raise ValueError('Invalid year. HTML-based agendas are only to be found in 2015, 2016, and 2017.')
    
    print "Scraping HTML agendas from year", str(year)+"..."
    outputContent = ""
    errorContent = str(year)+"\nnon-HTML agendas encountered:\n\n"
    yearHTMLsoup = BeautifulSoup(urllib2.urlopen(agendaURLs[year]).read(), "html.parser")
    linkTable = yearHTMLsoup.find("table", class_="telerik-reTable-2")
    for row in linkTable.find_all("tr"):
        anchor =  row.td.a
        try:
            a_href = anchor['href']
            if (a_href.find("AgendaViewer") >= 0 and a_href.find(".pdf") == -1):
                print "scraping " + a_href
                outputContent += urllib2.urlopen(a_href).read()
            else:
                errorContent += anchor.string + "\t\t" + a_href + "\n"
                print "*** non-HTML agenda found: " + anchor.string + "\t" + a_href
        except TypeError:
            pass
    
    if appendToExisting:
        f = open(outputfile, 'a')
    else:
        f = open(outputfile, 'w')
    err_f = open("htmlgrabber_error.txt", 'w')
    f.write(outputContent)
    err_f.write(errorContent)
    f.close()
    err_f.close()
        
    

#command-line usability (run ""htmlgrabber.py -h" for help, or just read below....)
if __name__ == '__main__':
    import getopt
    y = 2017
    append = False
    output = "htmlgrabber_output.txt"
    try: 
        opts, args = getopt.getopt(sys.argv[1:],"hy:o:a")
    except getopt.GetoptError:
        print "Error - please use this format:\n\tpython htmlgrabber.py -y <year> -o <outputfile.txt>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "\nhtmlgrabber.py - command line interface\n\n\
Collects all html-based agendas from the San Jose City Council website\n\
in a given year, and spits them out as a single, continuous text file\n\
(raw html). Also populates htmlgrabber_error.txt with any agendas unable\n\
to be output, probably because that agenda is a pdf rather than html.\n\n\
usage: htmlgrabber.py -y <year> -o <outputfile>\n\t\
-a :\tappends new HTML to the existing outputfile\n\n"
            sys.exit()
        elif opt == '-y':
            y = int(arg)
        elif opt == '-o':
            output = arg
        elif opt == '-a':
            append = True
    sys.exit(grabHTML(y, output, append))
