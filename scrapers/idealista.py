import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    url = "https://www.idealista.pt/comprar-casas/lisboa/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    imoveis = []

    for item in soup.select("article"):
        titulo_tag = item.select_one("a.item-link")
        preco_tag = item.select_one(".item-price")

        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "N/A"
        preco = preco_tag.get_text(strip=True) if preco_tag else "N/A"
        link = "https://www.idealista.pt" + titulo_tag['href'] if titulo_tag and 'href' in titulo_tag.attrs else "N/A"

        imoveis.append({
            "Título": titulo,
            "Preço": preco,
            "Link": link
        })

    print(f"{len(imoveis)} imóveis encontrados.")

    df = pd.DataFrame(imoveis)
    df.to_csv("idealista_imoveis.csv", index=False)
    print("Dados salvos em idealista_imoveis.csv")
