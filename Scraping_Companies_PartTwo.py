# ----------- DEBUT DU PROJET FIL ROUGE : récupération des données sur le site TrustPilot -------------------
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from time import sleep, time
from selenium.webdriver.common.by import By
import pandas as pd
import re
import numpy as np
import random
T_MIN = 2
T_MAX = 3

# RECUPERATION MANUELLE DES DONNEES #
# Instancitation du webdriver
try:
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())


def open_trust_pilot_and_close_cookie():
    # Ouverture d'une page TrustPilot
    driver.get('https://fr.trustpilot.com/')
    sleep(random.uniform(T_MIN, T_MAX))  # temps d'attente pour les cookies se chargent
    # Fermeture des cookies
    webelement = driver.find_element(by='id', value='onetrust-reject-all-handler')
    webelement.click()
    # à la fin de cette fonction on a trust pilot d'ouvert et les cookie ont été fermés


def get_clic_category(company):
    """
    recherche de l'entreprise
    """
    webelement = driver.find_element(by='class name', value="styles_searchInputField__Ltvjz")
    webelement.click()
    sleep(random.uniform(T_MIN, T_MAX))
    webelement.send_keys(company)
    sleep(random.uniform(T_MIN, T_MAX))
    webelement.send_keys(Keys.ENTER)
    sleep(random.uniform(T_MIN, T_MAX))


def get_informations_general_company():
    """
    On va récupérer les informations générales sur la company : nom, note, avis
    """
    sleep(random.uniform(T_MIN, T_MAX))
    try:
        name_company = driver.find_element(by='class name', value="typography_display-s__qOjh6").text
    except:
        name_company = None
    try:
        pourcentage_5_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[0].text.split('\n')[-1]
    except:
        pourcentage_5_stars = None
    try:
        pourcentage_4_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[1].text.split('\n')[-1]
    except:
        pourcentage_4_stars = None
    try:
        pourcentage_3_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[2].text.split('\n')[-1]
    except:
        pourcentage_3_stars = None
    try:
        pourcentage_2_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[3].text.split('\n')[-1]
    except:
        pourcentage_2_stars = None
    try:
        pourcentage_1_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[4].text.split('\n')[-1]
    except:
        pourcentage_1_stars = None
    try:
        avis_number = driver.find_element(by='class name', value="styles_header__yrrqf").text.split(":")[-1].strip().replace(' ', ' ')
    except:
        avis_number = None
    try:
        avis_notation = driver.find_element(by='class name', value="styles_header__yrrqf").text.split("Total")[0].split("Avis")[-1].strip()
    except:
        avis_notation = None

    print("-->" + str(name_company))
    print("-->" + str(pourcentage_5_stars))
    print("-->" + str(pourcentage_4_stars))
    print("-->" + str(pourcentage_3_stars))
    print("-->" + str(pourcentage_2_stars))
    print("-->" + str(pourcentage_1_stars))
    print("-->" + str(avis_number))
    print("-->" + str(avis_notation))
    print()
    return name_company, pourcentage_5_stars, pourcentage_4_stars, pourcentage_3_stars, pourcentage_3_stars, \
           pourcentage_1_stars, avis_number, avis_notation


def get_informations_comments(list_comment, n, l1, l2, l3, l4, l5):
    """
    On va récupérer les informations du commentaire : titre / date / réponse au commentaire (boolean) / qui a répondu
    au commentaire / nombre d'étoile
    """
    # TITRE
    try:
        title_comment_personne = list_comment[n].find_element(by='class name', value="typography_heading-s__f7029").text
    except:
        title_comment_personne = None

    # DATE
    try:
        date_experience = list_comment[n].find_elements(by='class name', value="typography_body-m__xgxZ_")[4].text.split(":")[-1].strip(" ")
    except:
        date_experience = None
    print("--> Titre du commentaire : " + str(title_comment_personne))
    print("--> Date du commentaire : " + str(date_experience))
    rep_bool = True

    # REPONSE COMMENTAIRE
    try:  # si on y arrive c'est qu'il y a une réponse au commentaire
        Reponse_comment = list_comment[n].find_element(by='class name', value="styles_replyInfo__FYSje").text.split(" ")[2].split("\n")[0]
    except:
        print("--> Pas de réponse à ce commentaire")
        rep_bool = False
        Reponse_comment = None
    else:
        print("--> Il y'a une réponse à ce commentaire")
        print("--> La réponse a été fournie par : " + str(Reponse_comment))

    # NOMBRE D'ETOILE
    balise_int = list_comment[n].find_element(by='class name', value="star-rating_starRating__4rrcf")  # balise en amont
    star_number = 0
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 1 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 1
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 2 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 2
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 3 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 3
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 4 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 4
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 5 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 5
    print("--> Nombre d'étoile : " + str(star_number))
    print()
    # CONDITION SUR LE NOMBRE D ETOILE POUR AJOUTER LES INFORMATIONS
    if star_number <= 2:
        l1.append(title_comment_personne)
        l2.append(date_experience)
        l3.append(rep_bool)
        l4.append(Reponse_comment)
        l5.append(star_number)


def go_next_page():
    sleep(random.uniform(T_MIN, T_MAX))
    webelement = driver.find_element(by='name', value='pagination-button-next')
    driver.execute_script('arguments[0].click()', webelement)
    sleep(random.uniform(T_MIN, T_MAX))


def actions_fill_list(list_titre, list_date, list_response, list_who, list_stars):
    try:
        list_comment = driver.find_elements(by='class name', value="styles_cardWrapper__LcCPA")  # Liste des commentaire
    except:
        print("on a pas réussi à récupérer la liste des commentaire")
    else:
        for i in range(len(list_comment)):
            get_informations_comments(list_comment, i, list_titre, list_date, list_response, list_who, list_stars)


t0 = time()  # début du chronomètre
# CLIQUE SUR L'ENTREPRISE VOULUE
open_trust_pilot_and_close_cookie()
sleep(random.uniform(T_MIN, T_MAX))
get_clic_category("Showroomprive.com")

# RECUPERATION DES INFORMATIONS GENERALES DE LA COMPANY
sleep(random.uniform(T_MIN, T_MAX))
name_company, pou_5, pou_4, pou_3, pou_2, pou_1, avis_number, avis_notation = get_informations_general_company()

# REMPLISSAGE DF / CREATION DE CSV
dictionnaire_df = {'Name_company': [name_company],
                   'Pourcentage de 5 étoiles': [pou_5],
                   'Pourcentage de 4 étoiles': [pou_4],
                   'Pourcentage de 3 étoiles': [pou_3],
                   'Pourcentage de 2 étoiles': [pou_2],
                   'Pourcentage de 1 étoiles': [pou_1],
                   'Nombre avis': [avis_number],
                   "Notation": [avis_notation]}
df_company = pd.DataFrame(data=dictionnaire_df)
df_company.to_csv("infos_Showroom_general.csv")  # ON GARDERA T_MIN = 2 / T_MAX = 3


# RECUPERATION DES INFORMATIONS SUR LES COMMENTAIRES
list_titre = []
list_date = []
list_reponse_comment = []
list_reponse_comment_qui = []
list_stars = []
nombre_page = 100
for i in range(nombre_page):
    actions_fill_list(list_titre, list_date, list_reponse_comment, list_reponse_comment_qui, list_stars)
    print("Nombre de commentaire récupérés : " + str(len(list_titre)))
    print("Page : " + str(i+1) + " / " + str(nombre_page))
    ti = time() - t0  # heure intermédiaire
    print("Réalisé en {} secondes".format(round(ti, 1)))
    print("Réalisé en {} minutes ".format(round(ti, 1) // 60))
    print()

    # REMPLISSAGE DF / CREATION DE CSV : on effectue cela à chaque page que l'on récupère pour avoir un fichier .csv
    # si le programme plante avant la fin
    dictionnaire_df1 = {'Titre comment': list_titre,
                       'Date de répinse': list_date,
                       'Reponse ou non': list_reponse_comment,
                       'Liste peronnes': list_reponse_comment_qui,
                       "Nombre d'étoile": list_stars}
    df_company = pd.DataFrame(data=dictionnaire_df1)
    df_company.to_csv("Infos_Commentaire2.csv")
    go_next_page()


# CALCUL DU TEMPS DE DU PROGRAMME
driver.close()
tt = time() - t0  # heure de fin
print("Réalisé en {} secondes".format(round(tt, 1)))
print("Réalisé en {} minutes ".format(round(tt, 1)//60))