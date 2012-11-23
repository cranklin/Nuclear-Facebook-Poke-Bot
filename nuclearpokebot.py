#!/usr/bin/python
import os
import pycurl
import cStringIO
import re
import time

username = "username"
password = "password"
returnpoke = True
newpoke = True

def login():
    os.remove("pycookie.txt")

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://www.facebook.com")
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
    c.perform()
    curlData = buf.getvalue()
    buf.close()

    charsettest = re.findall(ur"name=\"charset_test\" value=\"([^\"]*)",curlData)
    lgnrnd = re.findall(ur"name=\"lgnrnd\" value=\"([^\"]*)",curlData)
    locale = re.findall(ur"name=\"locale\" value=\"([^\"]*)",curlData)
    lsd = re.findall(ur"name=\"lsd\" value=\"([^\"]*)",curlData)

    persistent = 1
    default_persistent = 1
    timezone = 480
    lgnjs = time.time()
    lgnjs = int(lgnjs)

    postdata = 'charset_test='+charsettest[0]+'&locale='+locale[0]+'&email='+username+'&pass='+password+'&lsd='+lsd[0]+'&default_persistent='+str(default_persistent)+'&lgnjs='+str(lgnjs)+'&lgnrnd='+lgnrnd[0]+'&persistent='+str(persistent)+'&timezone='+str(timezone)

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://login.facebook.com/login.php?login_attempt=1")
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, postdata)
    c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
    #c.setopt(pycurl.VERBOSE, True)
    c.perform()
    curlData = buf.getvalue()
    buf.close()
    #print curlData



def poke():
    #enter infinite poke loop
    while True:
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://www.facebook.com/pokes?notif_t=poke")
        c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
        c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.ENCODING, "")
        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
        c.perform()
        curlData = buf.getvalue()
        buf.close()
        #print curlData
        pokebackdata = re.findall(ur"<div class=\"pokeHeader fsl fwb fcb\"><a href=\"(.*?)\" data-hovercard=\"\/ajax\/hovercard\/user.php\?id=([0-9]*)\">([^<]*)<\/a> has poked you.<\/div>",curlData)
        pokesuggestdata = re.findall(ur"<div class=\"userSuggestionName\"><span class=\"fwb\"><a href=\"https:\/\/www.facebook.com\/(.*?)\" data-hovercard=\"\/ajax\/hovercard\/user.php\?id=([0-9]*)\">([^<]*)<\/a><\/span><\/div>",curlData)
        #print pokebackdata
        userid = re.findall(ur"\"user\":\"([0-9]*)\"",curlData)
        fb_dtsg = re.findall(ur"name=\"fb_dtsg\" value=\"([^\"]*)",curlData)

        if len(pokesuggestdata)>0 and newpoke:
            for victim in pokesuggestdata:
                victimid = victim[1]
                postdata = '__a=1&nctr[_mod]=pagelet_pysp&suggestion=1&__user='+str(userid[0])+'&fb_dtsg='+fb_dtsg[0]+'&uid='+str(victimid)
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, "https://www.facebook.com/ajax/pokes/poke_inline.php")
                c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
                c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
                c.setopt(pycurl.WRITEFUNCTION, buf.write)
                c.setopt(pycurl.FOLLOWLOCATION, 1)
                c.setopt(pycurl.ENCODING, "")
                c.setopt(pycurl.SSL_VERIFYPEER, 0)
                c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.POSTFIELDS, postdata)
                c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
                #c.setopt(pycurl.VERBOSE, True)
                c.perform()
                curlData = buf.getvalue()
                buf.close()
                print "You poked "+victim[2]+"!"

        if len(pokebackdata)>2 and returnpoke:
            for victim in pokebackdata:
                victimid = victim[1]
                postdata = '__a=1&nctr[_mod]=pagelet_pokes&pokeback=1&__user='+str(userid[0])+'&fb_dtsg='+fb_dtsg[0]+'&uid='+str(victimid)
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, "https://www.facebook.com/ajax/pokes/poke_inline.php")
                c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
                c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
                c.setopt(pycurl.WRITEFUNCTION, buf.write)
                c.setopt(pycurl.FOLLOWLOCATION, 1)
                c.setopt(pycurl.ENCODING, "")
                c.setopt(pycurl.SSL_VERIFYPEER, 0)
                c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.POSTFIELDS, postdata)
                c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
                #c.setopt(pycurl.VERBOSE, True)
                c.perform()
                curlData = buf.getvalue()
                buf.close()
                print "You return poked "+victim[2]+"!"

        else:
            time.sleep(3)


def main():
    login()
    poke()

if __name__ == "__main__":
    main()
