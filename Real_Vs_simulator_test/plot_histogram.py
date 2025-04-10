import csv
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def read_counts_from_csv(filename):
    """Read quantum measurement counts from CSV file."""
    counts = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            counts[row['Measurement outcome']] = int(row['Frequency'])
    return counts


def draw_plot_histogram(counts, num_qubits, filename, device, save_name):
    """Draw and save histogram of quantum measurement results."""
    if device == 'real':
        counts = read_counts_from_csv(filename)

    # Generate all possible states and initialize counts
    all_states = [f"{i:0{num_qubits}b}" for i in range(2 ** num_qubits)]
    if 'QRLE_color' in save_name:
        results = counts
    else:
        results = {state: counts.get(state, 0) for state in all_states}

    # Configure plot based on circuit type
    figsize = (16, 9) if 'QRLE' in save_name else (16, 5)
    plot = plot_histogram(results, figsize=figsize, bar_labels=False,
                          title=f'Results from {"Superconducting Quantum Computer ibm_sherbrooke" if device == "real" else "simulator ibm_qasm"}')

    ax = plt.gca()
    ax.set_title(ax.get_title(), fontsize=20, fontweight='bold')
    ax.set_xlabel('Quantum States', fontsize=18, fontweight='bold')
    ax.set_ylabel('Counts', fontsize=18, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=16)

    # Add state labels for QRLE circuits
    if 'QRLE_simulator' in save_name:
        plt.axhline(y=1000, color='r', linestyle='--')
        for i, (state, count) in enumerate(results.items()):
            if count > 0:
                ax.text(i, count + 50, state[::-1], ha='center', va='bottom',
                        fontsize=16, fontweight='bold')

    plt.tight_layout()
    plot.savefig(f'../Results/{save_name}.png', dpi=300)
    plt.show()
