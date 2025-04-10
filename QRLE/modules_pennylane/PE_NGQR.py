import pennylane as qml
import numpy as np

n_qubits = 8
dev = qml.device("default.mixed", wires=n_qubits)

@qml.qnode(dev)
def PE_NGQR(noise_type=0, level=0):
    """Quantum circuit for PE_NGQR with optional noise injection."""
    # Apply Hadamard gates to qubits 1-6
    for i in range(1, 7):
        qml.Hadamard(wires=i)

    # Control patterns for multi-controlled X gates
    control_patterns = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 1]
    ]

    # Apply gates to both target qubits (0 and 7)
    for target in [0, 7]:
        for pattern in control_patterns:
            qml.MultiControlledX(control_wires=[1, 2, 3, 4, 5, 6],
                                wires=[target],
                                control_values=pattern)

    # Apply noise if specified
    if noise_type > 0:
        for i in range(n_qubits):
            if noise_type == 1:
                qml.PhaseShift(level, wires=i)
            elif noise_type == 2:
                qml.AmplitudeDamping(level, wires=i)
            elif noise_type == 3:
                qml.DepolarizingChannel(level, wires=i)

    return qml.state()