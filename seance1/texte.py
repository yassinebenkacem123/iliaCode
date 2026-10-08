"""ILIACode, séance 1 du module NLP. Du fichier aux tokens (fichier à compléter).

Chaque fonction est une étape de la chaîne
octets -> décoder -> réparer -> normaliser -> tokeniser -> mesurer.
"""
import re
import unicodedata
from collections import Counter

import ftfy

CHIFFRES_ARABES = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
MOTIF = r'"[^"]*"|#.*|\d+\.\d+|!=|<=|>=|\w+|[^\w\s]'  # le cœur, à compléter à gauche par les règles de protection


def lire(chemin, regle="utf-8"):
    """Bloc Lire. Ouvre le fichier en octets puis les décode en caractères."""
    # 1. ouvrir le fichier en mode binaire "rb" et lire ses octets
    # 2. décoder ces octets avec la règle reçue, puis renvoyer le texte
    with open(chemin, "rb") as f:
        octets = f.read() # machine already encode --> that's we decode
        return octets.decode(regle)

def reparer(texte):
    """Bloc Réparer. Corrige les mojibakes, laisse intact un texte sain."""
    # une ligne, ftfy.fix_text(texte, normalization=None)
    # normalization=None, car normaliser est l'étape suivante, pas celle-ci
    return ftfy.fix_text(texte, normalization=None)


def normaliser(texte, forme="NFKC"):
    """Bloc Normaliser. Une seule écriture par caractère."""
    # 1. unicodedata.normalize(forme, texte)
    # 2. supprimer les diacritiques arabes, de \u064B à \u065F, avec re.sub
    # 3. supprimer le tatweel \u0640 avec replace
    # 4. convertir les chiffres arabes avec translate et CHIFFRES_ARABES
    texte = unicodedata.normalize(forme, texte)
    texte = re.sub("[\u064B-\u065F]", "", texte) # diacritiques arabes
    texte = texte.replace("\u0640", "") # remove talweel, example: "مـهـم" --> "مهم"
    texte = texte.translate(CHIFFRES_ARABES) # convert arabic digits to latin digits, example: "٢٠٢٦" --> "2026"
    return texte


def tokeniser(texte):
    """Bloc Tokeniser. Six règles, protéger d'abord, découper ensuite."""
    # 1. re.findall(MOTIF, texte) applique les règles 1 à 5
    # 2. règle 6, pour chaque token qui est un mot et contient un tiret bas,
    #    garder le token puis ajouter ses composants, token.split("_")
    tokens = []
    for token in re.findall(MOTIF, texte):
        tokens.append(token)
        if "_" in token and re.fullmatch(r"\w+", token):
            tokens.extend(c for c in token.split("_") if c)
    return tokens



def mesurer(tokens):
    """Bloc Mesurer. Fréquence de chaque token distinct."""
    # une ligne, Counter(tokens)
    return Counter(tokens)


def chaine(chemin, regle="utf-8"):
    """La chaîne complète, du fichier aux tokens."""
    return tokeniser(normaliser(reparer(lire(chemin, regle))))
