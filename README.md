# Finite-Elemente-Methode (FEM) mit Python

Willkommen! In diesem Repository lernst du mittels verschiedener Notebooks die Finite-Elemente-Methode kennen.

Viel Erfolg und viel Spass,
Sebastian

---

## Überblick

Du hast zwei Möglichkeiten, die Notebooks direkt im Browser zu öffnen, ohne etwas zu installieren:

- **JupyterLite**: Startet sofort im Browser. Änderungen nicht dauerhaft gespeichert – am Ende herunterladen.
- **Google Colab**: Läuft auf Googles Servern (Google-Konto nötig). Für dauerhafte Speicherung: **File → Save a copy in Drive**.

---

## Kapitel 1 – Vorübung

### Notebook 0: Warm-up
Python-Grundlagen und Jupyter-Workflow.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=00_Jupyter_Python.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/00_Jupyter_Python.ipynb)

---

## Kapitel 2 – FEM mit 1D Stab- und Balkenelementen (Matrixsteifigkeitsmethode)

### Notebook 1: Übung 05 – Fachwerk
Einstieg in die FEM: Elementsteifigkeitsmatrizen, Transformation, Assemblierung, Randbedingungen und Spannungsberechnung – alles Schritt für Schritt am konkreten Beispiel eines ebenen Fachwerks.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=01_UE05_Fachwerk.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/01_UE05_Fachwerk.ipynb)

### Notebook 2: Matrixsteifigkeitsmethode – Funktionen
Dasselbe Fachwerk wie in Notebook 1, aber jetzt werden alle Schritte in **eigene Funktionen** verpackt: `element_stiffness_matrix`, `incidence_table`, `assemble_K`, `solve_system`. Die Funktionen entstehen direkt im Notebook – so ist nachvollziehbar, was darin steckt.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=02_Matrixsteifigkeitsmethode_Funktionen.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/02_Matrixsteifigkeitsmethode_Funktionen.ipynb)

### Notebook 3: Matrixsteifigkeitsmethode – Tool
Die Funktionen aus Notebook 2 sind nun in `fem_core.py` ausgelagert und werden nur noch importiert. Das Notebook konzentriert sich auf das **Modell und die Ergebnisse** – kein Implementierungsdetail mehr sichtbar. Geeignet als einsatzbereites Tool für beliebige ebene Fachwerke.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=03_Matrixsteifigkeitsmethode_Tool.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/03_Matrixsteifigkeitsmethode_Tool.ipynb)

### Notebook 4: Pre-Processing – Grafische Modelleingabe
Erweiterung von Notebook 3 um eine **interaktive GUI**: Knoten, Stäbe, Lager und Lasten werden grafisch per Maus eingezeichnet. Der erzeugte Code wird direkt im Notebook als Modell-Input übernommen und berechnet – kein manuelles Eintippen mehr.

> **Hinweis:** Benötigt eine lokale Jupyter-Umgebung oder Google Colab (nicht JupyterLite).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/04_Pre_processing.ipynb)

### Notebook 5: Zug-Druck-Balkenelemente
Erweiterung der Matrixsteifigkeitsmethode auf **Balkenelemente**: drei Freiheitsgrade je Knoten (u, v, φ) statt zwei. Die Elementsteifigkeitsmatrix umfasst nun auch Biegeanteile; als Schnittgrössen kommen Querkraft V und Biegemoment M zu den Normalkräften N hinzu.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=05_Balkenelemente.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/05_Balkenelemente.ipynb)

---

## Kapitel 3 – FEM mit 2D Elementen

### Notebook 6: Triangulare Membranelemente
Erster Schritt in 2D: das **lineare Dreieckselement (CST)** für eine vorgespannte Membran unter Druck. Pro Knoten nur **ein Freiheitsgrad** (Auslenkung $w$). Wir leiten Formfunktionen $N_i(x,y)$ direkt her, bauen $\underline{\underline{B}}$ und $\underline{\underline{K}}^e$ auf und vergleichen das FEM-Ergebnis mit der analytischen Fourier-Lösung für eine Rechteck-Membran. Zusatzaufgabe: E-förmige Membran mit Polygon-Vernetzung.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=06_Membran.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/06_Membran.ipynb)

### Notebook 7: Isoparametrische Vierecks-Elemente
**Bilineare Q4-Elemente** im ebenen Spannungszustand (plane stress). Neue Bausteine: Referenzelement, **Jacobi-Matrix**, Gauss-Integration. Pro Knoten 2 Freiheitsgrade ($u, v$), $\underline{\underline{K}}^e$ ist $8\times 8$. Beispiel: ein Kragarm aus Stahlblech, Validierung gegen die Bernoulli-Balken-Theorie.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=07_Isoparametric.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/07_Isoparametric.ipynb)

---

## Kapitel 4 – Ausblick: FEM mit 3D Elementen

### Notebook 8: 10-Knoten-Tetraederelement (T10)
Erweiterung in 3D mit dem **quadratischen 10-Knoten-Tetraederelement**: 4 Eckknoten + 6 Mid-Edge-Knoten. Volle $6\times 6$ Konstitutivmatrix mit Lamé-Konstanten, 5-Punkt-Gauss-Integration auf dem Tetraeder, $\underline{\underline{K}}^e$ ist $30\times 30$. Beispiel: 3D-Kragarm-Block mit Stress-Visualisierung. T10 ist – anders als Q4 – **frei von Shear-Locking**.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=08_Tetraeder_10_Knoten.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/08_Tetraeder_10_Knoten.ipynb)
