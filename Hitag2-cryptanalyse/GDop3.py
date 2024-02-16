from GDop2 import *

#Initialization of empty lists.
ex0,ex1,ex2,ex3,ex4,ex5,ex6,ex7,ex8=[],[],[],[],[],[],[],[],[]

#precompute all possible mask valuations for the mask of each layer.
for i0 in range(1<<20):
    ex0.append(expand(masks[0],i0))
for i1 in range(1<<15):
    ex1.append(expand(masks[1]|(1<<47), i1))
for i2 in range(1<<5):
    ex2.append(expand(masks[2]|(1<<47), i2))
for i3 in range(1<<3):
    ex3.append(expand(masks[3],i3))
for i4 in range(1<<1):
    ex4.append(expand(masks[4],i4))
for i5 in range(1<<1):
    ex5.append(expand(masks[5],i5))
for i6 in range(1<<1):
    ex6.append(expand(masks[6],i6))
for i7 in range(1<<1):
    ex7.append(expand(masks[7],i7))
for i8 in range(1<<1):
    ex8.append(expand(masks[8],i8))

#To get the results of f computations more quickly we can precompute its output for all 2^20 possible inputs.
cle,valeur=[],[]
for i9 in range(1<<20):
    valeur.append(f20(expand(masks[0],i9)))
    cle.append(expand(masks[0],i9))
dic=dict(zip(cle,valeur))

#Which bits to guess at layer0 
mask_filt=96785823617388


def find_state4(keystream):
    """
    This third optimization keeps the code as it is, except that instead of calling the f20 and
    expand functions in each loop, I decided to calculate all outputs associated with all 2^20
    possible inputs and store them in a dictionary. It won't be a simple loop from 0 to 2^20-1
    because the argument (state) we pass to the function is a 48-bit integer. So we will create a
    dictionary that has f20(expand(masks[0],i)) as the value and expand(masks[0],i) as the key
    Note that masks[0] is identical to mask_filt and determines all the input bits for the f20
    function. In each loop, we mask the pre-calculated new state with the mask_filt to avoid
    index out of range errors.

    As for the expand function, the principle is simpler. It involves storing all possible evaluations
    for each mask in 9 different arrays.

    This approach allows us to save a significant amount of time as the expand and f20 functions
    each contain over 150 operations.

    Args:
        keystream (list): List of observed keystream bits.

    Returns:
        list: List of approximately 2^16 candidate states.

    """
    
    state_candidates=[]
    # Iterate through possible values of the first layer's state variable
    for i0 in range(1<<bits[0]):
        state0 = ex0[i0]
        #Check if state0 produces the correct first keystream
        if dic[state0] != keystream[0]:
            continue

        # Iterate through possible values of the second layer's state variable
        for i1 in range(1<<(bits[1]+1)): # guess LFSR output bit 0
            state1 = (state0>>1) | ex1[i1]
            state11=state1&mask_filt
            #Check if state1 produces the correct second keystream
            if dic[state11] != keystream[1]:
                continue

            # Iterate through possible values of the third layer's state variable
            for i2 in range(1<<bits[2]+1): # guess LFSR output bit 1
                state2 = (state1>>1) | ex2[i2]
                state22=state2&mask_filt
                #Check if state2 produces the correct third keystream
                if dic[state22] != keystream[2]:
                    continue

                # Iterate through possible values of the fourth layer's state variable
                for i3 in range(1<<bits[3]):
                    state3 = lfsr(state2) | ex3[i3]
                    state33=state3&mask_filt
                    #Check if state3 produces the correct fourth keystream
                    if dic[state33] != keystream[3]:
                        continue

                    # Iterate through possible values of the fifth layer's state variable
                    for i4 in range(1<<bits[4]):
                        state4 = lfsr(state3) | ex4[i4]
                        state44=state4&mask_filt
                        #Check if state4 produces the correct fifth keystream
                        if dic[state44] != keystream[4]:
                            continue

                        # Iterate through possible values of the sixth layer's state variable
                        for i5 in range(1<<bits[5]):
                            state5 = lfsr(state4) | ex5[i5]
                            state55=state5&mask_filt
                            #Check if state5 produces the correct sixth keystream
                            if dic[state55] != keystream[5]:
                                continue

                            # Iterate through possible values of the seventh layer's state variable
                            for i6 in range(1<<bits[6]):
                                state6 = lfsr(state5) | ex6[i6]
                                state66=state6&mask_filt
                                #Check if state6 produces the correct seventh keystream
                                if dic[state66] != keystream[6]:
                                    continue

                                # Iterate through possible values of the eighth layer's state variable
                                for i7 in range(1<<bits[7]):
                                    state7 = lfsr(state6) | ex7[i7]
                                    state77=state7&mask_filt
                                    #Check if state7 produces the correct eighth keystream
                                    if dic[state77] != keystream[7]:
                                        continue

                                    # Iterate through possible values of the ninth layer's state variable
                                    for i8 in range(1<<bits[8]):
                                        state8 = lfsr(state7) | ex8[i8]
                                        state88=state8&mask_filt
                                        #Check if state8 produces the correct ninth keystream
                                        if dic[state88] != keystream[8]:
                                            continue
                                        #Test it against the remaining 23 observed keystream bits using test function
                                        if test(lfsr(state8),keystream)!=None:
                                            state_candidates.append(test(lfsr(state8),keystream)[1])
                                            print(state_candidates)
    return state_candidates


    


    
def test_val():
    """
    This is a validity testing function. It is essentially the same as the previous function, except
    that we will provide our own example by specifying the key, UID, IV1, and IV2. Then we 
    calculate the corresponding keystream1 and keystream2. After that, we perform the first 9 
    shifts of the register's state, and we check if the key returned by the algorithm is identical to
    the key we used. We use the try_recover function to reconstruct the key from an initial state 
    that produces the keystream. Additionally, we add an additional condition to each line to 
    verify (thus eliminating all incorrect states) if the guessed state after applying a mask is
    identical to the actual state we have already calculated and stored in test_states.
    
    """
    #Initialization of the key, the identifier uid, and two nonce vectors iv1 and iv2.
    key,uid,iv1,iv2=0x414141414141, 0x42424242, 0x43434343,0x43444344

    #Precompute state1 and state2, as well as ks1 and ks2.
    state = hitag2_init(key, uid, iv1)
    state2=hitag2_init(key, uid, iv2)
    keystream1_int= hitag2(state,32)
    keystream=list(map(int, "{0:032b}".format(keystream1_int)))
    keystream2_int=hitag2(state2)

    #calculate the first 9 shifts of the register
    test_states = []                 
    for _ in range(len(masks)):
        test_states.append(state)
        state = lfsr(state)
    
    # Iterate through possible values of the first layer's state variable
    for i0 in range(1<<bits[0]):
        state0 = ex0[i0]
        #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
        if (state0 & mask_filt) != (test_states[0] & mask_filt):
            continue
        
        #Check if state0 produces the correct first keystream
        if dic[state0] != keystream[0]:
            continue

        # Iterate through possible values of the second layer's state variable
        for i1 in range(1<<(bits[1]+1)): # guess LFSR output bit 0
            state1 = (state0>>1) | ex1[i1]
            state11=state1&mask_filt
            #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
            if (state11) != (test_states[1] & mask_filt):
                continue
            
            #Check if state1 produces the correct second keystream
            if dic[state11] != keystream[1]:
                continue

            # Iterate through possible values of the third layer's state variable
            for i2 in range(1<<(bits[2]+1)): # guess LFSR output bit 1
                state2 = (state1>>1) | ex2[i2]
                state22=state2&mask_filt
                #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                if(state22) != (test_states[2] & mask_filt):
                    continue
                
                #Check if state2 produces the correct third keystream
                if dic[state22] != keystream[2]:
                    continue

                # Iterate through possible values of the fourth layer's state variable
                for i3 in range(1<<bits[3]):
                    state3 = lfsr(state2) | ex3[i3]
                    state33=state3&mask_filt
                    #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                    if (state33) != (test_states[3] & mask_filt):
                        continue
                    
                    #Check if state3 produces the correct fourth keystream
                    if dic[state33] != keystream[3]:
                        continue

                    # Iterate through possible values of the fifth layer's state variable
                    for i4 in range(1<<bits[4]):
                        state4 = lfsr(state3) | ex4[i4]
                        state44=state4&mask_filt
                        #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                        if (state44) != (test_states[4] & mask_filt):
                            continue
                        
                        #Check if state4 produces the correct fifth keystream
                        if dic[state44] != keystream[4]:
                            continue

                        # Iterate through possible values of the sixth layer's state variable
                        for i5 in range(1<<bits[5]):
                            state5 = lfsr(state4) | ex5[i5]
                            state55=state5&mask_filt
                            #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                            if (state55) != (test_states[5] & mask_filt):
                                continue
                            
                            #Check if state5 produces the correct sixth keystream
                            if dic[state55] != keystream[5]:
                                continue

                            # Iterate through possible values of the seventh layer's state variable
                            for i6 in range(1<<bits[6]):
                                state6 = lfsr(state5) | ex6[i6]
                                state66=state6&mask_filt
                                #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                                if (state66) != (test_states[6] & mask_filt):
                                    continue
                                
                                #Check if state6 produces the correct seventh keystream
                                if dic[state66] != keystream[6]:
                                    continue

                                # Iterate through possible values of the eighth layer's state variable
                                for i7 in range(1<<bits[7]):
                                    state7 = lfsr(state6) | ex7[i7]
                                    state77=state7&mask_filt
                                    #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                                    if (state77) != (test_states[7] & mask_filt):
                                        continue
                                    
                                    #Check if state7 produces the correct eighth keystream
                                    if dic[state77] != keystream[7]:
                                        continue

                                    # Iterate through possible values of the ninth layer's state variable
                                    for i8 in range(1<<bits[8]):
                                        state8 = lfsr(state7) | ex8[i8]
                                        state88=state8&mask_filt
                                        
                                        #check if the common bits (after applying a filter mask) between the guessed state and the real state are not different.
                                        if(state88) != (test_states[8] & mask_filt):
                                            continue

                                        #Check if state8 produces the correct ninth keystream
                                        if dic[state88] != keystream[8]:
                                            continue
                                        #Test it against the remaining 23 observed keystream bits using test function
                                        if test(lfsr(state8),keystream)!=None:
                                            #Verify that the recovered key is the same as the one we used.
                                            return try_recover(test(lfsr(state8),keystream)[1],uid,iv1,iv2,keystream2_int)==key





#keystream=[0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]
                    
