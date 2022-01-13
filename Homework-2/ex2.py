from qiskit import *
from qiskit.visualization import *
from qiskit.circuit.library import *
from qiskit.circuit import *
import numpy as np
import cmath

#j1=1 j2=0 j3=1
theta=4*np.pi*0.101

circuit=QuantumCircuit(4,3)
circuit.h(0)
circuit.h(1)
circuit.h(2)

poarta=QuantumCircuit(1)
poarta=poarta.compose(RYGate(theta))
custom=poarta.to_gate(None,'U').control(1)
circuit.append(custom,[0,3])

poarta=QuantumCircuit(1)
poarta=poarta.compose(RYGate(theta).power(2))
custom=poarta.to_gate(None,'U^2').control(1)
circuit.append(custom,[1,3])

poarta=QuantumCircuit(1)
poarta=poarta.compose(RYGate(theta).power(4))
custom=poarta.to_gate(None,'U^4').control(1)
circuit.append(custom,[2,3])

circuit.barrier()
circuit.h(0)
circuit.h(1)
circuit.h(2)

poarta=QuantumCircuit(1)
poarta=poarta.compose(RXGate((-np.pi)/4))
custom=poarta.to_gate(None,'Rx(-pi/4)').control(1)
circuit.append(custom,[2,0])

poarta=QuantumCircuit(1)
poarta=poarta.compose(RXGate((-np.pi)/2))
custom=poarta.to_gate(None,'Rx(-pi/2)').control(1)
circuit.append(custom,[1,0])

poarta=QuantumCircuit(1)
poarta=poarta.compose(RXGate((-np.pi)/2))
custom=poarta.to_gate(None,'Rx(-pi/2)').control(1)
circuit.append(custom,[2,1])

circuit.barrier()
circuit.measure(0,0)
circuit.measure(1,1)
circuit.measure(2,2)
#circuit.measure(3,3)

print(circuit)

input=QuantumCircuit(4,3)
input.y(3)
input.z(3)
input.barrier()
input=input.compose(circuit)
print(input.draw())

simulator=Aer.get_backend('qasm_simulator')
result=execute(input,simulator,shots=10000).result()
counts=result.get_counts()
plot_histogram(counts).savefig('ex2.1.png')
print("Rezultat :")
print(counts)
print("Rezultat j1-j2-j3:",counts.get('101'))