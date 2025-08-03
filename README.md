# 📘 FB Advanced Scraper 

**FB Advanced Scraper** es un script en **Python 3 + Selenium 4** que inicia sesión en Facebook con credenciales proporcionadas por el usuario y extrae información pública de un perfil o página:

* Título de la página/perfil  
* HTML bruto de la sección **“Información”**  
* Lista de los primeros *N* posts visibles tras hacer varios scrolls

> ⚠️ **Uso estrictamente educativo.**  
> Asegúrate de cumplir los Términos de Servicio de Facebook y la legislación local sobre scraping y privacidad. Ejecuta el script **solo** en cuentas, perfiles o páginas sobre los cuales tengas autorización.

---

## ✨ Funciones principales

| Módulo                        | Descripción                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------------|
| **Login automatizado**        | Rellena email y contraseña, realiza el click de login y verifica que no quede en `/login` ni `/checkpoint`. |
| **User-Agent aleatorio**      | Elige un UA de una lista para evadir detección básica.                                         |
| **Scrolling humano**          | Realiza `MAX_SCROLLS` bajadas de página con pausas aleatorias configurables.                   |
| **Extracción de contenidos**  | • Título de la página <br>• HTML completo de “Información” <br>• Snippets de posts (`div[@role='article']`). |
| **Persistencia de resultados**| Guarda archivos `resultados_fb_scraper_<timestamp>.json` y `.txt` en el directorio actual.     |
| **Proxy opcional**            | Permite rotación sencilla de proxies HTTP/SOCKS añadiendo IP:PUERTO en `CONFIG["PROXY_LIST"]`. |

---

## 📋 Requisitos

| Dependencia      | Comando de instalación (Debian/Ubuntu/Parrot)                                     |
|------------------|-----------------------------------------------------------------------------------|
| **Python ≥ 3.8** | `sudo apt install python3 python3-venv`                                           |
| **Selenium 4**   | `pip install selenium==4.*`                                                       |
| **Google Chrome**| `sudo apt install google-chrome-stable` *(o usa Chromium)*                        |
| **ChromeDriver** | Debe coincidir con la versión de Chrome. Ejemplo:<br>`wget https://chromedriver.storage.googleapis.com/$(google-chrome --version \| awk '{print $3}' \| cut -d. -f1)/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && sudo mv chromedriver /usr/bin/ && sudo chmod +x /usr/bin/chromedriver` |

---

## ⚙️ Configuración rápida

El comportamiento se controla desde el diccionario `CONFIG` dentro del script:

```python
CONFIG = {
    "HEADLESS": False,          # Mostrar o no la ventana del navegador
    "MAX_SCROLLS": 3,           # Cantidad de scrolls hacia abajo
    "SCROLL_PAUSE_MIN": 1.5,    # Pausa mínima entre scrolls
    "SCROLL_PAUSE_MAX": 3.0,    # Pausa máxima entre scrolls
    "PAGE_LOAD_WAIT_MIN": 3,    # Espera después de cargar una URL
    "PAGE_LOAD_WAIT_MAX": 6,
    "RANDOM_UA_LIST": [...],    # Lista de User-Agents
    "PROXY_LIST": []            # Lista opcional de proxies "IP:PUERTO"
}


git clone https://github.com/camilogamboa2024/fb_advanced_scraper.git

cd fb_advanced_scraper

python3 -m venv venv

source venv/bin/activate

pip install selenium==4.*

service = Service("/ruta/a/tu/chromedriver")


python3 fb_advanced_scraper.py


Correo de Facebook: <tu_correo>
Contraseña de Facebook: ********
URL pública de perfil/página FB: https://www.facebook.com/ejemplo

