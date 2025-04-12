import pennylane as qml
import numpy as np

n_qubits = 6
dev = qml.device("default.mixed", wires=n_qubits)


@qml.qnode(dev)
def MQIR(noise_type=0, level=0):
    """Quantum circuit for MQIR with optional noise injection."""

    # Apply Hadamard gates to control qubits: qubit 1 to 4
    for i in range(1, 5):
        qml.Hadamard(wires=i)

    # Define control bit patterns (as strings) and convert to list of ints
    control_states = ['0011', '1011', '0100', '1100', '0101', '1101']
    control_patterns = [list(map(int, state)) for state in control_states]

    # Apply MultiControlledX gates with the specified patterns
    for pattern in control_patterns:
        qml.MultiControlledX(
            control_wires=[1, 2, 3, 4],  # 4 control qubits
            wires=0,  # target qubit
            control_values=pattern
        )

    # Apply rotation on ancilla qubit (qubit 5)
    qml.RY(np.pi / 2, wires=5)

    # Optional noise
    if noise_type > 0:
        for i in range(n_qubits):
            if noise_type == 1:
                qml.PhaseShift(level, wires=i)
            elif noise_type == 2:
                qml.AmplitudeDamping(level, wires=i)
            elif noise_type == 3:
                qml.DepolarizingChannel(level, wires=i)

    return qml.state()


# # === 调用函数并输出量子线路图 ===
# noise_type = 0
# level = 0.1
#
# # 输出 ASCII 量子线路图
# print(qml.draw(MQIR)(noise_type, level))
#
# # 获取量子态
# state = MQIR(noise_type, level)
