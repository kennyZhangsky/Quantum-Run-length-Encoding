import matplotlib.pyplot as plt
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.circuit.library.standard_gates import MCXGate
from plot_histogram import draw_plot_histogram

# Initialize quantum simulator and registers
num_qubits = 8
simulator = Aer.get_backend('qasm_simulator')
qreg = QuantumRegister(num_qubits)
creg = ClassicalRegister(num_qubits)
qc = QuantumCircuit(qreg, creg)

# Apply Hadamard gates to qubits 1 through 7
for i in range(1, num_qubits):
    qc.h(i)

# Define multi-controlled X gates with different control states
control_states = [
    '0001000', '0100010', '0011010',
    '0111001', '1001100', '1100110',
    '1011110', '1111001'
]
mcgates = [MCXGate(7, None, state) for state in control_states]

# Append all multi-controlled gates (controls on 1-7, target on 0)
for gate in mcgates:
    qc.append(gate, [1, 2, 3, 4, 5, 6, 7, 0])

# Apply X gate to qubit 7
qc.x(7)

# Draw and save the circuit diagram
figure = qc.draw("mpl")
figure.savefig('../Results/QRLE_color_circuit.png', dpi=300)
plt.show()

# Measure all qubits and execute the circuit
qc.measure(qreg, creg)
job = execute(qc, simulator, shots=20000)
counts = job.result().get_counts(qc)

# Filter results where qubit 7 is '1'
selected_results = {k: v for k, v in counts.items() if k[7] == '1'}

# Plot filtered results
draw_plot_histogram(selected_results, num_qubits, None, 'simulator', 'QRLE_color_simulator')