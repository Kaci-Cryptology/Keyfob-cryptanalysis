# Introduction

This repository provides a comprehensive description of the Hitag-2 cryptosystem, based on the study of several scientific articles. You can find this document in the "Hitag-2 cryptanalysis" directory. It also includes implementations of each attack and possible optimizations.

# Implementations

* `BruteForce.ipynb`: This file includes both the Hitag2 algorithm and a brute-force attack targeting the secret key on a central processing unit (CPU) using Python.
* `GDop1.ipynb`: A first optimization of the brute-force attack, the recursive Guess and Determine attack version. It targets the initial state that generated the keystream and then retrieves the secret key.
* `GDop2.ipynb`: A second optimization that removes recursion from the attack, thereby improving its efficiency.
* `GDop3.ipynb`: A third optimization involves precomputing the 'expand' and 'f' functions and storing them in arrays to avoid calling them at each iteration of the loop.
* `GDop4.ipynb`: A final optimization involves precomputing and memorizing subfilters, improving performance by avoiding recalculating these values ​​each time they are used.
* `BruteForceGPU.ipynb`: A parallel version of the brute-force attack is implemented using Numba CUDA, allowing simultaneous execution on multiple graphics processors.
* `BruteForce.py GDop1.py GDop2.py and GDop3.py`: All .py files should not be executed directly; they serve as source code for the notebooks.

# Execution

To execute the different attacks:

# For the .ipynb files, all necessary instructions are provided in the notebook itself. Simply follow the instructions provided there.
# For the OpenCL version, you will find a README file that explains in detail the procedure and execution of the attack.
