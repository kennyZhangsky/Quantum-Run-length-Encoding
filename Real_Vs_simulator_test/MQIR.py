import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import MCXGate
from plot_histogram import draw_plot_histogram

# Initialize quantum simulator and registers
num_qubits = 6
simulator = Aer.get_backend('qasm_simulator')
qreg = QuantumRegister(num_qubits)
creg = ClassicalRegister(num_qubits)
qc = QuantumCircuit(qreg, creg)

# Apply Hadamard gates to qubits 1 through 4
for i in range(1, num_qubits-1):
    qc.h(i)

# Define multi-controlled X gates with different control states
control_states = ['1100', '1101', '0010', '0011', '1010', '1011']
mcgates = [MCXGate(4, None, state) for state in control_states]

# Append all multi-controlled gates to the circuit (controls on 1-4, target on 0)
for gate in mcgates:
    qc.append(gate, [1, 2, 3, 4, 0])

# Apply rotation gate to qubit 5
qc.ry(np.pi/2, 5)

# Draw and save the circuit diagram
figure = qc.draw("mpl")
figure.savefig('../Results/MQIR_circuit.png', dpi=300)

# Measure all qubits and execute the circuit
qc.measure(qreg, creg)
job = execute(qc, simulator, shots=20000)
counts = job.result().get_counts(qc)

# Plot results
draw_plot_histogram(counts, num_qubits, None, 'simulator', 'MQIR_simulator')
draw_plot_histogram(None, num_qubits, 'MQIR.csv', 'real', 'MQIR_real')
