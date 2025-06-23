from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_imovirtual():
    url = "https://www.imovirtual.com/pt/resultados/comprar/apartamento/lisboa/lisboa?viewType=listing"

    print("🚀 Iniciando navegador...")

    options = Options()
    options.headless = False
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    print("⏳ Esperando anúncios carregarem...")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-cy='listing-item-link']"))
        )
        print("✅ Página carregada com sucesso!")
    except Exception as e:
        print("⚠️ Timeout esperando os anúncios:", e)
        driver.quit()
        return

    time.sleep(3)

    anuncios = driver.find_elements(By.CSS_SELECTOR, "a[data-cy='listing-item-link']")
    print(f"🔍 {len(anuncios)} anúncios encontrados!")

    imoveis = []

    for anuncio in anuncios:
        try:
            text = anuncio.text.strip()
            linhas = text.split("\n")
            titulo = linhas[0] if linhas else "Sem título"
            preco = next((linha for linha in linhas if "€" in linha), "Preço não encontrado")
            link = anuncio.get_attribute("href")

            print(f"🏠 {titulo} | 💰 {preco}")
            imoveis.append({
                "Título": titulo,
                "Preço": preco,
                "Link": link
            })

        except Exception as e:
            print("⚠️ Erro em um item:", e)
            continue

    driver.quit()

    if imoveis:
        pd.DataFrame(imoveis).to_csv("imovirtual_imoveis.csv", index=False)
        print(f"\n✅ {len(imoveis)} imóveis salvos em imovirtual_imoveis.csv")
    else:
        print("⚠️ Nenhum imóvel salvo.")

scrape_imovirtual()
