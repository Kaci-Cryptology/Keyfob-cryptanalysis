#Hitag-2 Brute Force CPU naive version
#It takes approximately 4 years on a standard computer.
#An optimized method for computing the non-linear function f.
def i4(x, a, b, c, d):
    return (((x >> a) & 1)*8)+((x >> b) & 1)*4+((x >> c) & 1)*2+((x >> d) & 1)


def f20_4(state):
    return ((0x3c65 >> i4(state,34,43,44,46)) & 1)

def f20_3(state):
    return (( 0xee5 >> i4(state,28,29,31,33)) & 1)

def f20_2(state):
    return (( 0xee5 >> i4(state,17,21,23,26)) & 1)

def f20_1(state):
    return (( 0xee5 >> i4(state, 8,12,14,15)) & 1)

def f20_0(state):
    return ((0x3c65 >> i4(state, 2, 3, 5, 6)) & 1)

def f20_last(s0,s1,s2,s3,s4):
    return (0xdd3929b >> ((s0 * 16)
                        + (s1 *  8)
                        + (s2 *  4)
                        + (s3 *  2)
                        + (s4 *  1))) & 1

#The fc function
def f20(state):
    return f20_last(f20_0(state), f20_1(state), f20_2(state), f20_3(state), f20_4(state))

#The initialization phase of Hitag-2 
def hitag2_init(key, uid, nonce):
    state = 0
    for i in range(32, 48):
        state = (state << 1) | ((key >> i) & 1)
    for i in range(0, 32):
        state = (state << 1) | ((uid >> i) & 1)
    for i in range(0, 32):
        nonce_bit = (f20(state) ^ ((nonce >> (31-i)) & 1))
        state = (state >> 1) | (((nonce_bit ^ (key >> (31-i))) & 1) << 47)
    return state

def lfsr_feedback(state):
    return (((state >>  0) ^ (state >>  2) ^ (state >>  3)
            ^ (state >>  6) ^ (state >>  7) ^ (state >>  8)
            ^ (state >> 16) ^ (state >> 22) ^ (state >> 23)
            ^ (state >> 26) ^ (state >> 30) ^ (state >> 41)
            ^ (state >> 42) ^ (state >> 43) ^ (state >> 46)
            ^ (state >> 47)) & 1)
def lfsr(state):
    return (state >>  1) + (lfsr_feedback(state) << 47)

def lfsr_feedback_inv(state):
    return (((state >>  47) ^ (state >>  1) ^ (state >>  2)
            ^ (state >>  5) ^ (state >>  6) ^ (state >>  7)
            ^ (state >> 15) ^ (state >> 21) ^ (state >> 22)
            ^ (state >> 25) ^ (state >> 29) ^ (state >> 40)
            ^ (state >> 41) ^ (state >> 42) ^ (state >> 45)
            ^ (state >> 46)) & 1)

def lfsr_inv(state):
    return ((state <<  1) + (lfsr_feedback_inv(state))) & ((1<<48)-1)

#This returns the first 32 bits of the keystream
def hitag2(state,KEYSIZE=32):
    keystream = 0
    for _ in range(0, 32):
        keystream = (keystream << 1) | f20(state)
        state = lfsr(state)
    return keystream



def BruteForce(uid,iv1,iv2,ks1,ks2):
    """

    This function implements a naive brute force attack on the 48-bit key K.
    param : It takes a serial number (uid) and two sets of (iv,ks) pairs as arguments
    Output : The secret key K
    
    """

    #Initializing an empty list.
    list_candidates=[]

    #We iterate over all possible candidate keys, which are 2^48 in total.
    for key_cand in range(1<<48+1):
        #We calculate the state of the register using the candidate key
        state=hitag2_init(key_cand,uid,iv1)

        #We call the Hitag2 function with this state as an argument. If it produces the correct keystream, we add the candidate key to the list of candidates
        if hitag2(state,32)==ks1:
            #Since the keystream is 32 bits, there are on average 2^48 - 2^32 = 2^16 keys that can produce the same (id, iv, ks) triplet due to possible collisions.
            list_candidates.append(key_cand)
            break
            
    #The second triplet helps to resolve this ambiguity and will return only one possible key.
    for key in list_candidates:
        state2=hitag2_init(key,uid,iv2)
        if ks2==hitag2(state2,32):
            return key


def Test():
    """

    This is a validity testing function
    To validate the attack, it is not recommended to iterate over all 2^48 possibilities as it would
    take a significant amount of time (approximately 4 years). Instead, we can use a 15-bit key,
    for example, and add a "break" statement as soon as a candidate key is found (which will be
    the only one since 15 bits is less than 32 bits in this example) to exit the loop.
    
    """

    #We take random key,uid,iv1,iv2
    key,uid,iv1,iv2=2**14-137,2**32-123,2**32-173,2**32-773

    #We calculate the corresponding keystreams.
    state0,state1=hitag2_init(key,uid,iv1),hitag2_init(key,uid,iv2)
    ks1,ks2=hitag2(state0,32),hitag2(state1,32)

    #We call our function with these arguments
    test=BruteForce(uid,iv1,iv2,ks1,ks2)

    #We verify the validity of the function.
    return test==key

if __name__ == "__main__":

    print(Test())
