#!/usr/bin/env python

# Running pepsite on own pdbs, running on existing pdbs can be done through the RESTless API.
import mechanize
import cookielib
import sys
import re
import time
#import urllib
import os
#from bs4 import BeautifulSoup



def parse_html(html_file,outfile):
    fi=open(html_file,'r')
    fo=open(outfile,'w')
    get_score=False
    for line in fi:
        line=line.strip()
        print line
        
        m=re.match('(\d+)$',line)
        if m:
            rank=m.group(1)
            print rank
            get_score=True
        elif get_score:
            score=line
            print 'SCORE: ' + rank + ' ' + score
            fo.write(rank +' ' + line + '\n')
            get_score=False
        if re.search('rank  p-value   N',line):
            fo.write(line + '\n')

    return 0

if len(sys.argv)!=3:
    print "\n\t./run_pepsite.py <filename> <peptide>\n"
    sys.exit()

filename=sys.argv[1]
peptide=sys.argv[2]

outfile_html=filename + '.' + peptide + '.html'

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
#br.set_handle_gzip(True)                                                                                                           
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(True)
# Follows refresh 0 but not hangs on refresh > 0                                                                                    
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?                                                                                                          
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3\.0.1')]                                                                                                                             

debug=False

url="http://pepsite2.russelllab.org/"
#Submit_url="http://www.predictioncenter.org/casp11/predictions_submission.cgi"
response = br.open(url)
#for frm in br.forms():
#    print frm
#sys.exit()
#print response.read()      # the text of the page                                                                                  
#response1 = br.response()  # get the response again                                                                                
#print response1.read()     # can apply lxml.html.fromstring()                                                                      
#br.select_form("uploadform2"
br.select_form(nr=1)
#print br.form
#print
br.form['ligand'] = peptide
#print br.form
#print
#print filename
br.form.set_all_readonly(False)
br.form.add_file(open(filename),'text/plain',filename,name='file')
#['file'] = str(filename)
br.form.set_all_readonly(False)
print br.form

req = br.submit()
result_url=br.geturl()
pdb_url=result_url + '&format=pdb'
rpdb_url=result_url + '&format=rpdb'


print "result url: " + result_url
n=0

while not re.search('Match results',br.open(result_url).read()):
    print ".",
    sys.stdout.flush()
    time.sleep(2)
    n=n+2
print
lynx_cmd="lynx -dump \"" + result_url + "\" >" + outfile_html
os.system(lynx_cmd)

#f=open(filename + '.html','w')
#f.write(BeautifulSoup(br.open(result_url).read()).get_text(),"lxml")
#f.close()

print "Outfile: " + outfile_html
parse_html(outfile_html,outfile_html + '.scores')
print "Outfile: " + outfile_html + '.scores'
for fmt in ('pdb','rpdb'):
    dl_url=result_url+'&format='+fmt
    outfile=filename + '.' + peptide + '.' + fmt
    #print dl_url + ' -> ' + outfile
    cmd='wget -q \"{}\" -O {}'.format(dl_url,outfile)
    os.system(cmd)
    print "Outfile: " + outfile
#    dl.retrieve(dl_url,outfile)
#print req.read()

#response=br.retrieve(submit_url)                                                                                                   

#print response.read()                                                                                                              



