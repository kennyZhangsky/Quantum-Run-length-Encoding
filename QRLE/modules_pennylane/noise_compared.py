import numpy as np
import matplotlib.pyplot as plt


from modules_pennylane.QRLE import QRLE
from modules_pennylane.MQIR import MQIR
from modules_pennylane.PE_NGQR import PE_NGQR

# font size
fontsize_title = 26
fontsize_xlabel = 24
fontsize_ylabel = 24
fontsize_ticks = 20
fontsize_legend = 20

QRLE_origin = QRLE().flatten()
MQIR_origin = MQIR().flatten()
PENGQR_origin = PE_NGQR().flatten()

# define noise levels
noise_levels = np.linspace(0, 1, 20)

phase_shift_fidelity_state1 = []
phase_shift_fidelity_state2 = []
phase_shift_fidelity_state3 = []

amplitude_damping_fidelity_state1 = []
amplitude_damping_fidelity_state2 = []
amplitude_damping_fidelity_state3 = []

depolarizing_fidelity_state1 = []
depolarizing_fidelity_state2 = []
depolarizing_fidelity_state3 = []

# ======================
# Phase Shift
# ======================
for level in noise_levels:

    noisy_state1 = QRLE(1, level).flatten()
    fidelity1 = np.abs(np.dot(np.conj(QRLE_origin), noisy_state1)) ** 2
    phase_shift_fidelity_state1.append(fidelity1)


    noisy_state2 = MQIR(1, level).flatten()
    fidelity2 = np.abs(np.dot(np.conj(MQIR_origin), noisy_state2)) ** 2
    phase_shift_fidelity_state2.append(fidelity2)


    noisy_state3 = PE_NGQR(1, level).flatten()
    fidelity3 = np.abs(np.dot(np.conj(PENGQR_origin), noisy_state3)) ** 2
    phase_shift_fidelity_state3.append(fidelity3)

# ======================
# Amplitude Damping
# ======================
for level in noise_levels:

    noisy_state1 = QRLE(2, level).flatten()
    fidelity1 = np.abs(np.dot(np.conj(QRLE_origin), noisy_state1)) ** 2
    amplitude_damping_fidelity_state1.append(fidelity1)


    noisy_state2 = MQIR(2, level).flatten()
    fidelity2 = np.abs(np.dot(np.conj(MQIR_origin), noisy_state2)) ** 2
    amplitude_damping_fidelity_state2.append(fidelity2)


    noisy_state3 = PE_NGQR(2, level).flatten()
    fidelity3 = np.abs(np.dot(np.conj(PENGQR_origin), noisy_state3)) ** 2
    amplitude_damping_fidelity_state3.append(fidelity3)

# ======================
# Depolarizing Channel
# ======================
for level in noise_levels:

    noisy_state1 = QRLE(2, level).flatten()
    fidelity1 = np.abs(np.dot(np.conj(QRLE_origin), noisy_state1)) ** 2
    depolarizing_fidelity_state1.append(fidelity1)


    noisy_state2 = MQIR(2, level).flatten()
    fidelity2 = np.abs(np.dot(np.conj(MQIR_origin), noisy_state2)) ** 2
    depolarizing_fidelity_state2.append(fidelity2)


    noisy_state3 = PE_NGQR(2, level).flatten()
    fidelity3 = np.abs(np.dot(np.conj(PENGQR_origin), noisy_state3)) ** 2
    depolarizing_fidelity_state3.append(fidelity3)


def draw(fidelity_state1, fidelity_state2, fidelity_state3):
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, fidelity_state1, label="QRLE", marker='o', linestyle='-', color='#264653')
    plt.plot(noise_levels, fidelity_state2, label="MQIR", marker='s', linestyle='-', color='#E66F51')
    plt.plot(noise_levels, fidelity_state3, label="PE-NGQR", marker='d', linestyle='-', color='#2A9D8E')
    plt.xlabel("Noise Strength", fontsize=fontsize_xlabel)
    plt.ylabel("Fidelity", fontsize=fontsize_ylabel)
    plt.title("Phase Shift on QRLE, MQIR and PE-NGQR", fontsize=fontsize_title)
    plt.xticks(fontsize=fontsize_ticks)
    plt.yticks(fontsize=fontsize_ticks)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    plt.legend(fontsize=fontsize_legend)
    plt.savefig("phase_shift_noise.png", dpi=300, bbox_inches='tight')
    plt.show()


# ======================
# Phase Shift
# ======================
draw(phase_shift_fidelity_state1, phase_shift_fidelity_state2, phase_shift_fidelity_state3)

# ======================
# Amplitude Damping
# ======================
draw(amplitude_damping_fidelity_state1, amplitude_damping_fidelity_state2, amplitude_damping_fidelity_state3)

# ======================
# Depolarizing Channel
# ======================
draw(depolarizing_fidelity_state1, depolarizing_fidelity_state2, depolarizing_fidelity_state3)
