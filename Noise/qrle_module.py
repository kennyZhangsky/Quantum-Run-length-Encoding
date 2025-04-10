import pennylane as qml
import numpy as np


def qrle_circuit(data):
    """Quantum circuit for QRLE encoding of run-length encoded data."""
    # Run-length encoding
    values, counts = [], []
    current_value, count = data[0], 1

    for i in range(1, len(data)):
        if data[i] == current_value:
            count += 1
        else:
            values.append(current_value)
            counts.append(count)
            current_value = data[i]
            count = 1
    values.append(current_value)
    counts.append(count)

    # Calculate required qubits
    m = len(values)
    max_value = max(max(values), max(counts))
    gamma = int(np.ceil(np.log2(max_value + 1)))  # Bits for values/counts

    log_m = max(1, int(np.ceil(np.log2(m))))  # Bits for index
    log_gamma = max(1, int(np.ceil(np.log2(gamma)))) if gamma > 1 else 1
    total_qubits = 1 + log_gamma + 1 + log_m  # Total qubits needed

    # Quantum circuit
    dev = qml.device('default.qubit', wires=total_qubits)

    @qml.qnode(dev)
    def circuit():
        # Create superposition
        for wire in range(1, total_qubits):
            qml.Hadamard(wires=wire)

        # Binary representations
        x_bin = [format(val, f'0{gamma}b') for val in values]
        k_bin = [format(count, f'0{gamma}b') for count in counts]

        # Encode data
        for i in range(m):
            i_bin = format(i, f'0{log_m}b')
            for h in range(gamma):
                h_bin = format(h, f'0{log_gamma}b')

                # Encode value bit (x_i
                if x_bin[i][gamma-h-1] == '1':
                    control_values = list(i_bin) + ['0'] + list(h_bin)
                    control_wires = list(range(log_gamma + 2, log_gamma + 2 + log_m)) + [log_gamma + 1] + list(range(1, 1 + log_gamma))
                    qml.MultiControlledX(control_wires=control_wires, wires=0, control_values=''.join(control_values))

                # Encode count bit (k_i
                if k_bin[i][gamma-h-1] == '1':
                    control_values = list(i_bin) + ['1'] + list(h_bin)
                    control_wires = list(range(log_gamma + 2, log_gamma + 2 + log_m)) + [log_gamma + 1] + list(range(1, 1 + log_gamma))
                    qml.MultiControlledX(control_wires=control_wires, wires=0, control_values=''.join(control_values))

        return qml.state()

    return circuit


# Test data
test_data = [[1, 1, 0, 3, 3, 3],
             [0, 0, 0, 3, 3, 3]]

for data in test_data:
    circuit = qrle_circuit(data)
    state = circuit()
    print(f"Circuit diagram for data {data}:")
    print(qml.draw(circuit)(), end='\n\n')
