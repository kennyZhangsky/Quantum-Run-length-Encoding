import pennylane as qml
import numpy as np

n_qubits = 8
dev = qml.device("default.mixed", wires=n_qubits)


@qml.qnode(dev)
def MQIR(noise_type=0, level=0):
    """Quantum circuit for MQIR with optional noise injection."""
    # Apply Hadamard gates to qubits 1-6
    for i in range(1, 7):
        qml.Hadamard(wires=i)

    # Multi-controlled X gates with different control patterns
    control_patterns = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 1]
    ]

    for pattern in control_patterns:
        qml.MultiControlledX(control_wires=[1, 2, 3, 4, 5, 6],
                             wires=[0],
                             control_values=pattern)

    # Rotation on qubit 7
    qml.RY(np.pi / 2, wires=7)

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