import socks #PySocks
import socket
from os import system
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.parse import urlencode, quote_plus
from threading import Thread
import re
todasAsUrls = set()

def limpaHTML(data):
	data = data.replace('\n', " ")
	data = data.replace('\r', " ")
	data = data.replace('\\n', " ")
	data = data.replace('\\r', " ")
	data = data.replace('"', " ")
	data = data.replace(',', " ")
	data = data.replace("'", " ")
	return data

def removeCRLF(data):
	data = data.replace('\n', "")
	data = data.replace('\r', "")
	return data

def mudaIPSocks5(ip, porta):
	socks.set_default_proxy(socks.SOCKS5, ip, porta)
	socket.socket = socks.socksocket

def criaTunelSSH(user, ip, porta):
	system("killall ssh")
	print("[+] Abrindo tunel com " + ip)
	system("nohup ssh -i m4.pem " + user + "@" + ip + " -ND " + str(porta) + " > /dev/null &")
	sleep(4)
def pesquisa(dork):
	dork = removeCRLF(dork)
	dorkAtual = open("dorkAtual.txt", "w")
	dorkAtual.write(dork)
	dorkAtual.close()
	payload = {'lr' : 'lang_pt', 'q' : dork}
	print("[+] Tentando pesquisar por [" + dork + "]")
	for i in range(0,1000,10):
		result = urlencode(payload, quote_via=quote_plus)
		url = "https://www.google.com.br/search?" + result + "&start="
		url2 = url + str(i) + "&sa=N&biw=1280&bih=1316"
		req = Request(url2, headers=header)
		try:
			html = urlopen(req)
		except:
			print("[-] Erro ao tentar pesquisar no Google")
			return -1
		soup = BeautifulSoup(html)
		links = soup.findAll("div", {"class" : "r"}, "a")
		if not links:
			print("[+] Chegou ao fim da pesquisa")
			return 0
		for merda in links:
			googleResult = str(merda.a)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', googleResult)
			for urlFromGoogle in urls:
				if(urlFromGoogle.find("&amp") != -1 or urlFromGoogle.find("</cite>") != -1 or urlFromGoogle.find(".../") != -1):
					continue
				if(urlFromGoogle in todasAsUrls):
					print("[-] Url ja foi acessada!")
					continue
				else:
					todasAsUrls.add(urlFromGoogle)
					listaUrls = open("listaUrls.txt", "a")
					listaUrls.write(urlFromGoogle + "\n")
					listaUrls.close()
				print("[+] Coletando de -> [" + urlFromGoogle + "]")
				system("nohup wget '" + urlFromGoogle + "' > /dev/null &")

	return 0
try:
	with open('listaUrls.txt', 'r') as f:
		for url in f:
			url = removeCRLF(url)
			todasAsUrls.add(url)
		print("[+] Lista carregada com sucesso!")
except IOError:
	print("[-] Lista nao encontrada")

header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
arquivoComAsDork = "dork2.txt"
ips = []
arq = open(arquivoComAsDork, 'r')
todasAsDorks = arq.readlines()
arq.close()
mudaIPSocks5("127.0.0.1", 8080)
ipAtual = 0
quantidadeIP = len(ips)
criaTunelSSH("ubuntu", ips[ipAtual], 8080)
for dorkAtual in todasAsDorks:
	pesquisa(dorkAtual)
	if(quantidadeIP-1 > ipAtual):
		ipAtual += 1
		criaTunelSSH("ubuntu", ips[ipAtual], 8080)
	else:
		ipAtual = 0
		criaTunelSSH("ubuntu", ips[ipAtual], 8080)

print("[+] Fim de tudo!")
