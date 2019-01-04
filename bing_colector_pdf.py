from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode, quote_plus
from threading import Thread, Lock
from re import compile
from fileinput import input, hook_encoded
from requests import get
from hashlib import md5

todasAsUrls = set()

def carregaDorks():
	linhas = input(openhook=hook_encoded("ISO-8859-1"))
	dorks = []
	for linha in linhas:
		dorks.append(removeCRLF(linha))
	return dorks

def pegaPDF(url):
	header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	try:
		pdf = get(url, headers = header)
	except:
		return
	with open("saida/pdf_bolado_" + md5(url.encode('utf-8')).hexdigest() + ".pdf", "wb") as f:
		f.write(pdf.content)

def removeCRLF(data):
	data = data.rstrip('\n')
	data = data.rstrip('\r')
	return data

def pesquisa(dork):
	areaCriticaURL = Lock()
	urlRE = compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	for i in range(0,1000,10):
		payload = {'q' : dork, 'first' : i}
		result = urlencode(payload, quote_via=quote_plus)
		url = "https://www.bing.com/search?" + result
		req = Request(url, headers=header)
		try:
			html = urlopen(req)
		except:
			print("[-] Erro ao tentar pesquisar no Bing")
			return
		soup = BeautifulSoup(html, "html.parser")
		htmlParse = soup.findAll("li", {"class" : "b_algo"}, "h2")
		if not htmlParse:
			return
		urlJobs = []
		urlJobs_append = urlJobs.append #Codigo otimizado
		urlRE_findall = urlRE.findall #Codigo otimizado
		urls = urlRE_findall(str(htmlParse)) #Codigo otimizado
		for url in urls:
			if(url.find("&amp") != -1 or url.find("<") != -1 or url.find("...") != -1 ):
				continue
			with areaCriticaURL:
				if(url in todasAsUrls):
					continue
				else:
					todasAsUrls.add(url)
					listaUrls = open("listaUrls.txt", "a")
					listaUrls.write(url + "\n")
					listaUrls.close()
			req = Request(url, headers = header)
			urlJobs_append(Thread(target=pegaPDF, args=(url,))) #Codigo otimizado
			urlJobs[-1].daemon = True
			urlJobs[-1].start()
		for threadURL in urlJobs:
			threadURL.join()

def carregaBaseDeURL():
	try:
		with open('listaUrls.txt', 'r') as f:
			for url in f:
				url = removeCRLF(url)
				todasAsUrls.add(url)
			print("[+] Lista de URL's carregada!")

	except IOError:
		print("[-] Lista nao encontrada, uma nova lista vai ser criada")


def main():
	carregaBaseDeURL()
	todasAsDorks = []
	t = []
	t_append = t.append #Codigo otimizado
	numeroThread = 100
	todasAsDorks = carregaDorks()
	contaThread = 1
	for dorkAtual in todasAsDorks:
		t_append(Thread(target=pesquisa, args=(dorkAtual,))) #Codigo otimizado
		t[-1].daemon = True
		t[-1].start()
		if(contaThread >= numeroThread):
			for th in t:
				th.join()
			t = []
			t_append = t.append #Codigo otimizado
			contaThread = 1
		else:
			contaThread += 1

		txtDork = open("dorkAtual.txt", "w")
		txtDork.write(dorkAtual + "\n")
		txtDork.close()
	print("[+] Fim de tudo!")

main()
