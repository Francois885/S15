"""Squelette à compléter - Modes de livraison (atelier S15).

Renommez ce fichier en mode_livraison.py avant de le compléter.

La classe abstraite ModeLivraison vous est fournie en entier : c'est
le CONTRAT. Vous n'avez pas à la modifier. Votre travail consiste à
écrire les sous-classes concrètes qui implémentent ce contrat, puis
l'intrus du duck typing et le client polymorphe.

Remplacez chaque mention « À COMPLÉTER » et chaque « raise
NotImplementedError » marqué par vos implémentations. Respectez les
conventions du cours : docstrings Google, validation inline,
properties en lecture seule, super().__init__().

Programmation Orientée Objet - EICPN 2025-2026.
"""

from abc import ABC, abstractmethod


class ModeLivraison(ABC):
    """Contrat abstrait pour tout mode de livraison d'un colis.

    NE PAS MODIFIER. Cette classe définit le contrat que toute
    sous-classe concrète doit honorer.
    """

    @abstractmethod
    def cout(self, poids_kg):
        """Calcule le coût de la livraison en euros pour un colis donné."""
        raise NotImplementedError

    @abstractmethod
    def delai_estime(self):
        """Retourne le délai estimé en jours ouvrés."""
        raise NotImplementedError

    @staticmethod
    def _valider_poids(poids_kg):
        """Valide un poids de colis (utilitaire partagé par les sous-classes).

        Raises:
            TypeError: Si poids_kg n'est pas un nombre (ou est un bool).
            ValueError: Si poids_kg n'est pas strictement positif.
        """
        if isinstance(poids_kg, bool) or not isinstance(poids_kg, (int, float)):
            raise TypeError("Le poids doit être un nombre (int ou float).")
        if poids_kg <= 0:
            raise ValueError("Le poids doit être strictement positif.")

    def recapitulatif(self, poids_kg):
        """Construit une ligne récapitulative pour ce mode de livraison.

        Méthode concrète : elle s'appuie sur cout() et delai_estime(),
        résolues dynamiquement selon le type concret. Toute sous-classe
        en hérite.
        """
        return (
            f"{type(self).__name__} : {self.cout(poids_kg):.2f} EUR, "
            f"livraison en {self.delai_estime()} jour(s) ouvré(s)"
        )

    def __repr__(self):
        """Représentation non ambiguë, polymorphe via type(self).__name__."""
        return f"{type(self).__name__}()"


class LivraisonStandard(ModeLivraison):
    """Livraison standard à domicile : tarif au poids, délai de 3 jours.

    Sous-classe sans état spécifique. Les tarifs sont des constantes
    de classe (déjà fournies). Implémentez cout() et delai_estime().

    Attributes:
        TARIF_BASE (float): Part fixe du coût, en euros.
        TARIF_PAR_KG (float): Part variable, en euros par kilogramme.
        DELAI_JOURS (int): Délai fixe, en jours ouvrés.
    """

    TARIF_BASE = 4.99
    TARIF_PAR_KG = 1.50
    DELAI_JOURS = 3

    def cout(self, poids_kg):
        """Coût = part fixe + part proportionnelle au poids.
        
        Pensez à valider le poids via self._valider_poids(poids_kg).
        """
        self._valider_poids(poids_kg)
        return self.TARIF_BASE + self.TARIF_PAR_KG * poids_kg

    def delai_estime(self):
        """Délai fixe de la livraison standard."""
        return self.DELAI_JOURS


class LivraisonExpress(ModeLivraison):
    """Livraison express : même barème que la standard plus un supplément.

    Sous-classe AVEC état configurable. Le supplément est fixé à la
    construction. Vous devez :
      - écrire __init__(self, supplement=10.0) qui appelle
        super().__init__(), valide le supplément (nombre, >= 0) et le
        stocke dans self._supplement ;
      - exposer supplement en property lecture seule ;
      - implémenter cout() (barème standard + supplément) et
        delai_estime().

    Attributes:
        supplement (float): Supplément express en euros (lecture seule).
    """
    TARIF_BASE = 4.99
    TARIF_PAR_KG = 1.50
    DELAI_JOURS = 1

    def __init__(self, supplement=10.0):
        super().__init__()
        if not isinstance(supplement, float) or isinstance(supplement, bool):
            raise TypeError("Doit etre un nombre entier.")
        if supplement < 0:
            raise ValueError("doit etre plus grand que 0.")
        
        self._supplement = supplement

    @property
    def supplement(self):
        return self._supplement
    
    def cout(self, poids_kg):
        self._valider_poids(poids_kg)
        return self.TARIF_BASE + self.TARIF_PAR_KG * poids_kg + self.supplement

    def delai_estime(self):
        """Délai fixe de la livraison standard."""
        return self.DELAI_JOURS    

    # À COMPLÉTER : __init__, property supplement, cout, delai_estime


class PointRelais(ModeLivraison):
    """Livraison en point relais : tarif forfaitaire, délai de 4 jours.

    Sous-classe AVEC état. Le nom du réseau est fixé à la construction
    (chaîne non vide). Le coût est forfaitaire mais le poids doit
    quand même être validé pour respecter le contrat de la méthode.

    Attributes:
        nom_reseau (str): Nom du réseau de points relais (lecture seule).
        TARIF_FORFAIT (float): Coût forfaitaire, en euros.
        DELAI_JOURS (int): Délai fixe, en jours ouvrés.
    """

    TARIF_FORFAIT = 3.50
    DELAI_JOURS = 4

    def __init__(self, nom_reseau):
        super().__init__()
        if not isinstance(nom_reseau, str):
            raise TypeError("Doit etre une chaine.")
        if not nom_reseau.strip():
            raise ValueError("La chaine est vide.") 
        self._non_reseau = nom_reseau

    @property
    def nom_reseau(self):
        return self._non_reseau  

    def cout(self, poids_kg):
        self._valider_poids(poids_kg)
        return self.TARIF_FORFAIT

    def delai_estime(self):
        """Délai fixe de la livraison standard."""
        return self.DELAI_JOURS  
    
    # À COMPLÉTER : __init__, property nom_reseau, cout, delai_estime


class RetraitMagasin:
    """Retrait en magasin : INTRUS du duck typing.

    Cette classe N'HÉRITE PAS de ModeLivraison (c'est voulu). Elle doit
    pourtant exposer cout(poids_kg) et delai_estime() pour être
    acceptée par le client polymorphe. Le retrait est gratuit et
    immédiat. Validez le poids comme les autres modes.
    """
    def cout(self, poids_kg):
        """Calcule le coût de la livraison en euros pour un colis donné."""
        ModeLivraison._valider_poids(poids_kg)
        return 0.0

    def delai_estime(self):
        """Délai fixe de la livraison standard."""
        return 0  
    # À COMPLÉTER : cout, delai_estime (sans hériter de ModeLivraison)


def comparer_livraisons(modes, poids_kg):
    """Compare plusieurs modes de livraison pour un colis donné.

    Client polymorphe : n'utiliser QUE le protocole cout(poids_kg) /
    delai_estime(). Aucun test isinstance. Construire une chaîne, une
    ligne par mode, de la forme :
        'LivraisonStandard : 8.74 EUR en 3 jour(s)'

    Args:
        modes (list): Objets exposant cout(poids_kg) et delai_estime().
        poids_kg (float): Poids du colis en kilogrammes.

    Returns:
        str: Un tableau textuel, une ligne par mode.
    """
   
    tab = []

    for i in modes:
        tab.append(
            f"{type(i).__name__} : "
            f"{i.cout(poids_kg):.2f} EUR en "
            f"{i.delai_estime()} jour(s)")
    return "\n".join(tab)


if __name__ == "__main__":
    #Décommentez au fur et à mesure de votre avancement.
    modes = [LivraisonStandard(), LivraisonExpress(), PointRelais("RelaisColis")]
    for mode in modes:
         print(mode.recapitulatif(2.5))
    print()
    modes = [LivraisonStandard(), LivraisonExpress(), PointRelais("RelaisColis"), RetraitMagasin()]
    print(comparer_livraisons(modes, 2.5))