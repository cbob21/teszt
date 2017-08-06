import scrapy
import re
import string
import json
import sys
import wget
import os
url = "http://grammars.grlmc.com/DeepLearn2017/materials/"
post_user = "userName"
post_pass = "userPassword"
username = "szablevi@gmail.com"
password = "0b29a17991"
directory = "pdfs/"
if not os.path.exists(directory):
    os.makedirs(directory)
reload(sys)
sys.setdefaultencoding('utf-8')
class teszt(scrapy.Spider):
    name = "teszt"

    def start_requests(self):
        return [scrapy.FormRequest(url,
                                   formdata={post_user: username, post_pass: password},
                                   callback=self.logged_in)]
    def logged_in(self, response):
        scr = response.xpath("//script/text()")[0].extract()
        scr = scr.replace("&nbsp;","")
        scr = re.findall('var material=\s*(.*?);',scr,re.DOTALL | re.MULTILINE)
        scr4 = ""
        for item in scr:
            scr4+=item.replace("'","\"")
        cutted_part = "{\"author\":\""
        splitted = scr4.split("{\"author\":\"")
        splitted.pop(0)
        for x in splitted:
            each = cutted_part+x
            remove_lines = str(os.linesep.join([s for s in each.splitlines() if s]))
            remove_last_comma = remove_lines.strip().rstrip(',')
            finalwork =  remove_last_comma.replace(',','XXXXXXXXXXXXX',remove_last_comma.count(',')-1).replace(',','').replace('XXXXXXXXXXXXX',',')
            parse = json.loads(finalwork)
            for y in parse['files']:
                #print "possible file name: "+parse['fullname']+" - "+y['description']+".pdf"
                if "drive.google" not in y['file']:
                    filenamestring = parse['fullname']+" - "+y['description']+".pdf"
                    filename = "".join(i for i in filenamestring if i not in "\/:*?<>|")
                    wget.download(y['file'],directory+filename)
        #url ="https://drive.google.com/file/d/0ByPBMv-S_GMEZVF2aDVYdGFaUVE/view?usp=sharing"
        #filename = wget.download(url,"google.pdf")
        #print filename
        #print "..."
