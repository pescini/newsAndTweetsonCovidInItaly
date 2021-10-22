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
  -o=FILE    Input file [default: temp.txt]
"""

if __name__ == "__main__":
	args = docopt(cli, version='0.1')
	
	plaintext = lambda x: BeautifulSoup(x.replace("\u0300",""), "html.parser").get_text().strip()
	
	with open(args["-i"],"r",encoding="utf8") as f:
		article = f.read()
		
		url = re.search('"@id":"(.*?)"',article).group(1)
		paragraph = " ".join([plaintext(x.group(1)) for x in re.finditer('<p class="art-text">(.*?)</p>', article)])
		quoted = ". ".join([x.group(0).strip('"') for x in re.finditer('".+?"', paragraph)])
		
	with open(args["-o"],"w",encoding="utf8") as f:
		f.write(url + ';"%s"'*2 % (paragraph.replace('"','""'),quoted.replace('"','""')))