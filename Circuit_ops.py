import time
import cmath
from numpy import pi, exp, log2, sin, cos, random, linspace, copy, zeros, roll, swapaxes
import matplotlib.pyplot as plt
from numba import jit, njit

from Gate_bases import x, y, z, s_phi, identity

def zero_state(n):
    state = zeros(2 ** n, dtype=complex)
    state[0] = 1
    return state

# -- Helper functions for gate calculations -- 

# Phase addition and multiplication functions
def Multiply_np(a, b):
    return a * b

@njit(parallel=True)
def Multiply_njit(a, b):
    return a * b

def Add_np(a, b, angle):
    return cos(angle/2) * a - 1j * sin(angle/2) * b

@njit(parallel=True)
def Add_njit(a, b, angle):
    return cos(angle/2) * a - 1j * sin(angle/2) * b


# -- Apply gate to state --
def apply(gate, state, global_phase=False, N_thresh=23):
    
    # A shorthand for the original state
    a = state
    N = int(log2(len(state)))
    
    # A shorthand for the state flipped by Pauli operators
    b = copy(a)
    b = b.reshape([2] * N)
    
    if N > N_thresh:
        Add = Add_njit
        Multiply = Multiply_njit
        
    else: 
        Add = Add_np
        Multiply = Multiply_np
        
    for k in range(len(gate[0])):

        q = gate[0][k]
        basis = gate[1][k]
        angle = gate[2]
        
        if basis == identity:
            pass
        
        if basis == x:
            b = roll(b, 1, q)
        
        if basis == y:
            b = roll(b, 1, q)
            b = swapaxes(b, 0, q)
            b[0] = Multiply(b[0], -1j)
            b[1] = Multiply(b[1], 1j)
            b = swapaxes(b, 0, q)
            
        if basis == s_phi:
            phi = gate[3][k]
            b = roll(b, 1, q)
            b = swapaxes(b, 0, q)
            phase1 = cos(phi) + 1j * sin(phi)
            phase2 = cos(phi) - 1j * sin(phi)
            b[0] = Multiply(b[0], phase2)
            b[1] = Multiply(b[1], phase1)
            b = swapaxes(b, 0, q)
            
        if basis == z:
            b = swapaxes(b, 0, q)
            b[1] = Multiply(b[1], -1)
            b = swapaxes(b, 0, q)
    
    b = b.flatten()
        
    state = Add(a, b, angle)
    
    # Remove global phase (may be awkward if first amplitude is close to zero)
    if global_phase == False:
        state = state * exp(- 1j * cmath.phase(state[0]))
    return state

# ADD COLOUR FOR PHASE?
def prob_plot(state, title):
    N = int(log2(len(state)))
    
    for i in range(2 ** N):
        plt.plot(linspace(i,i,2), linspace(0, abs(state[i])**2,2), 'b', linewidth=5)
    if (title):
        plt.title(title)
    else: 
        plt.title('Probability plot')
    plt.show()
    return

def fidelity(final, ideal):
    
    F = sum(final * ideal)
    
    return abs(F)**2

def save_fidelities(fidelities, filename, N, n_gates, err, runs):
    with open(filename, 'w') as f:
        f.write(f'Results for {N} qubits, {n_gates} gates with max error = {err * 100}% over {runs} runs \n')
        for fidelity in fidelities:
            f.write("%s\n" % fidelity)
        f.close()
        
def read_fidelities(filename):
    with open(filename) as f:
        new_fids = []
        fidelities2 = f.read().splitlines()
        for i in range(len(fidelities2)-1):
            new_fids.append(float(fidelities2[i+1]))
    return new_fids
    
#  -- Tests --

# Sample distribution with 1000 data

# err = 0.1

# solns = []
# for i in range(30000):
#     solns.append(r(err))

# num_of_bins = 100

# plt.title(f'Error distribution: sin function (gate error = { err * 100 / 2 }%)')
# plt.hist(solns, num_of_bins)

# # Alternatively:
# # plt.plot(histogram(solns, 20)[0])
# print(f'Magnitude of error less than { err / 2 } with 82% probability')
# print(f'Max error per gate = { err }')

# plt.show()