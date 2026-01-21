import requests
from bs4 import BeautifulSoup
import schedule
import time
import random
import json
import os

# ==================== CONFIGURAÇÕES ==================== #
BOT_TOKEN = '8551742735:AAF_OTF8mP0L5K6NeVHy-YO4vI2CR-vADtg'      # Token do seu bot
CHAT_ID = '-1003417235710'                # @username do seu canal público
AFILIADO_ID = '2009200720011'      # Seu ID de afiliado

POSTS_POR_DIA = 10
HORAS_ENTRE_POSTS = 2
CATEGORIA = 'mouses'
HASHTAGS = "#tecnologia #pc #gaming #hardware #afiliados"
ARQUIVO_POSTADOS = 'postados.json'

# ==================== FUNÇÕES ==================== #
def pegar_produtos():
    url = f'https://www.aliexpress.com/category/100003109/{CATEGORIA}.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        produtos = []
        items = soup.select('a[data-tracking]')[:50]
        for item in items:
            nome = item.get('title')
            link = item.get('href')
            imagem_tag = item.select_one('img')
            imagem = imagem_tag['src'] if imagem_tag else ''
            avaliacao_tag = item.select_one('span[title]')
            avaliacao = float(avaliacao_tag['title'].split()[0]) if avaliacao_tag else 0
            vendas_tag = item.select_one('span.sold-count')
            vendas = int(vendas_tag.text.replace(' sold','').replace(',','')) if vendas_tag else 0
            link_afiliado = f"{link}?aff_id={AFILIADO_ID}"
            if nome and link:
                produtos.append({
                    'nome': nome,
                    'link': link_afiliado,
                    'imagem': imagem,
                    'avaliacao': avaliacao,
                    'vendas': vendas
                })
        produtos.sort(key=lambda x: (x['avaliacao'], x['vendas']), reverse=True)
        return produtos
    except:
        return []

def carregar_postados():
    if os.path.exists(ARQUIVO_POSTADOS):
        with open(ARQUIVO_POSTADOS, 'r') as f:
            return json.load(f)
    return []

def salvar_postado(produto):
    postados = carregar_postados()
    postados.append(produto['link'])
    with open(ARQUIVO_POSTADOS, 'w') as f:
        json.dump(postados, f)

def produto_ja_postado(produto):
    return produto['link'] in carregar_postados()

def gerar_legenda(produto):
    frases = [
        f"🔥 Produto top: {produto['nome']}",
        f"💰 {produto['vendas']} vendidos! Aproveite!",
        f"🎯 Avaliado com {produto['avaliacao']}⭐, ideal para gamers!",
        f"🚀 Não perca: {produto['nome']}"
    ]
    frase = random.choice(frases)
    return f"{frase}\nAvaliação: {produto['avaliacao']}⭐\nVendas: {produto['vendas']}\nLink: {produto['link']}\n{HASHTAGS}"

def postar_produto():
    produtos = pegar_produtos()
    if not produtos:
        return
    produtos_nao_postados = [p for p in produtos if not produto_ja_postado(p)]
    if not produtos_nao_postados:
        return
    produto = random.choice(produtos_nao_postados)
    descricao = gerar_legenda(produto)
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={'chat_id': CHAT_ID, 'caption': descricao},
            files={'photo': requests.get(produto['imagem']).content} if produto['imagem'] else None
        )
        if response.status_code == 200:
            print(f"Produto postado: {produto['nome']}")
            salvar_postado(produto)
    except Exception as e:
        print("Erro ao postar:", e)

# ==================== AGENDAMENTO AUTOMÁTICO ==================== #
for i in range(POSTS_POR_DIA):
    schedule.every(HORAS_ENTRE_POSTS * i).hours.do(postar_produto)

print("Bot iniciado! Postando automaticamente...")
while True:
    schedule.run_pending()
    time.sleep(10)
