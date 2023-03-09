# ---------------- PROJET FIL ROUGE : PARTIE 2 : récupération des commentaires -------------------------
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


def get_informations_comments(list_comment, n, l1, l2, l3, l4, l5, l6, l7):
    """
    On va récupérer les informations du commentaire : titre / date / réponse au commentaire (boolean) / qui a répondu
    au commentaire / nombre d'étoile / commentaire / reponse au commentaire
    """
    # TITRE
    try:
        title_comment_personne = list_comment[n].find_element(by='class name', value="typography_heading-s__f7029").text
    except:
        title_comment_personne = None

    # COMMENTAIRE
    try:
        comment_personne = list_comment[n].find_elements(by='class name', value="typography_body-l__KUYFJ")[0].text
    except:
        comment_personne = None

    # DATE
    try:  # obtention d'une liste de 3 ou 4 éléments avec la date en 2 ou 3
        list_date = list_comment[n].find_element(by='class name', value="styles_reviewContentwrapper__zH_9M") \
                                    .find_elements(by='class name', value="typography_body-m__xgxZ_")
    except:
        date_experience = None
    else:
        test = list_date[1].text.find("Date de l'expérience:")
        if test == 0:  # c'est que la données de la date est en 2éme position
            date_experience = list_date[1].text.split(":")[-1].strip(" ")
        else:  # c'est que la données de la date est en 3éme position
            date_experience = list_date[2].text.split(":")[-1].strip(" ")

    # REPONSE COMMENTAIRE
    try:
        reponse_comment = list_comment[n].find_element(by='class name', value="styles_content__Hl2Mi"). \
            find_elements(by='class name', value="typography_body-m__xgxZ_")[2].text
    except:
        reponse_comment = None

    # REPONSE COMMENTAIRE OU NON
    rep_bool = True
    try:  # si on y arrive c'est qu'il y a une réponse au commentaire
        reponse_comment_bool = list_comment[n].find_element(by='class name', value="styles_replyInfo__FYSje").text.split(" ")[2].split("\n")[0]
    except:
        print("--> Pas de réponse à ce commentaire")
        rep_bool = False
        reponse_comment_bool = None
    else:
        print("--> Il y'a une réponse à ce commentaire")

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

    print("--> Titre du commentaire : " + str(title_comment_personne))
    print("--> Date du commentaire : " + str(date_experience))
    print("--> Nombre d'étoile : " + str(star_number))
    print("--> La réponse a été fournie par : " + str(reponse_comment_bool))
    print("--> Commentaire : " + str(comment_personne))
    print("--> Réponse au commentaire : " + str(reponse_comment))
    print()
    print()
    # CONDITION SUR LE NOMBRE D ETOILE POUR AJOUTER LES INFORMATIONS
    if star_number <= 2:
        l1.append(title_comment_personne)
        l2.append(date_experience)
        l3.append(rep_bool)
        l4.append(reponse_comment_bool)
        l5.append(star_number)
        l6.append(comment_personne)
        l7.append(reponse_comment)


def go_next_page():
    sleep(random.uniform(T_MIN, T_MAX))
    webelement = driver.find_element(by='name', value='pagination-button-next')
    driver.execute_script('arguments[0].click()', webelement)
    sleep(random.uniform(T_MIN, T_MAX))


def actions_fill_list(li_titre, li_date, li_rep_bool, li_rep_who, li_stars, li_comment, list_rep_comment):
    try:
        list_informations = driver.find_elements(by='class name', value="styles_cardWrapper__LcCPA")
    except:
        print("on a pas réussi à récupérer la liste des commentaire")
    else:
        for i in range(len(list_informations)):
            get_informations_comments(list_informations, i, li_titre, li_date,
                                      li_rep_bool, li_rep_who, li_stars,
                                      li_comment, list_rep_comment)


t0 = time()  # début du chronomètre
# CLIQUE SUR L'ENTREPRISE VOULUE
open_trust_pilot_and_close_cookie()
sleep(random.uniform(T_MIN, T_MAX))
get_clic_category("Showroomprive.com")


# 1er CSV : RECUPERATION DES INFORMATIONS GENERALES DE LA COMPANY
sleep(random.uniform(T_MIN, T_MAX))
name_company, pou_5, pou_4, pou_3, pou_2, pou_1, avis_number, avis_notation = get_informations_general_company()

# REMPLISSAGE DF / CREATION DE CSV / pour les informations générales de la company observée
dictionnaire_df = {'Name_company': [name_company],
                   'Pourcentage de 5 étoiles': [pou_5],
                   'Pourcentage de 4 étoiles': [pou_4],
                   'Pourcentage de 3 étoiles': [pou_3],
                   'Pourcentage de 2 étoiles': [pou_2],
                   'Pourcentage de 1 étoiles': [pou_1],
                   'Nombre avis': [avis_number],
                   "Notation": [avis_notation]}
df_company = pd.DataFrame(data=dictionnaire_df)
df_company.to_csv("PART2_Infos_generales_Showroomprivee.csv")  # ON GARDERA T_MIN = 2 / T_MAX = 3


# 2eme CSV et 3eme CSV : RECUPERATION DES INFORMATIONS SUR LES COMMENTAIRES
list_titre = []
list_date = []
list_reponse_boolean = []
list_reponse_who = []
list_stars = []
list_comment = []
list_reponse_comment = []
nombre_page = 10
for i in range(nombre_page):
    actions_fill_list(list_titre, list_date, list_reponse_boolean, list_reponse_who, list_stars, list_comment, list_reponse_comment)
    print("Nombre de commentaire récupérés : " + str(len(list_titre)))
    print("Page : " + str(i+1) + " / " + str(nombre_page))
    ti = time() - t0  # heure intermédiaire
    print("Réalisé en {} secondes".format(round(ti, 1)))
    print("Réalisé en {} minutes ".format(round(ti, 1) // 60))
    print()

    # REMPLISSAGE DF / CREATION DE CSV / pour les informations générales des commentaires négatifs
    # on effectue cela à chaque page que l'on récupère pour avoir un fichier .csv
    # si le programme plante avant la fin/ pour les informations générales de la company observée
    dictionnaire_infos_generales_comment = {'Titre comment': list_titre,
                                            'Date de réponse': list_date,
                                            'Reponse ou non': list_reponse_boolean,
                                            'Liste peronnes': list_reponse_who,
                                            "Nombre d'étoile": list_stars}
    dictionnaire_comment_response = {'Commentaire': list_comment,
                                     "Réponse commenaitre": list_reponse_comment}

    df_infos_generales_comment = pd.DataFrame(data=dictionnaire_infos_generales_comment)
    df_comment_response = pd.DataFrame(data=dictionnaire_comment_response)

    df_infos_generales_comment.to_csv("PART2_Infos_generales_Commentaire.csv")
    df_comment_response.to_csv("PART2_Commentaire_Reponses.csv")

    go_next_page()


# CALCUL DU TEMPS DE REPONSE GLOBAL DU PROGRAMME
driver.close()
tt = time() - t0  # heure de fin
print("Réalisé en {} secondes".format(round(tt, 1)))
print("Réalisé en {} minutes ".format(round(tt, 1)//60))
