"""Run locally: python tools/prepare_import.py /path/to/submissions.zip"""
import sys,zipfile,re,json,unicodedata,pathlib
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.body=False;self.parts=[];self.styles=[];self.style=False
 def handle_starttag(self,tag,attrs):
  if tag=='body':self.body=True;return
  if tag=='style':self.style=True;return
  if self.body and tag not in ('script','iframe','form','object','embed','meta','link','base'):
   safe=[(k,v) for k,v in attrs if not k.lower().startswith('on') and k.lower() not in ('srcdoc',) and not (v or '').lower().strip().startswith(('javascript:','data:'))]
   import html
   self.parts.append('<'+tag+''.join(' '+k+'="'+html.escape(v or '',quote=True)+'"' for k,v in safe)+'>')
 def handle_endtag(self,tag):
  if tag=='body':self.body=False
  elif tag=='style':self.style=False
  elif self.body and tag not in ('script','iframe','form','object','embed','meta','link','base'):self.parts.append('</'+tag+'>')
 def handle_data(self,data):
  if self.style:self.styles.append(data)
  elif self.body:self.parts.append(data)
 def handle_entityref(self,name):
  if self.body:self.parts.append('&'+name+';')
 def handle_charref(self,name):
  if self.body:self.parts.append('&#'+name+';')
def slug(s):
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower();return re.sub(r'[^a-z0-9]+','-',s).strip('-')
path=pathlib.Path(sys.argv[1]);out=[]
with zipfile.ZipFile(path) as z:
 for f in z.namelist():
  if not f.lower().endswith(('.html','.htm')):continue
  raw=z.read(f).decode('utf-8','replace');p=Parser();p.feed(raw)
  name=f.split('_')[0];blog_id=slug(name);out.append({'id':blog_id,'name':name,'originalHtml':''.join(p.parts),'originalCss':'\n'.join(p.styles),'sourceFile':f})
outfile=pathlib.Path(__file__).resolve().parent.parent/'private'/'import-data.json';outfile.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('Prepared',len(out),'blogs:',outfile)
