import json, collections,re
from bs4 import BeautifulSoup
from lxml import etree

def scanForHtmlTag(text):
    matches = re.findall('<.*?>', text)
    if len(matches) > 2:
        return True
    else:
        return False

def processXML(data, log):
  for child in data.iter():
      if child != None:
         if child.tag != None and isinstance(child.tag, basestring): 
            if len(child) == 0:
                if child.text != None:
                    if scanForHtmlTag(child.text):
                        #child.text = payload


def processJson(data):
  if type(data) is list:
      for m in data:
          processJson(m)
  elif type(data) is dict:
      for key in data:
           if isinstance(data[key], unicode):
#               if scanForHtmlTag(data[key]):
#                   data[key] = data[key] + payload
           else:
               processJson(data[key])
  else:     
      return

def isJavascript(contentdict):
    for a in contentdict:
        if 'application/x-javascript' in a:
            return True
    return False

def isJson(contentdict):
    for a in contentdict:
        if 'application/json' in a:
            return True
    return False

def isHtmlText(contentdict):
    for a in contentdict:
        if 'text/html' in a:
            return True
    return False

def isXml(contentdict):
    for a in contentdict:
        if 'application/xml' in a:
            return True
    return False

def response(ctx, flow):
    if flow.response.content != None and isXml(flow.response.headers['Content-Type']):
        etype = flow.response.headers['Content-Encoding'];
        flow.response.decode()

        parser = etree.XMLParser(strip_cdata=False)
        root = etree.XML(flow.response.content, parser)

	# ...
         
        flow.response.content = etree.tostring(root, encoding='UTF-8') 
        flow.response.headers['Content-Encoding'] = etype;
        if 'gzip' in etype:
            flow.response.encode('gzip')
    if flow.response.content != None and (isJson(flow.response.headers['Content-Type']) or
           isJavascript(flow.response.headers['Content-Type']) ):

        etype = flow.response.headers['Content-Encoding'];
        flow.response.decode()
      
        jsondata = json.JSONDecoder(strict=False).decode(flow.response.content)

	# ...

        flow.response.content = json.JSONEncoder().encode(jsondata)
        flow.response.headers['Content-Encoding'] = etype;
        if 'gzip' in etype:
            flow.response.encode('gzip')
    elif flow.response.content != None and isHtmlText( flow.response.headers['Content-Type'] ):
        etype = flow.response.headers['Content-Encoding'];
        flow.response.decode()

        htmldata = BeautifulSoup(flow.response.content)
        body = htmldata.body

	# ...

        r = htmldata.prettify(formatter=None)
        flow.response.content = r.encode('ascii','ignore') 

        f.close()

        flow.response.headers['Content-Encoding'] = etype;
        if 'gzip' in etype:
            flow.response.encode('gzip')
    else:
	# ...




