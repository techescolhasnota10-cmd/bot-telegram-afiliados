import requests
import time
import random

BOT_TOKEN = "8551742735:AAF_OTF8mP0L5K6NeVHy-YO4vI2CR-vADtg"
CHAT_ID = "-1003417235710"

produtos = [
    {
        "nome": "Mouse Gamer RGB 7200 DPI",
        "preco": "R$ 79,90",
        "link": "https://s.click.aliexpress.com/e/_c4FflhXp",
        "imagem": "https://i.imgur.com/4M7IWwP.jpg"
    },
    {
        "nome": "Teclado Mecânico Gamer LED",
        "preco": "R$ 199,90",
        "link": "https://s.click.aliexpress.com/e/_c4FflhXp",
        "imagem": "https://i.imgur.com/J5LVHEL.jpg"
    }
]

def postar_produto():
    produto = random.choice(produtos)
    legenda = (
        f"🔥 {produto['nome']}\n"
        f"💰 {produto['preco']}\n"
        f"👉 {produto['link']}\n\n"
        "#tecnologia #gaming #pc #afiliados"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": produto["imagem"],
        "caption": legenda
    })

print("🤖 Bot iniciado...")
while True:
    postar_produto()
    time.sleep(60)  # posta a cada 1 minuto (teste)
