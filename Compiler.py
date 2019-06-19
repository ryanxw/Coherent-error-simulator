from numpy import pi, sin, cos, random
from Gate_bases import *
from Error_dist import r


# -- The gate compiler --
def compile_gate(gate, errors, synth_Z=True):

  [single_err, phase_err, XX_err] = errors

  gate_type = gate[0]     # Gate type
  q = gate[1]             # Qubit(s)
  t = gate[2]             # Gate angle 
  phi = gate[3]           # Gate axis (on the x-y plane)
  
  # -- Helper functions for returning gates --

  def S_phi(q, t, phi):
    return [[q], [s_phi], t * r(single_err), [phi + (r(phase_err) - 1) * pi / 2]]

  def X(q, t):
    return S_phi(q, t, 0)
  
  def Y(q, t):
    return S_phi(q, t, pi/2)
  
  def Z(q, t):
    if synth_Z:
      return Y(q, pi/2), X(q, t), Y(q, -pi/2)
    else:
      return [[q], [z], t * r(phase_err), [0]]

  def XX(q1, q2, t):
    return [[q1, q2], [s_phi, s_phi], t * r(XX_err), [(r(phase_err) - 1) * pi / 2, (r(phase_err) - 1) * pi / 2]]
  
  # -- Switch between different gate types --

  if gate_type == s_phi:
    return S_phi(q, t, phi)

  if gate_type == x:
    return X(q, t)

  if gate_type == y:
    return Y(q, t)
  
  if gate_type == z:
    return Z(q, t)
  
  if gate_type == xx:
    return XX(q[0], q[1], t)
  
  if gate_type == h:
    return Y(q, pi/2), X(q, -pi)
  
  if gate_type == cnot:
    return Y(q[0], pi/2), XX(q[0], q[1], pi/2), X(q[0], -pi/2), X(q[1], -pi/2), Y(q[0], -pi/2)

# -- Compile and output list of noisy gates --


