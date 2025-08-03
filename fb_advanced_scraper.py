#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import logging
import json
from datetime import datetime
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service

CONFIG = {
    "HEADLESS": False,
    "MAX_SCROLLS": 3,
    "SCROLL_PAUSE_MIN": 1.5,
    "SCROLL_PAUSE_MAX": 3.0,
    "PAGE_LOAD_WAIT_MIN": 3,
    "PAGE_LOAD_WAIT_MAX": 6,
    "RANDOM_UA_LIST": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/15.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    ],
    "PROXY_LIST": []
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("FB_AdvancedScraper")

def get_random_user_agent():
    return random.choice(CONFIG["RANDOM_UA_LIST"])

def get_random_proxy():
    return random.choice(CONFIG["PROXY_LIST"]) if CONFIG["PROXY_LIST"] else None

def human_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))

def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    ua = get_random_user_agent()
    chrome_options.add_argument(f"user-agent={ua}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1200, 800)
    return driver

def login_facebook(driver, email, password):
    try:
        logger.info("Iniciando sesión en Facebook...")
        driver.get("https://www.facebook.com/login")
        human_sleep(2, 4)

        email_input = driver.find_element(By.ID, "email")
        pass_input = driver.find_element(By.ID, "pass")
        login_btn = driver.find_element(By.NAME, "login")

        email_input.send_keys(email)
        pass_input.send_keys(password)
        human_sleep(1, 2)
        login_btn.click()
        human_sleep(5, 7)

        if "login" in driver.current_url or "checkpoint" in driver.current_url:
            logger.error("No se pudo iniciar sesión. Verificá las credenciales o el CAPTCHA.")
            return False

        logger.info("Sesión iniciada correctamente.")
        return True

    except ElementNotInteractableException as e:
        logger.error(f"No se pudo interactuar con un campo de login: {e}")
        return False
    except Exception as e:
        logger.error(f"Error durante el login: {e}")
        return False

def scroll_down(driver, times=1):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_sleep(CONFIG["SCROLL_PAUSE_MIN"], CONFIG["SCROLL_PAUSE_MAX"])

def scrape_facebook_public(url, email, password):
    driver = None
    data = {}
    try:
        driver = init_driver(headless=CONFIG["HEADLESS"])
        if not login_facebook(driver, email, password):
            data['error'] = "No se pudo iniciar sesión."
            return data

        driver.get(url)
        logger.info(f"Accediendo a: {url}")
        human_sleep(CONFIG["PAGE_LOAD_WAIT_MIN"], CONFIG["PAGE_LOAD_WAIT_MAX"])
        scroll_down(driver, times=CONFIG["MAX_SCROLLS"])
        data['title'] = driver.title

        try:
            about_section = driver.find_element(By.XPATH, "//div[contains(text(),'Información')]")
            about_section.click()
            human_sleep(2, 4)
            data['about_html'] = driver.page_source
        except NoSuchElementException:
            data['about_html'] = "No se encontró sección 'Información'."
        except Exception as e:
            data['about_html'] = f"Error accediendo a 'Información': {str(e)}"

        posts_html = []
        try:
            posts = driver.find_elements(By.XPATH, "//div[@role='article']")
            for idx, post in enumerate(posts, start=1):
                post_text = post.text
                snippet = post_text[:200] + ("..." if len(post_text) > 200 else "")
                posts_html.append(f"Post #{idx}: {snippet}")
        except Exception as e_posts:
            logger.warning(f"No se pudieron extraer posts: {e_posts}")

        data['posts'] = posts_html
        logger.info("Scraping finalizado.")

    except Exception as e:
        logger.error(f"Error durante el scraping: {e}")
        data['error'] = str(e)
    finally:
        if driver:
            driver.quit()
    return data

def guardar_resultados(resultados):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_file = f"resultados_fb_scraper_{timestamp}.txt"
    json_file = f"resultados_fb_scraper_{timestamp}.json"

    with open(txt_file, "w", encoding="utf-8") as f:
        for k, v in resultados.items():
            f.write(f"{k.upper()}:\n")
            if isinstance(v, list):
                for item in v:
                    f.write(f"  - {item}\n")
            else:
                f.write(f"{v}\n")
            f.write("\n")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    logger.info(f"Resultados guardados en:\n - {txt_file}\n - {json_file}")

if __name__ == "__main__":
    print("=============================")
    print("  FB ADVANCED SCRAPER  ")
    print("   Fines Educativos")
    print("=============================")
    print("\n[INFO] Revisar TOS de Facebook.")
    fb_email = input("Correo de Facebook: ").strip()
    fb_pass = getpass("Contraseña de Facebook: ")
    fb_url = input("URL pública de perfil/página FB: ").strip()
    resultado = scrape_facebook_public(fb_url, fb_email, fb_pass)

    print("\n=== RESULTADOS OBTENIDOS ===")
    for k, v in resultado.items():
        if isinstance(v, str):
            snippet = v[:300]
            snippet += "..." if len(v) > 300 else ""
            print(f"{k.upper()}: {snippet}")
        else:
            print(f"{k.upper()}:")
            for item in v:
                print(f"  - {item}")
    guardar_resultados(resultado)
    print("\n[FIN DEL SCRIPT]")

