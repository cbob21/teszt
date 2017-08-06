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
        #JSON PARSE START
        scr = response.xpath("//script/text()")[0].extract()
        scr = scr.replace("&nbsp;","")
        scr = re.findall('var material=\s*(.*?);',scr,re.DOTALL | re.MULTILINE)
        scr4 = ""
        for item in scr:
            scr4+=item.replace("'","\"")
        cut = "{\"author\":\""
        splitted = scr4[:-1].split("{\"author\":\"")
        splitted.pop(0)
        skipped =""
        for x in splitted:
            each = cut+x
            remove_lines = str(os.linesep.join([s for s in each.splitlines() if s]))
            remove_last_comma = remove_lines.strip().rstrip(',')
            finalwork =  remove_last_comma.replace(',','XXXXXXXXXXXXX',remove_last_comma.count(',')-1).replace(',','').replace('XXXXXXXXXXXXX',',')
            parse = json.loads(finalwork)
        #JSON PARSE END
            for y in parse['files']:
                filenamestring = parse['fullname']+" - "+y['description']
                filename = "".join(i for i in filenamestring if i not in "\/:*?<>|")
                if "drive.google" in y['file']:
                    try:
                        form = "https://drive.google.com/uc?id="
                        id = y['file'][:-17][32:]
                        downloaded_name = wget.download(form+id)
                        extension = downloaded_name.split(".")[-1]
                        os.rename(str(downloaded_name),str(directory+filename+"."+extension))
                        if extension == "uc": # dead links
                            os.remove(str(directory+filename+"."+extension))
                    except ValueError:
                        print "error while downloading..."
                elif y['file'][-3:] == "pdf" or y['file'][-4:] == "pptx" :
                    try:
                        downloaded_name = wget.download(y['file'])
                        extension = downloaded_name.split(".")[-1]
                        wget.download(y['file'])
                        os.rename(str(downloaded_name),str(directory+filename+"."+extension))
                    except ValueError:
                        print "error while downloading..."
                else:
                    skipped+=y['file']+"\n"
        with open("skipped_links.txt","w") as save:
            save.write(skipped)
