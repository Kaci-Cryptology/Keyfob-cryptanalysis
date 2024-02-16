from BruteForce import *
import itertools
import pickle
import zipfile
def try_recover(state, uid, iv1, iv2, ks2):
    """

    This function attempts to recover a key based on a candidate state, UID,a second keystream and two IV.
    It then tests this key against iv2 and ks2. If the key produces the correct keystream, it returns the key.
    
    """
    # Convert UID and state to binary strings and map each character to an integer
    state_int = list(map(int, f"{uid:032b}")) + list(map(int, f"{state:048b}"))[32:48][::-1] + list(map(int, f"{state:048b}"))[:32][::-1]
    
    # Extract a sublist of state_int containing bits from index 32 to 47
    key1 = state_int[32:48]
    
    # Iterate over the range [0, 32)
    for i in range(32):
        # Extract a sublist of state_int from index i to i+48 and reverse it
        a3 = state_int[i:48+i][::-1]
        
        # Calculate the XOR between state_int[i+48], iv1[i], and the integer value of a3 converted from binary
        key1.append(state_int[i+48] ^ int(f"{iv1:032b}"[i]) ^ f20(int(''.join(map(str, a3)), 2)))
    
    # Convert the list of bits in key1 to an integer
    key1 = int(''.join(str(bit) for bit in key1), 2)
    
    # Check if the keystream produced by iv2 matches ks2
    if ks2 == hitag2(hitag2_init(key1, uid, iv2)):
        return key1

masks=[96785823617388, 87980872208712, 17188389120, 17180000512, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184] # Which bits to guess at each layer
bits=[20, 14, 4, 3, 1, 1, 1, 1, 1]# bits to guess in each layer
def expand(mask, x):
    """
    Deposits bits from a counter `x` over the bits in a mask value `mask`.

    Parameters:
    - mask (int): The mask value representing which bits to deposit.
    - x (int): The counter value to deposit over the mask.

    Returns:
    - res (int): The resulting value after depositing bits over the mask.

    Algorithm:
    1. Initialize `res` to 0.
    2. Iterate over each bit position `i` from 0 to 47.
       - If the least significant bit of `mask` is 1:
         - Set the `i`-th bit of `res` to the least significant bit of `x`.
         - Right-shift `x` by 1 bit.
       - Right-shift `mask` by 1 bit.
    3. Return the resulting value `res`.
    """
    res = 0
    for i in range(0, 48):
        if mask & 1:
            res |= (x & 1) << i
            x >>= 1
        mask >>= 1
    return res

def test(state,keystream):
    """
    Tests the candidate state by comparing it to the remaining 23 bits of the secret key.
    Reverses the LFSR 32 times to return the initial state that generated the keystream.

    Args:
        state (int): Candidate state to test and the keystream.

    Returns:
        list: List containing the initial state that generated the keystream.

    """
    for bit in range(len(masks), 32):
        if f20(state) != keystream[bit]:
            return
        state = lfsr(state)
    for _ in range(32):
        state = lfsr_inv(state)
    return [True,state]




def find_state1(keystream, state, layer, filt_mask=0x5806b4a2d16c):
    """
    Recursively finds the state that generated the keystream by iterating through layers.

    Args:
        keystream (list): List of observed keystream bits.
        state (int): Current state value which starts at 0
        layer (int): Current layer value which starts at 0
        filt_mask (int): Mask value for the layer's filter input bits.

    Returns:
        None

    """
    if layer < len(masks):
        # Iterate through the counter to determine the filter input bits for the layer
        for fill in range(0, 1 << bits[layer]):
            # Expand the counter value to the layer's mask using the expand function
            new_state = state | expand(masks[layer], fill)
            #print(new_state)
            # Check if the computed f20(new_state) matches the observed keystream bit for this layer
            if f20(new_state) != keystream[layer]:
                continue
            if layer < 2 : # 2 = Last LFSR guess
                # Iterate to the next layer with an updated LFSR feedback bit (0 and 1)
                find_state1(keystream, new_state >> 1, layer + 1, filt_mask)
                find_state1(keystream, (new_state >> 1) | (1 << 47), layer + 1, filt_mask)
            else:
                # Iterate to the next layer using the LFSR feedback of the computed state
                find_state1(keystream, lfsr(new_state), layer + 1, filt_mask)
