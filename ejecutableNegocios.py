import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.by import By

class Navegator:
    def __init__(self, DEBUG):
        if DEBUG:
            self.ruta = 'chromedriver.exe' 
        else:
            self.ruta = ChromeDriverManager().install()
        
    def iniciar_chrome(self):
        options = Options()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1000,1000")
        # options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disbale-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        # options.add_argument("--no-proxy-server")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # PARAMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
        exp_opt = [
                    "enable-automation",
                    "ignore-certificate-errors",
                    "enable-logging"
                ]
        options.add_experimental_option("excludeSwitches", exp_opt)
        # PARAMETROS QUE DEFINEN PREFERENCIAS EN CHROMEDRIVER
        pref={
            "profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": ["es-ES", "es"],
            "credentials_enable_service": False
        }
        options.add_experimental_option("prefs", pref) 

        s = Service(self.ruta)
        driver = webdriver.Chrome(service=s, options=options)
        # driver = webdriver.Chrome(options=options)
        
        return driver

def Search_New_URLs(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ul.ant-list-items p")))
    enterprises = driver.find_elements(By.CSS_SELECTOR, "li.ant-list-item")
    for enterprise in enterprises:
        enterprise_bd = {}
        # print('link: ' + enterprise.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))
        enterprise_bd['link'] = enterprise.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        name = enterprise.find_element(By.CSS_SELECTOR, "p.font-bold").text
        # print('name: ' + name)
        enterprise_bd['name'] = name
        dir = enterprise.find_element(By.CSS_SELECTOR, "p.text-xs").text
        # print('dir: ' + dir)
        enterprise_bd['dir'] = dir
        extras = enterprise.find_elements(By.CSS_SELECTOR, "div.mt-1")
        enterprise_bd['Activity'] = []     
        for extra in extras:
            tag = extra.find_element(By.CSS_SELECTOR, "path")
            if "M6 0C2" in tag.get_attribute("d"):
                # print("Muni: " + extra.text)
                enterprise_bd['Muni'] = extra.text     
            if "M908 640H8" in tag.get_attribute("d"):
                # print("Type: " + extra.text)
                enterprise_bd['Type'] = extra.text     
            if "M938 458" in tag.get_attribute("d"):
                # print("Tag: " + extra.text)
                enterprise_bd['Activity'].append(extra.text)     
        # print('')
        list_enterprise.append(enterprise_bd)
        

list_enterprise =[]

with open('info.json', 'r', encoding='utf-8') as f:
    list_enterprise = json.load(f)
    
nav = Navegator(DEBUG=True)
driver = nav.iniciar_chrome()


for i in range(5260, 24992):
    while(True):
        try:
            Search_New_URLs('https://www.negocioscuba.cu/directorio-de-empresas?page=' + str(i))
            break
        except:
            pass
    if i%20 == 0:
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(list_enterprise, f, ensure_ascii=False, indent=4)
with open('info.json', 'w', encoding='utf-8') as f:
    json.dump(list_enterprise, f, ensure_ascii=False, indent=4)