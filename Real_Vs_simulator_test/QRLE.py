import matplotlib.pyplot as plt
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import MCXGate
from plot_histogram import draw_plot_histogram  # Note: Fixed typo in function name (if your actual function is named this way)

# Initialize quantum simulator
simulator = Aer.get_backend('qasm_simulator')
num_qubits = 4

# Create quantum and classical registers
qreg = QuantumRegister(num_qubits)
creg = ClassicalRegister(num_qubits)
qc = QuantumCircuit(qreg, creg)

# Apply Hadamard gates to all qubits except the first one (index 0)
for i in range(1, num_qubits):
    qc.h(i)

# Define multi-controlled X gates with different control states
control_states = ['010', '011', '100', '101', '110', '111']
mcgates = [MCXGate(3, None, state) for state in control_states]

# Append all multi-controlled gates to the circuit
for gate in mcgates:
    qc.append(gate, [1, 2, 3, 0])  # Controls on qubits 1-3, target on qubit 0

# Draw and save the circuit diagram
figure = qc.draw("mpl")
figure.savefig('../Results/QRLE_circuit.png', dpi=300)
plt.show()

# Measure all qubits
qc.measure(qreg, creg)

# Execute the circuit on the simulator
job = execute(qc, simulator, shots=20000)
result = job.result()
counts = result.get_counts(qc)

# Plot results from simulator and real device (if data file exists)
draw_plot_histogram(counts, num_qubits, None, 'simulator', 'QRLE_simulator')
draw_plot_histogram(None, 4, 'QRLE.csv', 'real', 'QRLE_real')