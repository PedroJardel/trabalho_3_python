from bs4 import BeautifulSoup
import requests
import re

import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"}

url_kabum = "https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100&facet_filters=&sort=most_searched"

kabum = requests.get(url_kabum, headers=headers)

html_kabum = BeautifulSoup(kabum.content, "html.parser")

produtos_Kabum = html_kabum.find_all("div", class_="sc-d55b419d-11 jSCrcV")

list_prod_Kabum = []

for produto in produtos_Kabum:
    titulo = produto.find("span", class_="sc-d99ca57-0 kUQyzS sc-d55b419d-16 fMikXK nameCard").get_text().split(",")[0]
    preco_string = produto.find("span", class_="sc-3b515ca1-2 gybgF priceCard").get_text().split(",")
    preco = re.sub(r"[^0-9]", "", preco_string[0])
    list_prod_Kabum.append({ "titulo": titulo, "preco": float(preco)})

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
link = "https://www.magazineluiza.com.br/placa-de-video/informatica/s/in/pcvd/"

navegador.get(link)

sleep(3)

html_magalu = BeautifulSoup(navegador.page_source, "html.parser")

produtos_magalu = html_magalu.find_all("div", attrs= { "data-testid": "product-card-content"})

list_prod_magalu = []

for produto in produtos_magalu:
    titulo = produto.find("h2", attrs={"data-testid": "product-title"}).get_text().split(",")[0]
    preco_string = produto.find("p", attrs={"data-testid": "price-value"}).get_text().split(",")
    preco = re.sub(r"[^0-9]", "", preco_string[0])
    list_prod_magalu.append({ "titulo": titulo, "preco": float(preco)})

todos_list = []

for placa in list_prod_Kabum:
    todos_list.append({"titulo": placa['titulo'], "preco": placa['preco']})

for placa in list_prod_magalu:
    todos_list.append({"titulo": placa['titulo'], "preco": placa['preco']})

def titulo_opcao (msg, traco="="):
    print(traco*50)
    print(msg)
    print( traco*50)

def lista_Kabum():
    titulo_opcao("Placas de Vídeo na Kabum")
    print("Modelo...................................................................................:Preço(R$)")
    for produto in list_prod_Kabum:
        print(f"{produto['titulo']:89s} {locale.currency(produto['preco'], grouping=True, symbol=True)}")

def lista_magalu():
    titulo_opcao("Placas de Vídeo na Magalu")
    print("Modelo..............................................................................................:Preço(R$)")
    for produto in list_prod_magalu:
        print(f"{produto['titulo']:100s} {locale.currency(produto['preco'], grouping=True, symbol=True)}")

def lista_todos_unique():
    todos = set()

    for placa in list_prod_Kabum:
        todos.add(placa['titulo'])

    for placa in list_prod_magalu:
        todos.add(placa['titulo'])

    lista = sorted(list(todos))

    titulo_opcao("Todas as placas de vídeo únicas à venda")

    for placa in lista:
        if str(placa).startswith("Placa de Vídeo" or "Placa De Vídeo"):
            print(placa)

def lista_todos_decrescente():
    lista_preco = sorted(todos_list, key=lambda placa: placa['preco'], reverse=True)

    titulo_opcao("Todas as placas de vídeo à venda")

    print("Modelo..............................................................................................:Preço(R$)")
    for produto in lista_preco:
        print(f"{produto['titulo']:100s} {locale.currency(produto['preco'], grouping=True, symbol=True)}")

def media_preco():
    subtotal = 0
    num = 0

    for placa in todos_list:
        num += 1
        subtotal += float(placa['preco'])

    titulo_opcao("Média de Preço das Placas de Vídeo")
    print("Quantidade...................:Media(R$)")
    print(f"{num: <29} R${locale.currency((subtotal/num), grouping=True, symbol=True)}")

def pesq_nome():
    nome = input("Digite o nome da placa de vídeo(Ex: RTX 3060, RX 6600, GTX 1060): ").upper()

    print("Modelo..............................................................................................:Preço(R$)")
    for produto in todos_list:
        if nome in produto['titulo'].upper():
            print(f"{produto['titulo']:100s} {locale.currency(produto['preco'], grouping=True, symbol=True)}")


while True:
    titulo_opcao("Comparador de Placas de Vídeo")    
    print("1. Placas da Kabum")
    print("2. Placas da Magalu")
    print("3. Todos as Placas")
    print("4. Todas as Placas em Ordem Decrescente de preço") 
    print("5. Média de Preço das Placas de Vídeo")
    print("6. Pesquisa por Nome")
    print("7. Finalizar")    
    opcao = int(input("Opção: "))
    match (opcao):
        case 1:
            lista_Kabum()
        case 2:
            lista_magalu()
        case 3:
            lista_todos_unique()
        case 4:
            lista_todos_decrescente()
        case 5:
            media_preco()
        case 6:
            pesq_nome()
        case _:
            titulo_opcao("Obrigado por utilziar o nosso comparador")
            break