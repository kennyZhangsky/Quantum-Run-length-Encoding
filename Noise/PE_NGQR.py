import pennylane as qml
import numpy as np

n_qubits = 6
dev = qml.device("default.mixed", wires=n_qubits)

@qml.qnode(dev)
def PE_NGQR(noise_type=0, level=0):
    """Quantum circuit for PE_NGQR with optional noise injection."""
    # Apply Hadamard gates to qubits 1-5
    for i in range(1, 5):
        qml.Hadamard(wires=i)

    # Control patterns for multi-controlled X gates
    control_states = ['0011', '1011', '0100', '1100', '0101', '1101']
    control_patterns = [list(map(int, state)) for state in control_states]

    # Apply gates to both target qubits (0 and 5)
    for target in [0, 5]:
        for pattern in control_patterns:
            qml.MultiControlledX(control_wires=[1, 2, 3, 4],
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
# === 调用函数并输出量子线路图 ===
# noise_type = 0
# level = 0.1
#
# # 输出 ASCII 量子线路图
# print(qml.draw(PE_NGQR)(noise_type, level))
#
# # 获取量子态
# state = PE_NGQR(noise_type, level)
