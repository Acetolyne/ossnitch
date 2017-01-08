#!/usr/bin/env python3

print("  ___      ____        _ _       _     ")       
print(" / _ \ ___/ ___| _ __ (_) |_ ___| |__  ")
print("| | | / __\___ \| '_ \| | __/ __| '_ \ ")
print("| |_| \__ \___) | | | | | || (__| | | |")
print(" \___/|___/____/|_| |_|_|\__\___|_| |_|")
print("")
print("OsSnitch version 1.0.0-beta by Acetolyne")

import sys, getopt, urllib, http.cookiejar, re, os
#@todo add a -l option for listing the files

def grabwebsite(ip):
  data = ""
  cj = http.cookiejar.CookieJar()
  op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  op.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rev:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),] # who cares were a MAC.
  url = "http://iknowwhatyoudownload.com/en/peer/?ip="+ip
  website = op.open(url)
  website = website.read().decode()
  for sd in website:
    data += str(sd)
  return data

def printtags(tmp):
  alltags = ""
  tags = re.findall(r'<span class="label label-.*?">(.*?)<\/span>', tmp, re.DOTALL)
  for tag in tags:
    alltags = alltags + " " + tag.strip()
  print("TAGS: "+alltags)

def getdata(tmp, files):
  table = re.findall(r'<tr class=".*?">(.*?)<\/tr>', tmp, re.DOTALL)
  for a in table:
    info = re.findall(r'<td class=".*?">.*?<\/td>.*?<td class="date-column">(.*?)<\/td>.*?<td class="category-column">(.*?)<\/td>.*?<a href="(.*?)">(.*?)<\/a>', a, re.DOTALL)
    for data in info:
      tmpfiles = []
      #Lets strip out all files that dont tell us the OS
      if (data[1] != 'XXX' and data[1] != 'Movies' and data[1] != 'Music' and data[1] != 'TV'):
        filename = (data[3].strip())
        base, tmpext = os.path.splitext(filename)
        tmpfiles = [data[0], data[1], data[2], tmpext]
        files.append(tmpfiles)
  files.sort(key=lambda r: r[0], reverse=True)
  return files

def checkmatch(tmp):
  thisos = ""
  windows = [".exe", ".inf", ".dll", ".bat"] #define windows extensions
  debianlinux = [".deb"] #define debian linux extensions
  macosx = [".mac"] #define mac extensions
  linux = [""] #define linux extensions
  tmp = tmp.lower()
  if tmp in windows:
    thisos = "Windows"
  if tmp in linux:
    thisos = "Linux"
  if tmp in debianlinux:
    thisos = "Debian Linux"
  if tmp in macosx:
    thisos = "Mac OSX"
  return thisos

def getos(data):
  finos = ""
  for this in data:
    if finos:
      break
    else:
      torrentinfo = ""
      cj = http.cookiejar.CookieJar()
      op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
      op.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rev:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),] # who cares were a MAC.
      url = "http://iknowwhatyoudownload.com"+this[2]
      website = op.open(url)
      website = website.read().decode()
      for sd in website:
        torrentinfo += str(sd)
        torext = re.findall(r'<td title=".*?">(.*?)<\/td>', torrentinfo.strip(), re.DOTALL)
      for a in torext:
        base, tmpext = os.path.splitext(a)
        finos = checkmatch(tmpext)
  if finos:
    print("Based on the most recent file that could identify the OS your target is most likely running "+finos) 
  else:
    print("No downloaded torrents could be used to identify the possible operating system.")

def main(argv):
  files = []
  ip = ""
  try:
    opts, args = getopt.getopt(argv,"hi:",["ipaddress="])
  except getopt.GetoptError:
    print("USAGE: ossnitch -i <ipaddress>")
    sys.exit()
  for opt, arg in opts:
    if opt in ("-i", "--ipaddress"):
      ip = arg
      print("Looking at info for IP: "+ip)
  if not ip:
    print("USAGE: ossnitch -i <ipaddress>")
    sys.exit()
  thissite = grabwebsite(ip)
  printtags(thissite)
  tmp = thissite[thissite.find('<tbody>')+len('<tbody>'):thissite.rfind('</tbody>')]
  data = getdata(tmp, files)
  getos(data)

if __name__ == "__main__":
  main(sys.argv[1:])

