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
Dasselbe Fachwerk wie in Notebook 1, aber die gesamte FE-Logik ist in `fem_core.py` gekapselt. Der Fokus liegt auf dem **Zusammenspiel der Funktionen**: Modell definieren, `assemble_K` aufrufen, mit `solve_system` lösen, Ergebnisse mit `postprocessing` und `plot_results` auswerten.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=02_Matrixsteifigkeitsmethode_Funktionen.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/02_Matrixsteifigkeitsmethode_Funktionen.ipynb)

### Notebook 3: Matrixsteifigkeitsmethode – Tool
Erweiterung von Notebook 2 zum **einsatzbereiten Berechnungs-Tool**: Modelldaten anpassen, eine Zelle ausführen, alle Ergebnisse (Verschiebungen, Lagerkräfte, Dehnungen, Spannungen, Normalkräfte) und Visualisierung erhalten. Geeignet für beliebige ebene Fachwerke.

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

## Kapitel 3 – Ausblick: FEM mit 2D Elementen

*Folgt in Kürze.*
