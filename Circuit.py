from Circuit_ops import apply, zero_state
from Compiler import compile_gate

# -- The quantum circuit --
class Circuit:
    def __init__(self, name, N):
        # Circuit name
        self.name = name
        # Single-qubit over-rotation, phase-error, two-qubit-over-rotation
        self.errors = [.0, .0, .0]
        # Ideal gates used for plotting circuits
        self.ideal_gates = []
        # Noisy native gates
        self.noisy_gates = []
        # Initialize state to be zero state
        self.state = zero_state(N)
        # Number of qubits where numba is used. It seems numba doesn't work when we import it from a different module
        self.N_thresh = 99
    
    def set_state(self, state):
        self.state = state

    def set_errors(self, errors):
        self.errors = errors
        
    def compile_gates(self):
        errors = self.errors
        ideal_gates = self.ideal_gates

        noisy_gates = []

        for ideal_gate in ideal_gates:
            compiled_gate = compile_gate(ideal_gate, errors)

            # Synthesized gate
            if type(compiled_gate) == tuple:
                for noisy_gate in compiled_gate:
                    noisy_gates.append(noisy_gate)
                
            # Native gate
            else:
                noisy_gates.append(compiled_gate)
        
        self.noisy_gates = noisy_gates

    # Computes the final state given the initial state and circuit
    def compute(self):
        state = self.state
        self.compile_gates()

        for gate in self.noisy_gates:
            state = apply(gate, state, N_thresh=self.N_thresh)
        return state
    
    # Clear gates
    def clear_gates(self):
        self.ideal_gates = []
        self.noisy_gates = []
        
    # -- Ideal gates in a circuit --
    def S_phi(self, q, t, phi):
        self.ideal_gates.append(["S_phi", q, t, phi])
        return self

    def X(self, q, t):
        self.ideal_gates.append(["X", q, t, None])
        return self

    def Y(self, q, t):
        self.ideal_gates.append(["Y", q, t, None])
        return self
    
    def Z(self, q, t):
        self.ideal_gates.append(["Z", q, t, None])
        return self
    
    def XX(self, q1, q2, t):
        self.ideal_gates.append(["XX", [q1, q2], t, None])
        return self
    
    # -- Synthesized gates --
    def H(self, q):
        self.ideal_gates.append(["H", q, None, None])
        return self

    def CNOT(self, q1, q2):
        self.ideal_gates.append(["CNOT", [q1, q2], None, None])
        return self

    # -- Plot circuit for ideal gates --
    def plot_circuit(self):
        return