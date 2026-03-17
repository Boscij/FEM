"""
fem_pre.py – Pre-Processing GUI fuer ebene Fachwerke.

Hinweis: Dieser Code ist nicht Teil der Vorlesung.
         Er dient als Hilfswerkzeug zur grafischen Modelleingabe.

Funktionen:
    show_gui : Startet die interaktive Fachwerk-Eingabe-GUI
               (benoetigt %matplotlib widget im Notebook)
"""

import io
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import ipywidgets as w
from IPython.display import display, clear_output


def show_gui():
    """
    Startet die interaktive Fachwerk-Eingabe-GUI.
    Muss in einem Jupyter-Notebook mit %matplotlib widget ausgefuehrt werden.
    """

    plt.close('all')
    clear_output()
    plt.ioff()   # Verhindert Auto-Display der Figure in Colab

    # -- Modell-Zustand -------------------------------------------------------
    model = {
        'nodes':       [],
        'elements':    [],
        'constraints': [],
        'loads':       [],
        'sel':         None,
    }

    SNAP = 100
    NTOL = 80
    ETOL = 50
    XLIM = (-200, 2600)
    YLIM = (-700, 1600)

    # -- Hilfsfunktionen ------------------------------------------------------

    def snap(x, y):
        return round(x / SNAP) * SNAP, round(y / SNAP) * SNAP

    def nearest_node(x, y):
        for i, (nx, ny) in enumerate(model['nodes']):
            if np.hypot(nx - x, ny - y) < NTOL:
                return i
        return None

    def nearest_element(x, y):
        for e, (i, j, _) in enumerate(model['elements']):
            x1, y1 = model['nodes'][i]; x2, y2 = model['nodes'][j]
            dx, dy = x2 - x1, y2 - y1
            L2 = dx*dx + dy*dy
            if L2 < 1e-9:
                continue
            t = max(0.0, min(1.0, ((x - x1)*dx + (y - y1)*dy) / L2))
            if np.hypot(x1 + t*dx - x, y1 + t*dy - y) < ETOL:
                return e
        return None

    def delete_node(n):
        model['elements']    = [[i - (i > n), j - (j > n), sk]
                                 for i, j, sk in model['elements']
                                 if i != n and j != n]
        model['constraints'] = [[nd - (nd > n), a, v]
                                 for nd, a, v in model['constraints'] if nd != n]
        model['loads']       = [[nd - (nd > n), a, f]
                                 for nd, a, f in model['loads']       if nd != n]
        model['nodes'].pop(n)
        if   model['sel'] == n:                             model['sel'] = None
        elif model['sel'] is not None and model['sel'] > n: model['sel'] -= 1

    # -- Figure & Zeichnen ----------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 5.5))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.08)

    def redraw():
        ax.cla()
        ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
        ax.set_aspect('equal'); ax.set_facecolor('#f8f9fa')
        ax.set_xlabel('X [mm]'); ax.set_ylabel('Y [mm]')
        for gx in range(int(XLIM[0] // SNAP) * SNAP, XLIM[1] + SNAP, SNAP):
            ax.axvline(gx, color='#e0e0e0', lw=0.5, zorder=0)
        for gy in range(int(YLIM[0] // SNAP) * SNAP, YLIM[1] + SNAP, SNAP):
            ax.axhline(gy, color='#e0e0e0', lw=0.5, zorder=0)
        for e, (i, j, sk) in enumerate(model['elements']):
            x1, y1 = model['nodes'][i]; x2, y2 = model['nodes'][j]
            ax.plot([x1, x2], [y1, y2], '-', color='#1a1a2e', lw=2.5,
                    solid_capstyle='round', zorder=2)
            ax.text((x1+x2)/2 + 15, (y1+y2)/2 + 15, sk, fontsize=7, color='#888', zorder=3)
        for nd, a, v in model['constraints']:
            x, y = model['nodes'][nd]
            if a == 1:
                pts = np.array([[x - 65, y - 25], [x + 65, y - 25], [x, y]])
            else:
                pts = np.array([[x - 25, y - 65], [x - 25, y + 65], [x, y]])
            ax.add_patch(mpatches.Polygon(pts, closed=True,
                                          color='#27ae60', alpha=0.85, zorder=3))
        for nd, a, f in model['loads']:
            x, y = model['nodes'][nd]
            sgn = 1 if f >= 0 else -1
            dx  = sgn * 180 * (1 - a); dy = sgn * 180 * a
            ax.annotate('', xy=(x, y), xytext=(x - dx, y - dy),
                        arrowprops=dict(arrowstyle='-|>', color='#c0392b',
                                       lw=2, mutation_scale=16), zorder=4)
            ax.text(x - 1.7*dx, y - 1.7*dy, f'{f:.0f} N',
                    ha='center', va='center', fontsize=8, color='#c0392b',
                    bbox=dict(fc='white', ec='none', alpha=0.8), zorder=4)
        for k, (x, y) in enumerate(model['nodes']):
            fc = '#f39c12' if k == model['sel'] else '#2980b9'
            ax.plot(x, y, 'o', color=fc, ms=13, mec='white', mew=2, zorder=5)
            ax.text(x, y + 70, str(k + 1), ha='center', fontsize=9,
                    fontweight='bold', color='#2c3e50', zorder=6)
        info = f'Modus: {mode_sel.value}  |  Rechtsklick = loeschen'
        if model['sel'] is not None:
            info += f'  |  Knoten {model["sel"] + 1} ausgewaehlt'
        ax.set_title(info, fontsize=9)
        fig.canvas.draw_idle()

    # -- Mouse-Events ---------------------------------------------------------

    def on_click(event):
        if event.inaxes != ax or event.xdata is None:
            return
        x, y = event.xdata, event.ydata
        mode = mode_sel.value
        if event.button == 3:
            n = nearest_node(x, y)
            if n is not None:
                delete_node(n)
            else:
                e = nearest_element(x, y)
                if e is not None:
                    model['elements'].pop(e)
            redraw(); return
        if event.button != 1:
            return
        if mode == 'Knoten':
            sx, sy = snap(x, y)
            if nearest_node(sx, sy) is None:
                model['nodes'].append([float(sx), float(sy)])
        elif mode == 'Stab':
            n = nearest_node(x, y)
            if n is None: return
            if model['sel'] is None:
                model['sel'] = n
            elif model['sel'] == n:
                model['sel'] = None
            else:
                sk = sec_key_in.value.strip() or f's{len(model["elements"]) + 1}'
                model['elements'].append([model['sel'], n, sk])
                model['sel'] = None
        elif mode == 'Lager':
            n = nearest_node(x, y)
            if n is None: return
            model['sel'] = n
            con_ux.value = any(nd == n and a == 0 for nd, a, _ in model['constraints'])
            con_uy.value = any(nd == n and a == 1 for nd, a, _ in model['constraints'])
        elif mode == 'Last':
            n = nearest_node(x, y)
            if n is None: return
            model['sel'] = n
            load_fx.value = next((f for nd, a, f in model['loads'] if nd == n and a == 0), 0.0)
            load_fy.value = next((f for nd, a, f in model['loads'] if nd == n and a == 1), 0.0)
        redraw()

    def on_motion(event):
        if event.inaxes == ax and event.xdata is not None:
            sx, sy = snap(event.xdata, event.ydata)
            coord_lbl.value = f'X: {int(sx):6d} mm   Y: {int(sy):6d} mm'
        else:
            coord_lbl.value = ''

    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)

    # -- Widgets --------------------------------------------------------------

    coord_lbl = w.Label(value='', layout=w.Layout(width='230px'))

    mode_sel = w.ToggleButtons(
        options=['Knoten', 'Stab', 'Lager', 'Last'],
        value='Knoten',
        style={'button_width': '52px'},
        layout=w.Layout(width='230px'),
    )

    sec_key_in = w.Text(
        value='s1', description='Stab-Key:',
        style={'description_width': '65px'},
        layout=w.Layout(width='210px'),
    )

    con_ux  = w.Checkbox(description='U_x = 0   (x gesperrt)', indent=False)
    con_uy  = w.Checkbox(description='U_y = 0   (y gesperrt)', indent=False)
    con_btn = w.Button(description='Uebernehmen', button_style='warning',
                       layout=w.Layout(width='125px', margin='4px 0'))

    def _apply_con(_):
        n = model['sel']
        if n is None: return
        model['constraints'] = [[nd, a, v] for nd, a, v in model['constraints'] if nd != n]
        if con_ux.value: model['constraints'].append([n, 0, 0.0])
        if con_uy.value: model['constraints'].append([n, 1, 0.0])
        model['sel'] = None; redraw()

    con_btn.on_click(_apply_con)
    lager_panel = w.VBox([
        w.HTML('<small>Knoten anklicken, dann:</small>'),
        con_ux, con_uy, con_btn,
    ])

    load_fx  = w.FloatText(value=0.0, description='F_x [N]:', layout=w.Layout(width='200px'),
                            style={'description_width': '65px'})
    load_fy  = w.FloatText(value=0.0, description='F_y [N]:', layout=w.Layout(width='200px'),
                            style={'description_width': '65px'})
    load_btn = w.Button(description='Uebernehmen', button_style='warning',
                         layout=w.Layout(width='125px', margin='4px 0'))

    def _apply_load(_):
        n = model['sel']
        if n is None: return
        model['loads'] = [[nd, a, f] for nd, a, f in model['loads'] if nd != n]
        if load_fx.value != 0.0: model['loads'].append([n, 0, load_fx.value])
        if load_fy.value != 0.0: model['loads'].append([n, 1, load_fy.value])
        model['sel'] = None; redraw()

    load_btn.on_click(_apply_load)
    last_panel = w.VBox([
        w.HTML('<small>Knoten anklicken, dann:</small>'),
        load_fx, load_fy, load_btn,
    ])

    lager_box = w.VBox([
        w.HTML('<b>Lager</b>'),
        lager_panel,
    ])
    last_box = w.VBox([
        w.HTML('<b>Last</b>'),
        last_panel,
    ])

    sec_text = w.Textarea(
        value='s1: A=15.00, E=210000\ns2: A=28.28, E=210000\ns3: A=10.00, E=210000\ns4: A=56.56, E=210000\ns5: A=10.00, E=210000',
        layout=w.Layout(width='230px', height='105px'),
    )

    undo_btn  = w.Button(description='Undo',   button_style='info',
                          layout=w.Layout(width='88px'))
    clear_btn = w.Button(description='Leeren', button_style='danger',
                          layout=w.Layout(width='88px'))
    gen_btn   = w.Button(description='Code generieren', button_style='primary',
                          layout=w.Layout(width='200px', margin='6px 0'))

    code_out = w.Textarea(
        value='',
        placeholder='Hier erscheint der generierte Code...',
        layout=w.Layout(width='780px', height='360px'),
        disabled=True,
    )

    def _undo(_):
        if model['elements']:   model['elements'].pop()
        elif model['nodes']:    delete_node(len(model['nodes']) - 1)
        redraw()

    def _clear(_):
        for k in ['nodes', 'elements', 'constraints', 'loads']:
            model[k].clear()
        model['sel'] = None; redraw()

    def _parse_sections():
        secs, mats = {}, {}
        for line in sec_text.value.strip().split('\n'):
            if ':' not in line: continue
            key, rest = line.split(':', 1); key = key.strip()
            p = {}
            for part in rest.split(','):
                if '=' not in part: continue
                k, v = part.split('='); p[k.strip()] = float(v.strip())
            mats[key] = [p.get('E', 210000.0)]
            secs[key]  = [p.get('A', 1.0), key]
        return secs, mats

    def _generate(_):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf

        axn  = {0: 'x', 1: 'y'}
        secs, mats = _parse_sections()

        print('nodal_coordinates = np.array([')
        for i, (x, y) in enumerate(model['nodes']):
            print(f'    [{x:8.1f}, {y:8.1f}],   # Knoten {i+1}')
        print('])\n')

        print('elements = [')
        for i, (ni, nj, sk) in enumerate(model['elements']):
            print(f'    [{ni}, {nj}, "{sk}"],   # Stab {i+1}')
        print(']\n')

        print('materials = {')
        for name, vals in mats.items():
            print(f'    "{name}": [{vals[0]:.1f}],')
        print('}\n')

        print('sections = {')
        for key, (A, mat) in secs.items():
            print(f'    "{key}": [{A:.2f}, "{mat}"],')
        print('}\n')

        print('constraints = [')
        for nd, a, v in model['constraints']:
            print(f'    [{nd}, {a}, {v:.1f}],   # Knoten {nd+1}: {axn[a]} gesperrt')
        print(']\n')

        print('loads = [')
        for nd, a, f in model['loads']:
            print(f'    [{nd}, {a}, {f:.1f}],   # Knoten {nd+1}: F_{axn[a]} = {f:.1f} N')
        print(']')

        sys.stdout = old_stdout
        code_out.value = buf.getvalue()

    undo_btn.on_click(_undo)
    clear_btn.on_click(_clear)
    gen_btn.on_click(_generate)
    mode_sel.observe(lambda c: (model.update({'sel': None}), redraw()), names='value')

    # -- Layout ---------------------------------------------------------------

    sep     = w.HTML('<hr style="margin:5px 0; border-color:#ddd">')
    sidebar = w.VBox([
        w.HTML('<b>Modus</b>'),
        mode_sel,
        coord_lbl,
        sep,
        w.HTML('<b>Stab-Key</b>'),
        sec_key_in,
        sep,
        w.HTML('<b>Eigenschaften [TEST v2]</b>'),
        lager_box,
        sep,
        last_box,
        sep,
        w.HTML('<b>Querschnitte</b> <small>(key: A=..., E=...)</small>'),
        sec_text,
        sep,
        w.HBox([undo_btn, clear_btn]),
        gen_btn,
    ], layout=w.Layout(width='255px', padding='6px 8px', border='1px solid #ddd'))

    display(w.VBox([
        w.HBox([fig.canvas, sidebar],
               layout=w.Layout(align_items='flex-start', gap='10px')),
        code_out,
    ]))
    redraw()
