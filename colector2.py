#import socks #PySocks
#import socket
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
	system("nohup ssh " + user + "@" + ip + " -ND " + str(porta) + " > /dev/null &")
	sleep(4)
def pesquisa(dork):
	dork = removeCRLF(dork)
	payload = {'lr' : 'lang_pt', 'tbs' : 'qdr:y','q' : dork}
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
		links = soup.findAll("h3", {"class" : "r"})
		if not links:
			print("[+] Chegou ao fim da pesquisa")
			return 0
		for merda in links:
			googleResult = str(merda.a)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', googleResult)
			for urlFromGoogle in urls:
				print("[+] Coletando de -> [" + urlFromGoogle + "]")
				req = Request(urlFromGoogle, headers = header)
				try:
					str1 = str(urlopen(req, timeout = 30).read())
				except:
					print("[-] Erro ao acessar url")
					continue
				str1 = limpaHTML(str1)
				emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str1)
				txtEmails = open("emailsDoGoogle.txt", "a+")
				for email in emails:
					print("[+] Email -> [" + email + "]")
					txtEmails.write(email + "\n")
				txtEmails.close()
	return 0
header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
pesquisa('site:br "@hotmail.com" "@gmail.com" -"@yahoo.com.br" ext:asp')
"""
arquivoComAsDork = "dorks.txt"
ips = []
arq = open(arquivoComAsDork, 'r')
todasAsDorks = arq.readlines()
arq.close()
mudaIPSocks5("127.0.0.1", 8080)
ipAtual = 0
quantidadeIP = 8
criaTunelSSH("socks", ips[ipAtual], 8080)
for dorkAtual in todasAsDorks:
	pesquisa(dorkAtual)
	if(quantidadeIP-1 > ipAtual):
		ipAtual += 1
		criaTunelSSH("socks", ips[ipAtual], 8080)
	else:
		ipAtual = 0
		criaTunelSSH("socks", ips[ipAtual], 8080)

print("[+] Fim de tudo!")"""
