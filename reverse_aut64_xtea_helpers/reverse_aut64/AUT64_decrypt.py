from AUT64_encrypt import *
class Cryptographer:
    @staticmethod
    def inverse(out, inp):
        """
        Inverse les valeurs de `inp` dans `out`, de manière à ce que
        `out[inp[i]] = i` pour chaque index `i` de `out`.
        """
        for i in range(len(out)):
            assert inp[i] < len(out)
            out[inp[i]] = i

    @staticmethod
    def apply_pbox(m, pbox, n=1):
        """
        Applique la permutation `pbox` à la liste `m` `n` fois (par défaut, `n=1`).
        La permutation consiste à réorganiser les éléments de `m` selon `pbox`.
        """
        while n > 0:
            n -= 1
            n_m = [0] * len(m)
            for i in range(len(m)):
                n_m[pbox[i]] = m[i]
            m[:] = n_m

    @staticmethod
    def apply_pbox_bitwise(input_data, pbox):
        """
        Applique la permutation `pbox` aux bits de `input_data`.
        """
        result = 0
        for bit in range(8):
            if input_data & (1 << bit):
                result |= 1 << pbox[bit]
        return result

    @staticmethod
    def apply_sbox(byte, sbox):
        """
        Applique une substitution à 4 bits sur le `byte` donné en utilisant la table `sbox`.
        La substitution est effectuée sur chaque moitié de 4 bits du `byte`.
        """
        return sbox[byte & 0xf] | (sbox[(byte >> 4) & 0x0f] << 4)

    @staticmethod
    def compress_sum_low(state, key_reg, roundN):
        """
        Calcule une somme compressée (`r6`) en combinant des nibbles de l'état (`state`)
        et des nibbles du registre de clé (`key_reg`) à l'aide de tables de recherche.
        """
        r6 = 0
        for byte in range(7):
            ln = state[byte] & 0xf  # Obtient le nibble inférieur du byte
            lk = key_reg[table_ln[8 * roundN + byte]]  # Obtient le nibble de la clé
            p0 = ln | (lk << 4)  # Combine les nibbles de l'état et de la clé
            r6 ^= table_offset[p0]
        return r6

    @staticmethod
    def compress_sum_high(state, key_reg, roundN):
        """
        Calcule une somme compressée (`r5`) en combinant des nibbles de l'état (`state`)
        et des nibbles du registre de clé (`key_reg`) à l'aide de tables de recherche.
        """
        r5 = 0
        for byte in range(7):
            un = state[byte] >> 4  # Obtient le nibble supérieur du byte
            uk = key_reg[table_un[8 * roundN + byte]]  # Obtient le nibble de la clé
            p1 = un | (uk << 4)  # Combine les nibbles de l'état et de la clé (uk, un)
            r5 ^= table_offset[p1]
        return r5

    @staticmethod
    def compress_substitute(ln, lk):
        """
        Effectue une substitution et déplace le résultat dans le nibble supérieur.
        """
        ls = (table_sub[lk] << 4) & 0xf0  # Substitue et déplace le résultat dans le nibble supérieur
        for i_ln in range(16):
            if table_offset[ls + i_ln] == ln:
                return i_ln
        assert 0
        return 0

    @staticmethod
    def compress_unsubstitute(ln, lk):
        """
        Annule la substitution effectuée précédemment par `compress_substitute`.
        """
        if lk == 0:
            assert 0

        ls = (table_sub[lk] << 4) & 0xf0  # Substitue et déplace le résultat dans le nibble supérieur
        return table_offset[ls + ln]

   

    @staticmethod
    def decompress(state, key_reg, roundN):
        """
        Décompresse le résultat de la fonction de compression `compress`.
        """
        high = state[7] >> 4
        r5 = high ^ Cryptographer.compress_sum_high(state, key_reg, roundN)
        high = Cryptographer.compress_unsubstitute(r5, key_reg[table_un[8 * roundN + 7]])

        low = state[7] & 0xf
        r6 = low ^ Cryptographer.compress_sum_low(state, key_reg, roundN)
        low = Cryptographer.compress_unsubstitute(r6, key_reg[table_ln[8 * roundN + 7]])

        return ((high << 4) & 0xf0) | (low & 0x0f)

 

    @staticmethod
    def decrypt(m, key_reg, pbox, sbox, nRounds):
        """
        Fonction de déchiffrement qui effectue l'opération inverse du chiffrement.
        """
        sbox_inverse = [0] * len(sbox)
        Cryptographer.inverse(sbox_inverse, sbox)

        pbox_inverse = [0] * len(pbox)
        Cryptographer.inverse(pbox_inverse, pbox)

        for round in range(nRounds):
            step4 = m[7]
            step3 = Cryptographer.apply_sbox(step4, sbox_inverse)
            step2 = Cryptographer.apply_pbox_bitwise(step3, pbox_inverse)
            m[7] = Cryptographer.apply_sbox(step2, sbox_inverse)
            m[7] = Cryptographer.decompress(m, key_reg, nRounds - 1 - round)
            Cryptographer.apply_pbox(m, pbox_inverse)
        return m


if __name__ == "__main__":
    key_reg = [12, 6, 4, 14, 5, 4, 8, 11]
    P= [0x1,0x14,0x12,0x4,0x5,0x6,0x7,0x8]
    pbox = [2, 6, 0, 5, 7, 4, 3, 1]
    sbox=[0, 1, 2, 3, 4, 5, 7, 11, 6, 8, 10, 9, 13, 12, 15, 14]
    nRounds=8
    ciphertext=encrypt(P,key_reg,pbox,sbox,nRounds)
    cryptographer = Cryptographer()
    print("Le message clair est",P)
    print("le message chiffré est",ciphertext)
    print("Le message clair en utilisant l'algorithme de déchiffrement est",cryptographer.decrypt(ciphertext, key_reg, pbox, sbox, nRounds))
