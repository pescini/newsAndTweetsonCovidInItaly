import sys, getopt, re
from bs4 import BeautifulSoup


def main(argv):
	file = None
	try:
		opts, args = getopt.getopt(argv,"f:",["file="])
	except getopt.GetoptError:
		print("ERROR")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-f", "--file"):
			file = arg
	return file

if __name__ == "__main__":
	file = main(sys.argv[1:])
	rank = 1 + 10*( int(file[7:-5]) - 1)
	
	with open("HTML/"+file,"r",encoding="utf8") as f:
		data = f.read()
	
	list = re.search('<!-- risultati -->(.|\n)+<!-- /risultati -->', data).group(0)
	article = [x.group(0) for x in re.finditer('<article>(.|\n)+?</article>', list)]
	
	length = len(article)
	i = 0
	with open("temp.csv","w",encoding="utf8") as f:
		while i < length:
			line = [''] * 7
			line[0] = str(rank+i)
			line[1] = re.search('href="(.*?)\?ref=search' ,article[i]).group(1)
			line[3] = '"%s"' % re.search('articolo" >((.|\n)*?)</a></h1>', article[i]).group(1).strip().replace('"','""')
			line[5] = re.search('<time datetime="(.*?)">' ,article[i]).group(1)
			line[6] = re.search('class="section">sez\. (.*?)</span>' ,article[i]).group(1)
			try:
				soup = BeautifulSoup(re.search('<p>((.|\n)*?)</p>', article[i]).group(1), "html.parser")
				line[4] = '"%s"' % soup.get_text().replace("→","").strip().replace('"','""').replace("\n"," ")
			except Exception:
				pass
			try:
				line[2] = re.search('<em class="author">di (.*?)</em>', article[i]).group(1)
			except Exception:
				pass
			
			f.write(";".join(line)+"\n")
			i+=1
