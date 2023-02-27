import warnings
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

from time import sleep
import pandas as pd
import re
import numpy as np
import random
T_MIN = 1
T_MAX = 2

# RECUPERATION MANUELLE DES DONNEES #
# Instancitation du webdriver
try:
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())



    # Ouverture d'une page TrustPilot
driver.get('https://fr.trustpilot.com/')
sleep(3)  # temps d'attente pour les cookies se chargent
    # Fermeture des cookies
webelement = driver.find_element(by='id', value='onetrust-reject-all-handler')
webelement.click()
    # à la fin de cette fonction on a trust pilot d'ouvert et les cookie ont été fermés
webelement = driver.find_element(by='class name', value='styles_searchInputField__Ltvjz')
webelement.click()

webelement.send_keys('www.showroomprive.com')

webelement.send_keys(Keys.ENTER)
sleep(3)
#avis_moyen = driver.find_element(by='class name', value="typography_heading-m__T_L_X typography_appearance-default__AAY17")  # on obtient un élément unique : logique
#nb_total_avis = driver.find_element(by='class name', value="typography_body-l__KUYFJ typography_appearance-default__AAY17")  # on obtient une liste avec les 20 sociétés de la page
"""prct_1_etoile = driver.find_element(by='class name', value="")
prct_2_etoile = driver.find_element(by='class name', value="")
prct_3_etoile = driver.find_element(by='class name', value="")
prct_4_etoile = driver.find_element(by='class name', value="")
prct_5_etoile = driver.find_element(by='class name', value="")"""
sleep(3)
note_moyenne = driver.find_elements(by='class name', value="styles_header__yrrqf")
print("note_moyenne : ", note_moyenne)
#




"""

liste_notation_etoile = driver.find_elements(by='class name', value="styles_row__wvn4i")
print(len(liste_notation_etoile))
print(liste_notation_etoile[0].text)
print()
print(liste_notation_etoile[1].text)
print()
print(liste_notation_etoile[2].text)
print()
print(liste_notation_etoile[3].text)
print()
print(liste_notation_etoile[4].text)"""

sleep(3)
titres = driver.find_elements(by='class name', value="styles_cardWrapper__LcCPA")
print(len(titres))
title_comment_personne = titres[0].find_element(by='class name', value="typography_heading-s__f7029").text
print(title_comment_personne)

"""
webelement = driver.find_element(by='name', value='pagination-button-next')
sleep(3)
webelement.click()
sleep(3)
driver.back()"""

var = driver.find_elements(by='class name', value="styles_content__Hl2Mi")
var2 = var[1].find_element(by='class name', value="typography_body-m__xgxZ_")
"""var = driver.find_elements(by='class name', value="typography_body-m__xgxZ_")
var2 = var[1].find_element(by='class name', value="typography_body-m__xgxZ_").text"""
#typography_body-m__xgxZ_
print(len(var))
print(var2.text)

#paper_paper__1PY90
#styles_content__Hl2Mi
var = driver.find_elements(by='class name', value="styles_cardWrapper__LcCPA")
var2 = var[0].find_element(by='class name', value="paper_paper__1PY90")
var3 = var[0].find_element(by='class name', value="typography_body-m__xgxZ_")


print("Le/la client(e) à posté : ",var3.text)
#star-rating_starRating__4rrcf
print(len(var))
if "var2" in locals() or "var2" in globals():
    print("Showroomprive à repondu")
else:
    print("Showroomprive n'a pas répondu")

liste_commentaire = driver.find_elements(by='class name', value="styles_reviewContentwrapper__zH_9M")
print(len(liste_commentaire))
commentaire = liste_commentaire[0].find_element(by='class name', value="typography_body-l__KUYFJ")
print("L'avis est : ", commentaire.text)
    # for checking existence in locals() function
for i in range(len(liste_commentaire)):
    liste_commentaire = driver.find_elements(by='class name', value="styles_reviewContentwrapper__zH_9M")
    print(liste_commentaire[i].find_element(by='class name', value="typography_body-l__KUYFJ").text)

#a = driver.find_element(By.xpath("img[@alt='Rated 5 out of 5 stars']"))
#a = driver.find_element_by_xpath('//img[@alt="Rated 5 out of 5 stars"]')
#print("taille de a", a)


"""
for i in range(len(notes)):
    notes = driver.find_elements(by='class name', value="styles_reviewContentwrapper__zH_9M")
    note1 = notes[i].find_element(By.XPATH, "//img[@alt='Noté 3 sur 5 étoiles']")
    #notes2 = notes[i].find_element(By.XPATH, "//img[@alt='Noté 2 sur 5 étoiles']")
    if "note1" in locals() or "note1" in globals():
        print("La note de l'avis est inférieure ou égale à 2")
    else:
        print("La note est supérieur à 2")"""




"""
webelement = driver.find_element(by='name', value='pagination-button-next')
webelement.click()
sleep(3)
for i in range(len(liste_commentaire)):
    liste_commentaire = driver.find_elements(by='class name', value="styles_reviewContentwrapper__zH_9M")
    print(liste_commentaire[i].find_element(by='class name', value="typography_body-l__KUYFJ").text)

driver.back()"""




#problème ici

notes = driver.find_elements(by='class name', value="styles_reviewContentwrapper__zH_9M")
note1 = notes[0].find_element(By.XPATH, "//img[@alt]")
print(note1)




sleep(1000)