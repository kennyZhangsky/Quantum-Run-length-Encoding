import numpy as np
import matplotlib.pyplot as plt

from QRLE import QRLE
from MQIR import MQIR
from PE_NGQR import PE_NGQR

# Font sizes
fontsize_title = 26
fontsize_xlabel = 24
fontsize_ylabel = 24
fontsize_ticks = 20
fontsize_legend = 20

# Noise levels
noise_levels = np.linspace(0, 1, 20)

# 原始无噪声状态
QRLE_origin = QRLE().flatten()
MQIR_origin = MQIR().flatten()
PENGQR_origin = PE_NGQR().flatten()


def compute_fidelity(reference, noisy):
    return np.abs(np.dot(np.conj(reference), noisy)) ** 2


def compute_fidelities(noise_type, origin_funcs):
    """Compute fidelities under a certain noise type."""
    fidelity_lists = [[] for _ in range(3)]

    for level in noise_levels:
        states = [f(noise_type, level).flatten() for f in [QRLE, MQIR, PE_NGQR]]
        for i, state in enumerate(states):
            fidelity = compute_fidelity(origin_funcs[i], state)
            fidelity_lists[i].append(fidelity)

    return fidelity_lists


def draw(f1, f2, f3, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, f1, label="QRLE", marker='o', linestyle='-', color='#264653')
    plt.plot(noise_levels, f2, label="MQIR", marker='s', linestyle='-', color='#E66F51')
    plt.plot(noise_levels, f3, label="PE-NGQR", marker='d', linestyle='-', color='#2A9D8E')
    plt.xlabel("Noise Strength", fontsize=fontsize_xlabel)
    plt.ylabel("Fidelity", fontsize=fontsize_ylabel)
    plt.title(title, fontsize=fontsize_title)
    plt.xticks(fontsize=fontsize_ticks)
    plt.yticks(fontsize=fontsize_ticks)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.legend(fontsize=fontsize_legend)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()


# 运行三种噪声模拟
origin_states = [QRLE_origin, MQIR_origin, PENGQR_origin]

# Phase Shift noise_type = 1
ps_fid1, ps_fid2, ps_fid3 = compute_fidelities(noise_type=1, origin_funcs=origin_states)
draw(ps_fid1, ps_fid2, ps_fid3, "Phase Shift Noise", "phase_shift_noise.png")

# Amplitude Damping noise_type = 2
ad_fid1, ad_fid2, ad_fid3 = compute_fidelities(noise_type=2, origin_funcs=origin_states)
draw(ad_fid1, ad_fid2, ad_fid3, "Amplitude Damping Noise", "amplitude_damping_noise.png")

# Depolarizing Channel noise_type = 3 ← 注意这里原代码错了
dp_fid1, dp_fid2, dp_fid3 = compute_fidelities(noise_type=3, origin_funcs=origin_states)
draw(dp_fid1, dp_fid2, dp_fid3, "Depolarizing Channel Noise", "depolarizing_noise.png")
