'''This is to check the website integrity.
Its midnight code so excuse efficiency.

run this after you have a server running at *000 port.
ie after calling python manage.py runserver or something like
that if you have some other setup
'''
from BeautifulSoup import BeautifulSoup
import urllib2

def getlinks(code,header):
	soup=BeautifulSoup(code)
	linklist=[]
	for f in soup.findAll('a'):
		if ('next' in f.text.lower().strip())or('previous' in f.text.lower().strip()):
			continue
		linklist.append(header+f['href'])
	return linklist
def crawl(seed):
	broken=[]
	done=[]
	todo=[seed]
	header=seed
	while True:
		if len(todo)<1:
			break
		new_links=[]
		for i in todo:
			try:
				page=urllib2.urlopen(i)
				if page.code!=200:#check if broken
					broken.append((page.code,i))
				print page.code,i,
				nl=getlinks(page.read(),header)
				for k in nl:
					if k not in done:
						done.append(k)
						new_links.append(k)
				print len(nl)
			except Exception as e:
				print e
		todo=new_links
	print broken
	return broken,done
	
if __name__=='__main__':
	print 'Crawling the localhost at http://localhost:8000'
	print '-------------------------------------------'
	broken,done=crawl('http://localhost:8000')
	print '-------------------------------------------'
	print 'Broken links found'
	for i in broken:
		print i
	
