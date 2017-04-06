from enum import Enum


class TypeCombinaison(Enum):
    """Énumeration des types de combinaisons possibles."""
    QUINTON = 7
    CARRE = 6
    FULL = 5
    BRELAN = 4
    SEQUENCE = 3
    DEUX_PAIRES = 2
    UNE_PAIRE = 1
    AUTRE = 0

    def __str__(self):
        if self == TypeCombinaison.QUINTON:
            return "Quinton"
        if self == TypeCombinaison.CARRE:
            return "Carre"
        if self == TypeCombinaison.FULL:
            return "Full"
        if self == TypeCombinaison.BRELAN:
            return "Brelan"
        if self == TypeCombinaison.SEQUENCE:
            return "Sequence"
        if self == TypeCombinaison.DEUX_PAIRES:
            return "Deux paires"
        if self == TypeCombinaison.UNE_PAIRE:
            return "Une paire"
        if self == TypeCombinaison.AUTRE:
            return "Autre"


class Carte(Enum):
    """Énumeration des types de cartes."""
    AS = 0
    ROI = 1
    DAME = 2
    VALET = 3
    DIX = 4
    NEUF = 5

    def __str__(self):
        if self == Carte.AS:
            return "A"
        if self == Carte.ROI:
            return "R"
        if self == Carte.DAME:
            return "D"
        if self == Carte.VALET:
            return "V"
        if self == Carte.DIX:
            return "X"
        if self == Carte.NEUF:
            return "9"
