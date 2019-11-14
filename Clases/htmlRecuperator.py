#   *************************************                                 
#   **                                 **
#   **       autor: Alonzo joseph      **
#   **        fecha: 18/10/2019        **
#   **               UTM               **
#   **                                 **
#   *************************************
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox
import sys

class HtmlRecuperator():
    def __init__(self, url, ventana):
        self.url = url
        self.html = ""
        self.svg = ""
        self.getDom(ventana)

    def getDom(self, ventana):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')
        driver.get(self.url)
        try:
            self.svg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "print-sheet"))
            )
            self.svg = self.svg.get_attribute('innerHTML')
        except:
            driver.quit()
            s = str(sys.exc_info()[0])
            if s == "<class 'selenium.common.exceptions.TimeoutException'>":
                s = "Tiempo limite de respuesta agotado \n \"TimeoutException\" \nRevise su conexión a internet"
            else:
                s = "Ocurrio un error"
            tk.messagebox.showerror(parent=ventana, message= s, title="Error")
        finally:
            driver.quit()

    def getSvg(self):
        return self.svg