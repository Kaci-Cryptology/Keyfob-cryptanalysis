import struct

class XTEA:
    def __init__(self, key):
        """
        Initialise XTEA avec une clé de chiffrement.

        Args:
            key (list[int]): La clé de chiffrement, composée de 4 entiers de 32 bits.

        Raises:
            ValueError: Si la clé n'a pas exactement 4 entiers de 32 bits.
        """
        if len(key) != 4:
            raise ValueError("La clé doit avoir 4 entiers de 32 bits")
        self.key = key

    def _encrypt_round(self, v0, v1, key, num_rounds):
        """
        Effectue un tour de chiffrement XTEA.

        Args:
            v0 (int): Le premier mot de données de 32 bits.
            v1 (int): Le deuxième mot de données de 32 bits.
            key (list[int]): La clé de chiffrement.
            num_rounds (int): Le nombre de tours de chiffrement.

        Returns:
            Tuple[int, int]: Un tuple contenant les mots de données chiffrés.
        """
        delta = 0x9E3779B9
        sum_val = 0

        # Boucle de chiffrement XTEA pour le nombre de tours spécifié
        for _ in range(num_rounds):
            # Étape 1 : Ajoute le résultat du XOR et des décalages à v0
            v0 += ((v1 << 4) ^ (v1 >> 5)) + v1 ^ (sum_val + key[sum_val & 3])

            # Étape 2 : Incrémente la valeur de somme
            sum_val += delta

            # Étape 3 : Ajoute le résultat du XOR et des décalages à v1
            v1 += ((v0 << 4) ^ (v0 >> 5)) + v0 ^ (sum_val + key[(sum_val >> 11) & 3])

        # Retourne les mots de données chiffrés sous forme de tuple
        return v0, v1

    def _decrypt_round(self, v0, v1, key, num_rounds):
        """
        Effectue un tour de déchiffrement XTEA.

        Args:
            v0 (int): Le premier mot de données de 32 bits.
            v1 (int): Le deuxième mot de données de 32 bits.
            key (list[int]): La clé de chiffrement.
            num_rounds (int): Le nombre de tours de chiffrement.

        Returns:
            Tuple[int, int]: Un tuple contenant les mots de données déchiffrés.
        """
        delta = 0x9E3779B9
        sum_val = delta * num_rounds

        # Boucle de déchiffrement XTEA pour le nombre de tours spécifié
        for _ in range(num_rounds):
            # Étape 1 : Soustrait le résultat du XOR et des décalages à v1
            v1 -= ((v0 << 4) ^ (v0 >> 5)) + v0 ^ (sum_val + key[(sum_val >> 11) & 3])

            # Étape 2 : Décrémente la valeur de somme
            sum_val -= delta

            # Étape 3 : Soustrait le résultat du XOR et des décalages à v0
            v0 -= ((v1 << 4) ^ (v1 >> 5)) + v1 ^ (sum_val + key[sum_val & 3])

        # Retourne les mots de données déchiffrés sous forme de tuple
        return v0, v1

    def encrypt(self, data, num_rounds):
        """
        Chiffre les données avec XTEA.

        Args:
            data (Tuple[int, int]): Un tuple contenant deux mots de données de 32 bits.
            num_rounds (int): Le nombre de tours de chiffrement.

        Returns:
            Tuple[int, int]: Un tuple contenant les mots de données chiffrés.
        """
        if len(data) != 2:
            raise ValueError("Les données doivent être un tuple de 2 entiers de 32 bits")
        v0, v1 = data
        key = self.key

        # Appelle la méthode _encrypt_round pour effectuer le chiffrement
        v0, v1 = self._encrypt_round(v0, v1, key, num_rounds)
        
        # Retourne les mots de données chiffrés sous forme de tuple
        return v0, v1

    def decrypt(self, data, num_rounds):
        """
        Déchiffre les données chiffrées avec XTEA.

        Args:
            data (Tuple[int, int]): Un tuple contenant deux mots de données chiffrés de 32 bits.
            num_rounds (int): Le nombre de tours de déchiffrement.

        Returns:
            Tuple[int, int]: Un tuple contenant les mots de données déchiffrés.
        """
        if len(data) != 2:
            raise ValueError("Les données doivent être un tuple de 2 entiers de 32 bits")
        v0, v1 = data
        key = self.key

        # Appelle la méthode _decrypt_round pour effectuer le déchiffrement
        v0, v1 = self._decrypt_round(v0, v1, key, num_rounds)

        # Retourne les mots de données déchiffrés sous forme de tuple
        return v0, v1

# Exemple d'utilisation
if __name__ == "__main__":
    key = [0xAABBCCDD, 0xEEFF0011, 0x22334455, 0x66778899]
    xtea = XTEA(key)

    data = (0x01234567, 0x89ABCDEF)
    num_rounds = 64
    encrypted_data = xtea.encrypt(data, num_rounds)
    decrypted_data = xtea.decrypt(encrypted_data, num_rounds)

    assert decrypted_data == data
    print("Données chiffrées :", encrypted_data)
    print("Données déchiffrées :", decrypted_data)
