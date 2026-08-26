"""AS/AD model of a temporary Strait of Hormuz supply shock.

The model combines an expectations-augmented Phillips curve, an IS curve and
a Taylor rule. It is deliberately small: the purpose is to make the policy
trade-off visible, not to produce a forecast.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Calibration
PI_STAR, R_STAR = 2.0, 1.0        # Inflation target and natural real rate (%)
PHI_PI, PHI_Y   = 1.5, 0.5        # Taylor-rule coefficients
GAMMA, ALPHA    = 0.4, 1.0        # Phillips slope and IS sensitivity
BETA  = (ALPHA * PHI_PI) / (1 + ALPHA * PHI_Y)
DELTA = PHI_PI - BETA * PHI_Y
EPSILON_SHOCK, T_MAX = 3.0, 8     # Shock size (pp) and simulation periods

# Simulation
def simulate(T, pi_star, r_star, phi_pi, phi_y, gamma, alpha, eps):
    beta = (alpha * phi_pi) / (1 + alpha * phi_y)
    pi, yg, rr = np.zeros(T), np.zeros(T), np.zeros(T)
    pi[0], rr[0] = pi_star, r_star
    for t in range(1, T):
        pi[t] = (pi[t-1] + gamma * beta * pi_star + eps[t]) / (1 + gamma * beta)
        yg[t] = -beta * (pi[t] - pi_star)
        rr[t] = r_star + phi_pi * (pi[t] - pi_star) + phi_y * yg[t]
    return pi, yg, rr

epsilon = np.zeros(T_MAX)
epsilon[1] = EPSILON_SHOCK   # One-period shock at t=1
pi, y, r = simulate(T_MAX, PI_STAR, R_STAR, PHI_PI, PHI_Y, GAMMA, ALPHA, epsilon)

# Colours and labels
COL = {0: '#1B4F72', 1: '#E74C3C', 2: '#27AE60', 3: '#F39C12', 4: '#8E44AD'}
LBL = {0: 't=0  Initial equilibrium', 1: 't=1  Supply shock',
       2: 't=2  Shock fades', 3: 't=3  Convergence'}

# Monetary-policy rule | AS/AD chart
fig = plt.figure(figsize=(18, 10))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.0)
ax_l = fig.add_subplot(gs[0])       # Monetary-policy rule
ax_r = fig.add_subplot(gs[1], sharey=ax_l)  # AS/AD
plt.setp(ax_r.get_yticklabels(), visible=False)

PI_LO, PI_HI = -0.5, 7.5
Y_LO, Y_HI   = -5.5, 3.5
R_LO, R_HI   = -1.0, 6.0
y_arr = np.linspace(Y_LO, Y_HI, 300)
r_arr = np.linspace(R_LO, R_HI, 300)

# Right panel: AS / AD

# Fixed aggregate-demand curve
ax_r.plot(y_arr, PI_STAR - y_arr / BETA, color='#2C3E50', lw=3, zorder=5)
ax_r.text(Y_HI - 0.6, PI_STAR - (Y_HI - 0.6)/BETA + 0.3, 'AD',
          fontsize=16, fontweight='bold', color='#2C3E50',
          bbox=dict(boxstyle='round,pad=0.12', fc='white', alpha=0.85, ec='none'))

# Aggregate-supply curves for the relevant periods
show = [0, 1, 2, 3, 4]

for t_i in show:
    if t_i == 0:
        intercept = PI_STAR
    else:
        intercept = pi[t_i - 1] + epsilon[t_i]

    oa = intercept + GAMMA * y_arr
    lw = 2.8 if t_i <= 2 else 1.4
    ls = '-' if t_i <= 2 else (0, (5, 3))
    al = 0.95 if t_i <= 2 else 0.55

    ax_r.plot(y_arr, oa, color=COL[t_i], lw=lw, ls=ls, alpha=al, zorder=4)

    lx = Y_HI - 0.3
    ly = intercept + GAMMA * lx
    if PI_LO < ly < PI_HI:
        ax_r.text(lx + 0.1, ly, f'AS$_{{{t_i}}}$', fontsize=11,
                  color=COL[t_i], fontweight='bold', va='center')

# Equilibrium points and annotations
offsets_r = {0: (22, -28), 1: (22, 22), 2: (22, -28)}
for t_i in show:
    ms = 130 if t_i <= 2 else 55
    ax_r.scatter(y[t_i], pi[t_i], c=COL[t_i], s=ms, zorder=12,
                 edgecolors='k', linewidth=1.2)

    if t_i in offsets_r:
        ox, oy = offsets_r[t_i]
        ax_r.annotate(
            f't={t_i}\n($y$={y[t_i]:.1f}%, $\\pi$={pi[t_i]:.1f}%)',
            xy=(y[t_i], pi[t_i]), xytext=(ox, oy),
            textcoords='offset points', fontsize=9, color=COL[t_i],
            fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COL[t_i], lw=1.5,
                            connectionstyle='arc3,rad=0.15'),
            bbox=dict(boxstyle='round,pad=0.3', fc='white',
                      ec=COL[t_i], alpha=0.9, lw=1.2))

# Reference guides
for t_i in [0, 1, 2]:
    ax_r.plot([0, y[t_i]], [pi[t_i], pi[t_i]],
              color=COL[t_i], ls=':', alpha=0.4, lw=1)
    ax_r.plot([y[t_i], y[t_i]], [PI_LO, pi[t_i]],
              color=COL[t_i], ls=':', alpha=0.3, lw=0.8)

# Transition arrows
for a, b in [(0, 1), (1, 2)]:
    ax_r.annotate('', xy=(y[b], pi[b]), xytext=(y[a], pi[a]),
                  arrowprops=dict(arrowstyle='->', color='gray',
                                  lw=2, connectionstyle='arc3,rad=0.25', alpha=0.5))

ax_r.set_xlabel('Output Gap  ($y_t$, %)', fontsize=14, labelpad=10)
ax_r.set_title('Aggregate Supply (AS) / Aggregate Demand (AD)',
               fontsize=14, fontweight='bold', pad=15)
ax_r.set_xlim(Y_LO, Y_HI); ax_r.set_ylim(PI_LO, PI_HI)
ax_r.axhline(PI_STAR, color='gray', ls='--', alpha=0.25, lw=0.8)
ax_r.axvline(0, color='#2C3E50', ls='-', alpha=0.7, lw=1.2)
ax_r.grid(True, alpha=0.15, lw=0.5)
ax_r.text(0.15, PI_STAR + 0.2, f'$\\pi^*={PI_STAR}\\%$',
          fontsize=10, color='gray', alpha=0.7)


# Left panel: monetary-policy rule

rpm_pi = PI_STAR + (r_arr - R_STAR) / DELTA
ax_l.plot(r_arr, rpm_pi, color='#2C3E50', lw=3, zorder=5)
lbl_r = R_HI - 0.6
ax_l.text(lbl_r + 0.1, PI_STAR + (lbl_r - R_STAR)/DELTA + 0.3, 'MPR',
          fontsize=16, fontweight='bold', color='#2C3E50',
          bbox=dict(boxstyle='round,pad=0.12', fc='white', alpha=0.85, ec='none'))
ax_l.invert_xaxis()

offsets_l = {0: (-28, -28), 1: (-65, 22), 2: (-28, -28)}
for t_i in show:
    ms = 130 if t_i <= 2 else 55
    ax_l.scatter(r[t_i], pi[t_i], c=COL[t_i], s=ms, zorder=12,
                 edgecolors='k', linewidth=1.2)

    if t_i in offsets_l:
        ox, oy = offsets_l[t_i]
        ax_l.annotate(
            f't={t_i}\n($r$={r[t_i]:.1f}%)',
            xy=(r[t_i], pi[t_i]), xytext=(ox, oy),
            textcoords='offset points', fontsize=9, color=COL[t_i],
            fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COL[t_i], lw=1.5,
                            connectionstyle='arc3,rad=0.15'),
            bbox=dict(boxstyle='round,pad=0.3', fc='white',
                      ec=COL[t_i], alpha=0.9, lw=1.2))

for t_i in [0, 1, 2]:
    ax_l.plot([r[t_i], R_LO], [pi[t_i], pi[t_i]],
              color=COL[t_i], ls=':', alpha=0.4, lw=1)
    ax_l.plot([r[t_i], r[t_i]], [PI_LO, pi[t_i]],
              color=COL[t_i], ls=':', alpha=0.3, lw=0.8)

for a, b in [(0, 1), (1, 2)]:
    ax_l.annotate('', xy=(r[b], pi[b]), xytext=(r[a], pi[a]),
                  arrowprops=dict(arrowstyle='->', color='gray',
                                  lw=2, connectionstyle='arc3,rad=-0.25', alpha=0.5))

ax_l.set_xlabel('Real interest rate  ($r_t$, %)', fontsize=14, labelpad=10)
ax_l.set_ylabel('Inflation  ($\\pi_t$, %)', fontsize=14, labelpad=10)
ax_l.set_title('Monetary Policy Rule (MPR)\nTaylor rule',
               fontsize=14, fontweight='bold', pad=15)
ax_l.set_xlim(R_HI, R_LO)
ax_l.set_ylim(PI_LO, PI_HI)
ax_l.axhline(PI_STAR, color='gray', ls='--', alpha=0.25, lw=0.8)
ax_l.axvline(R_STAR, color='gray', ls=':', alpha=0.25, lw=0.8)
ax_l.grid(True, alpha=0.15, lw=0.5)
ax_l.text(R_STAR + 0.15, PI_LO + 0.3, f'$r^*={R_STAR}\\%$',
          fontsize=10, color='gray', alpha=0.7)

# Legend
leg = []
for t_i in [0, 1, 2, 3]:
    ms = 9 if t_i <= 2 else 6
    ls = '-' if t_i <= 2 else '--'
    lw = 2.5 if t_i <= 2 else 1.5
    leg.append(Line2D([0], [0], color=COL[t_i], marker='o', ls=ls,
                      markersize=ms, lw=lw, label=LBL.get(t_i, f't={t_i}')))
leg.append(Line2D([0], [0], color='#2C3E50', lw=3, label='AD / MPR'))

fig.legend(handles=leg, loc='lower center', ncol=5, fontsize=10,
           bbox_to_anchor=(0.5, -0.03), frameon=True, fancybox=True,
           edgecolor='#BDC3C7', facecolor='#FAFAFA')

fig.suptitle(
    'Negative Supply Shock: Closure of the Strait of Hormuz\n'
    'AS/AD model with a Taylor rule — shock at t=1, fading from t=2',
    fontsize=16, fontweight='bold', y=1.0)

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig(os.path.join(OUTPUT_DIR, 'hormuz_oa_da_taylor.png'),
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close(fig)
