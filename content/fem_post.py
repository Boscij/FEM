"""
fem_post.py – Post-Processing für die Matrixsteifigkeitsmethode.

Funktionen (Stabelemente):
    postprocessing       : Dehnung, Spannung und Normalkraft je Element
    plot_results         : Visualisierung der verformten Konfiguration

Funktionen (Zug-Druck-Balkenelemente):
    print_results_beam   : Verschiebungen, Lagerkraefte und Schnittgroessen ausgeben
    plot_results_beam    : Visualisierung der verformten Konfiguration
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def postprocessing(U, nodal_coordinates, elements, sections, materials):
    """Berechnet Dehnung ε, Spannung σ und Normalkraft N je Element.

    Parameters
    ----------
    U                 : Verschiebungsvektor [mm]
    nodal_coordinates : Knotenkoordinaten [mm]
    elements, sections, materials : Modelldaten

    Returns
    -------
    eps : Dehnungen  [-]
    sig : Spannungen [MPa]
    N   : Normalkräfte [N]
    """
    eps = np.zeros(len(elements))
    sig = np.zeros(len(elements))
    N   = np.zeros(len(elements))

    for e, (i, j, sec_key) in enumerate(elements):
        A_e, mat_key = sections[sec_key]
        E_e  = materials[mat_key][0]
        xy_e = nodal_coordinates[[i, j], :]

        dx = xy_e[1, 0] - xy_e[0, 0]
        dy = xy_e[1, 1] - xy_e[0, 1]
        L  = np.sqrt(dx**2 + dy**2)
        c  = dx / L;  s = dy / L

        T   = np.array([[c, s, 0., 0.], [0., 0., c, s]])
        u_l = T @ U[[2*i, 2*i+1, 2*j, 2*j+1]]

        eps[e] = (u_l[1] - u_l[0]) / L
        sig[e] = E_e * eps[e]
        N[e]   = sig[e] * A_e

    return eps, sig, N


def plot_results(nodal_coordinates, elements, constraints, loads,
                 U, sig, scale=200):
    """Verformte und unverformte Konfiguration, eingefärbt nach Spannung.

    Parameters
    ----------
    nodal_coordinates : Knotenkoordinaten [mm]
    elements          : Elementliste
    constraints       : Randbedingungen
    loads             : Lasten
    U                 : Verschiebungsvektor [mm]
    sig               : Spannungen je Element [MPa]
    scale             : Vergrösserungsfaktor für die Verformung
    """
    xy_def   = nodal_coordinates + scale * U.reshape(-1, 2)
    segs_ref = [nodal_coordinates[el[:2]] for el in elements]
    segs_def = [xy_def[el[:2]]            for el in elements]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_aspect('equal')

    # Referenzkonfiguration (grau gestrichelt)
    ax.add_collection(LineCollection(segs_ref, linewidths=1.5,
                                     linestyles='--', colors='gray'))

    # Verformte Konfiguration, eingefärbt nach Spannung
    cmap   = plt.get_cmap('RdBu_r', 10)
    lc_def = LineCollection(segs_def, array=sig, cmap=cmap, linewidths=3)
    ax.add_collection(lc_def)
    fig.colorbar(lc_def, ax=ax, label='Spannung $\\sigma$ [MPa]')

    # Knoten
    ax.plot(*nodal_coordinates.T, 'ko', ms=6, zorder=5)
    ax.plot(*xy_def.T,            'rs', ms=6, zorder=5)
    for k, (x, y) in enumerate(nodal_coordinates):
        ax.annotate(str(k + 1), xy=(x, y), xytext=(6, 6),
                    textcoords='offset points', fontsize=10)

    # Lager
    for node, axis, _ in constraints:
        marker = 6 if axis == 1 else 5   # 6 = caretdown, 5 = caretright
        ax.plot(*nodal_coordinates[int(node)], marker=marker,
                ms=18, color='green', zorder=4)

    # Lasten
    for node, axis, force in loads:
        xy = nodal_coordinates[int(node)]
        dF = np.zeros(2);  dF[int(axis)] = force
        ax.annotate('', xy=xy, xytext=xy - dF * 3e-4,
                    arrowprops=dict(arrowstyle='-|>', color='red',
                                    mutation_scale=18, lw=2))

    ax.autoscale()
    ax.set_xlabel('$X$ [mm]')
    ax.set_ylabel('$Y$ [mm]')
    ax.set_title(f'Verformung (Faktor {scale}x)  -  Referenz: grau gestrichelt')
    plt.tight_layout()
    plt.show()


def print_results_beam(U, F, N, V, M, nodal_coordinates, constraints, elements):
    """Gibt Verschiebungen, Lagerkraefte und Schnittgroessen fuer Balkenelemente aus."""
    n_nodes = len(nodal_coordinates)
    axname  = {0: 'u', 1: 'v', 2: 'phi'}

    print("Verschiebungen:")
    print(f"  {'Knoten':>6}  {'u [mm]':>12}  {'v [mm]':>12}  {'phi [rad]':>12}")
    for k in range(n_nodes):
        print(f"  {k+1:>6}  {U[3*k]:>12.4f}  {U[3*k+1]:>12.4f}  {U[3*k+2]:>12.6f}")

    print()
    print("Lagerkraefte:")
    for node, axis, _ in constraints:
        dof  = 3 * int(node) + int(axis)
        unit = 'N' if axis < 2 else 'Nmm'
        print(f"  Knoten {node+1}, {axname[axis]}: {F[dof]:>12.2f} {unit}")

    print()
    print("Schnittgroessen je Element (Knoten i / Knoten j):")
    print(f"  {'Elem':>4}  {'N_i [N]':>12}  {'N_j [N]':>12}"
          f"  {'V_i [N]':>12}  {'V_j [N]':>12}"
          f"  {'M_i [Nmm]':>14}  {'M_j [Nmm]':>14}")
    for e in range(len(elements)):
        print(f"  {e+1:>4}  {N[e,0]:>12.2f}  {N[e,1]:>12.2f}"
              f"  {V[e,0]:>12.2f}  {V[e,1]:>12.2f}"
              f"  {M[e,0]:>14.2f}  {M[e,1]:>14.2f}")


def plot_results_beam(nodal_coordinates, elements, constraints, loads,
                      U, N, scale=20):
    """Verformte und unverformte Konfiguration fuer Balkenelemente, eingefaerbt nach Normalkraft."""
    n_nodes = len(nodal_coordinates)
    u_trans = np.array([[U[3*k], U[3*k+1]] for k in range(n_nodes)])
    xy_def  = nodal_coordinates + scale * u_trans

    segs_ref = [nodal_coordinates[[i, j]] for i, j, _ in elements]
    segs_def = [xy_def[[i, j]]            for i, j, _ in elements]
    N_mid    = [0.5 * (N[e, 0] + N[e, 1]) for e in range(len(elements))]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_aspect('equal')

    ax.add_collection(LineCollection(segs_ref, linewidths=1.5,
                                     linestyles='--', colors='gray', label='Referenz'))

    cmap   = plt.get_cmap('RdBu_r', 10)
    lc_def = LineCollection(segs_def, array=np.array(N_mid), cmap=cmap, linewidths=3)
    ax.add_collection(lc_def)
    fig.colorbar(lc_def, ax=ax, label='Normalkraft N [N]')

    ax.plot(*nodal_coordinates.T, 'ko', ms=7, zorder=5)
    ax.plot(*xy_def.T,            'rs', ms=7, zorder=5, label='verformt')
    for k, (x, y) in enumerate(nodal_coordinates):
        ax.annotate(str(k + 1), xy=(x, y), xytext=(8, 8),
                    textcoords='offset points', fontsize=10)

    for node, axis, _ in constraints:
        marker = 6 if axis == 1 else (5 if axis == 0 else 7)
        ax.plot(*nodal_coordinates[int(node)], marker=marker,
                ms=20, color='green', zorder=4)

    for node, axis, force in loads:
        xy = nodal_coordinates[int(node)].copy()
        dF = np.zeros(2);  dF[int(axis)] = force
        ax.annotate('', xy=xy, xytext=xy - dF * 4e-5,
                    arrowprops=dict(arrowstyle='-|>', color='red',
                                    mutation_scale=18, lw=2))

    ax.autoscale()
    ax.set_xlabel('X [mm]')
    ax.set_ylabel('Y [mm]')
    ax.set_title(f'Verformung (Faktor {scale}x)  -  Referenz: grau gestrichelt')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
