import math

def calculate_entropy(bits):
    # Calcul de l'entropie de Shannon pour une séquence de bits
    n = len(bits)
    if n == 0:
        return 0.0

    # Calcul de la fréquence des bits 0 et 1
    count0 = bits.count("0")
    count1 = n - count0

    # Calcul des probabilités
    p0 = count0 / n
    p1 = count1 / n

    # Calcul de l'entropie
    entropy = 0.0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)

    return entropy

def find_encrypted_bits(sequence, encrypted_bit_count):
    max_entropy = 0.0
    encrypted_bits = ""

    for i in range(len(sequence) - encrypted_bit_count + 1):
        subsequence = sequence[i:i + encrypted_bit_count]
        entropy = calculate_entropy(subsequence)
        if entropy > max_entropy:
            max_entropy = entropy
            encrypted_bits = subsequence

    return encrypted_bits

