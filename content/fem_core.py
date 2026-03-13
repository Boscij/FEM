import numpy as np


def element_stiffness_matrix(EA, xy_e):
    """Global element stiffness matrix Ke for a 2D bar element."""
    dx = xy_e[1, 0] - xy_e[0, 0]
    dy = xy_e[1, 1] - xy_e[0, 1]
    L  = np.sqrt(dx**2 + dy**2)

    c = dx / L
    s = dy / L

    k_lokal = (EA / L) * np.array([[1, -1], [-1, 1]])

    T = np.array([[c, s, 0, 0],
                  [0, 0, c, s]])

    return T.T @ k_lokal @ T


def incidence_table(elements):
    """DOF indices for each element: [2i, 2i+1, 2j, 2j+1]."""
    conn = np.array([[e[0], e[1]] for e in elements], dtype=int)
    return np.vstack((
        2 * conn[:, 0],
        2 * conn[:, 0] + 1,
        2 * conn[:, 1],
        2 * conn[:, 1] + 1,
    )).T


def preprocessing(nodal_coordinates, elements, sections, materials):
    """Assembliert SSM K und Differentialoperator D.

    D @ U liefert die axialen Dehnungen aller Elemente (vektorisiert).
    Inspiriert von: Weder, M. / ZHAW (2024).

    Returns
    -------
    K : (ndof × ndof) Struktursteifigkeitsmatrix
    D : (n_elem × ndof) Differentialoperator
    """
    dofs = incidence_table(elements)
    ndof = int(np.max(dofs) + 1)
    K    = np.zeros((ndof, ndof))
    D    = np.zeros((len(elements), ndof))

    for e, (i, j, sec_key) in enumerate(elements):
        A_e, mat_key = sections[sec_key]
        E_e  = materials[mat_key][0]
        xy_e = nodal_coordinates[[i, j], :]

        dx = xy_e[1, 0] - xy_e[0, 0]
        dy = xy_e[1, 1] - xy_e[0, 1]
        L  = np.sqrt(dx**2 + dy**2)
        c  = dx / L;  s = dy / L

        k_lokal = (E_e * A_e / L) * np.array([[1., -1.], [-1., 1.]])
        T       = np.array([[c, s, 0., 0.], [0., 0., c, s]])
        De      = (T[1, :] - T[0, :]) / L   # axialer Differentialoperator

        idx = dofs[e]
        K[np.ix_(idx, idx)] += T.T @ k_lokal @ T
        D[np.ix_([e], idx)]  = De

    return K, D


def postprocessing(U, D, elements, sections, materials):
    """Berechnet Dehnung ε, Spannung σ und Normalkraft N je Element.

    Parameters
    ----------
    U        : globaler Verschiebungsvektor [mm]
    D        : Differentialoperator aus preprocessing()
    elements, sections, materials : Modelldaten

    Returns
    -------
    eps : Dehnungen  [-]
    sig : Spannungen [MPa]
    N   : Normalkräfte [N]
    """
    E_moduli = np.array([materials[sections[el[-1]][-1]][0] for el in elements])
    areas    = np.array([sections[el[-1]][0]               for el in elements])

    eps = D @ U           # axiale Dehnungen
    sig = E_moduli * eps  # Spannungen [MPa]
    N   = sig * areas     # Normalkräfte [N]

    return eps, sig, N


def assemble_K(nodal_coordinates, elements, sections, materials):
    """Assemble global stiffness matrix K."""
    dofs = incidence_table(elements)
    ndof = int(np.max(dofs) + 1)
    K = np.zeros((ndof, ndof))

    for e, (i, j, sec_key) in enumerate(elements):
        A, mat_key = sections[sec_key]
        E  = materials[mat_key][0]
        xy_e = nodal_coordinates[[i, j], :]
        Ke   = element_stiffness_matrix(E * A, xy_e)
        idx  = dofs[e]
        K[np.ix_(idx, idx)] += Ke

    return K


def solve_system(K, constraints, loads):
    """
    Solve K u = f with prescribed displacements and nodal loads.

    Returns
    -------
    U      : displacement vector (all DOFs)
    F      : force vector (all DOFs, reactions filled in)
    fixed  : boolean mask, True where DOF is prescribed
    """
    ndof = K.shape[0]

    fixed = np.zeros(ndof, dtype=bool)
    U_prescribed = []

    for node, axis, val in constraints:
        dof = 2 * int(node) + int(axis)
        fixed[dof] = True
        U_prescribed.append(val)

    U_prescribed = np.array(U_prescribed, dtype=float)
    free = ~fixed

    F = np.zeros(ndof)
    for node, axis, val in loads:
        dof = 2 * int(node) + int(axis)
        F[dof] = val

    K_FF = K[np.ix_(free,  free)]
    K_FU = K[np.ix_(free,  fixed)]
    F_F  = F[free]

    U_free = np.linalg.solve(K_FF, F_F - K_FU @ U_prescribed)

    U = np.zeros(ndof)
    U[fixed] = U_prescribed
    U[free]  = U_free

    K_UF = K[np.ix_(fixed, free)]
    K_UU = K[np.ix_(fixed, fixed)]
    F[fixed] = K_UF @ U_free + K_UU @ U_prescribed

    return U, F, fixed
