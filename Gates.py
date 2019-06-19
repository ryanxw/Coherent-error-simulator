from Compiler import compile_gate
from Error_dist import r
from Compiler import compile_gate

# -- Set up your gate set (so we may use "apply" without instantiating "Circuit") -- 
# -- Assumes a certain way gates are synthesized --
class Gates:
    def __init__(self, single_err=.0, phase_err=.0, XX_err=.0, synth_Z=True):
        self.single_err = single_err
        self.phase_err = phase_err
        self.XX_err = XX_err
        self.errors = [single_err, phase_err, XX_err]
        self.synth_Z = synth_Z

    def gate(self, qubits, bases, angle, axes):   
        return [qubits, bases, angle, axes]
    
    # -- Native gate library --

    def S_phi(self, q, theta, phi):
        return compile_gate(["S_phi", q, theta, phi], self.errors, self.synth_Z)

    def X(self, q, t):
        return compile_gate(["X", q, t, None], self.errors, self.synth_Z)

    def Y(self, q, t):
        return compile_gate(["Y", q, t, None], self.errors, self.synth_Z)
    
    def Z(self, q, t):
        return compile_gate(["Z", q, t, None], self.errors, self.synth_Z)
    
    def XX(self, q1, q2, t):
        return compile_gate(["XX", [q1, q2], t, None], self.errors, self.synth_Z)
    
    def H(self, q):
        return compile_gate(["H", q, None, None], self.errors, self.synth_Z)
    
    def CNOT(self, q1, q2):
        return compile_gate(["CNOT", [q1, q2], None, None], self.errors, self.synth_Z)
        
    def gate_set(self):
        return 

    # Add identity for fun
    def Id(self, q):
        return self.gate([q], ["Identity"], 0, [0])

