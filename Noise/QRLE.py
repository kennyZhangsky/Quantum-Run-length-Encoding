import pennylane as qml

n_qubits = 4
dev = qml.device("default.mixed", wires=n_qubits)

@qml.qnode(dev)
def QRLE(noise_type=0, level=0):
    """Quantum circuit for QRLE with optional noise injection."""
    # Apply Hadamard gates to qubits 1-3
    for i in range(1, 4):
        qml.Hadamard(wires=i)

    # Multi-controlled X gates with different control patterns
    control_patterns = [
        [0, 1, 0],  # 010
        [1, 1, 0],  # 110
        [0, 0, 1],  # 001
        [1, 0, 1],  # 101
        [0, 1, 1],  # 011
        [1, 1, 1]   # 111
    ]

    for pattern in control_patterns:
        qml.MultiControlledX(control_wires=[1, 2, 3],
                            wires=[0],
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