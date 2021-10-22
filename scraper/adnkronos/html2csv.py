import sys, re
from docopt import docopt
from bs4 import BeautifulSoup

cli="""
Usage:
  jsonlist2csv.py (-h | --help)
  jsonlist2csv.py [-i=FILE] [-o=FILE]

Options:
  -h --help  Show this screen.
  -i=FILE    Input file [default: temp.html]
  -o=FILE    Input file [default: temp.csv]
"""

if __name__ == "__main__":
	args = docopt(cli, version='0.1')
	
	with open("HTML/"+args["-i"],"r",encoding="utf8") as f:
		data = f.read()
	
	expert = re.search('QUERY: +&quot;(.*?)&quot;',data).group(1)
	list = re.search('<section class="list-art-cont light-list">(.|\n)+</section>', data).group(0)
	article = [x.group(0) for x in re.finditer('<article class="art art-list "(.|\n)+?</article>', list)]
	
	length = len(article)
	i = 0
	with open(args["-o"],"w",encoding="utf8") as f:
		while i < length:
			line = [''] * 5
			line[0] = expert
			line[1] = re.search('<span class="day">(.*?)</span>',article[i]).group(1)
			line[2] = re.search('<span class="time">(.*?)</span>',article[i]).group(1)
			title   = re.search('<h3 class="title">(.|\n)+</h3>',article[i]).group(0)
			line[3] = "https://www.adnkronos.com" + re.search('<a href="(.*?)">',title).group(1)
			line[4] = '"%s"' % re.search('">(.*?)</a>',title).group(1).strip().replace('"','""')
			
			f.write(";".join(line)+"\n")
			i+=1
