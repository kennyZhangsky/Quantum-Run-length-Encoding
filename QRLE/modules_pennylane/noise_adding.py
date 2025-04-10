import numpy as np
import matplotlib.pyplot as plt
import pennylane as qml

# Font settings for plots
FONT = {
    'title': 26,
    'xlabel': 24,
    'ylabel': 24,
    'ticks': 20,
    'legend': 20
}

# Common quantum state and setup
STATE = np.array([0.354 + 0j, 0 + 0j, 0.354 + 0j, 0 + 0j, 0 + 0j, 0.354 + 0j,
                  0 + 0j, 0.354 + 0j, 0 + 0j, 0.354 + 0j, 0 + 0j, 0.354 + 0j,
                  0 + 0j, 0.354 + 0j, 0 + 0j, 0.354 + 0j])
N_QUBITS = 4
NOISE_LEVELS = np.linspace(0, 1, 20)


def initialize_quantum_state():
    """Initialize and return the quantum state."""
    dev = qml.device("default.mixed", wires=N_QUBITS)

    @qml.qnode(dev)
    def encode_state():
        qml.AmplitudeEmbedding(STATE, wires=range(N_QUBITS), normalize=True)
        return qml.state()

    return encode_state().flatten()


def create_noisy_circuit(noise_gate, target_qubit=None):
    """Create a quantum circuit with specified noise applied."""
    dev = qml.device("default.mixed", wires=N_QUBITS)

    @qml.qnode(dev)
    def circuit(level):
        qml.AmplitudeEmbedding(STATE, wires=range(N_QUBITS), normalize=True)
        if target_qubit is None:
            for i in range(N_QUBITS):
                noise_gate(level, wires=i)
        else:
            noise_gate(level, wires=target_qubit)
        return qml.state()

    return circuit


def calculate_fidelity(original_state, noisy_circuit):
    """Calculate fidelity between original and noisy states."""
    fidelity = []
    for level in NOISE_LEVELS:
        noisy_state = noisy_circuit(level).flatten()
        fidelity.append(np.abs(np.dot(np.conj(original_state), noisy_state)) ** 2)
    return fidelity


def plot_results(fidelity_data, title, filename):
    """Plot and save the fidelity results."""
    plt.figure(figsize=(10, 6))
    for label, data in fidelity_data.items():
        plt.plot(NOISE_LEVELS, data, label=label,
                 marker='o' if label == "Phase Shift" else ('x' if label == "Amplitude Damping" else 's'),
                 linestyle='-',
                 color='b' if label == "Phase Shift" else ('r' if label == "Amplitude Damping" else 'g'))

    plt.xlabel("Noise Strength", fontsize=FONT['xlabel'])
    plt.ylabel("Fidelity", fontsize=FONT['ylabel'])
    plt.title(title, fontsize=FONT['title'])
    plt.xticks(fontsize=FONT['ticks'])
    plt.yticks(fontsize=FONT['ticks'])
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    plt.legend(fontsize=FONT['legend'])
    plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
    plt.show()


def run_noise_analysis(noise_configs):
    """Run complete noise analysis for given configurations."""
    original_state = initialize_quantum_state()

    for config in noise_configs:
        fidelity_data = {}
        for noise_type in ['Phase Shift', 'Amplitude Damping', 'Depolarizing Channel']:
            noise_gate = {
                'Phase Shift': qml.PhaseShift,
                'Amplitude Damping': qml.AmplitudeDamping,
                'Depolarizing Channel': qml.DepolarizingChannel
            }[noise_type]

            circuit = create_noisy_circuit(noise_gate, config['target_qubit'])
            fidelity_data[noise_type] = calculate_fidelity(original_state, circuit)

        plot_results(fidelity_data, config['title'], config['filename'])


# Define noise analysis configurations
NOISE_CONFIGS = [
    {'target_qubit': None, 'title': 'Noise on all qubits', 'filename': 'Noise_all'},
    {'target_qubit': 0, 'title': 'Noise on value qubit', 'filename': 'Noise_0'},
    {'target_qubit': 1, 'title': 'Noise on run length qubit', 'filename': 'Noise_1'},
    {'target_qubit': 2, 'title': 'Noise on index qubit', 'filename': 'Noise_2'},
    {'target_qubit': 3, 'title': 'Noise on position qubit', 'filename': 'Noise_3'}
]

# Run the analysis
run_noise_analysis(NOISE_CONFIGS)