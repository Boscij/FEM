# Finite-Elemente-Methode (FEM) mit Python

Willkommen! In diesem Repository lernst du mittels verschiedener Notebooks die Finite-Elemente-Methode kennen.

Viel Erfolg und viel Spass, 
Sebastian

---

## Überblick

Du hast zwei Möglichkeiten, die Notebooks in diesem Repository direkt im Browser zu öffnen, ohne etwas zu installieren:

- **JupyterLite**: Öffne das Notebook über den JupyterLite-Link. Das startet sofort im Browser und ist ideal zum schnellen Ausprobieren. Deine Änderungen werden dort aber nicht automatisch dauerhaft gespeichert. Wenn du Resultate und Lösungen behalten willst, lade am Ende deine bearbeitete Version des Notebooks herunter.

- **Google Colab**: Öffne das Notebook über den Colab-Link. Das läuft ebenfalls im Browser, aber auf Googles Servern. Dafür brauchst du ein Google-Konto. Damit deine Änderungen gespeichert bleiben, erstelle zu Beginn eine eigene Kopie des Notebooks: **File → Save a copy in Drive** (oder „In Drive speichern“). 


### Notebook 0: Warm-up
Python-Grundlagen und Jupyter-Workflow, damit du dich später auf die Mechanik konzentrieren kannst.
[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=00_Jupyter_Python.ipynb)  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/00_Jupyter_Python.ipynb)  

### Notebook 1: Übung 05 – Fachwerk
Elementsteifigkeitsmatrizen, Assemblierung, Randbedingungen und Spannungsberechnung am Beispiel eines ebenen Fachwerks.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=01_UE05_Fachwerk.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/01_UE05_Fachwerk.ipynb)

### Notebook 2: Matrixsteifigkeitsmethode
Von lokaler Elementsteifigkeit über Transformation bis zur globalen Strukturmatrix und zu den Verschiebungen/Kräften.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=02_Matrixsteifigkeitsmethode.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/02_Matrixsteifigkeitsmethode.ipynb)
---

## So benutzt du die Notebooks

- **Exercise-Version**: enthält bewusst Lücken (`...`).  
  Dein Ziel ist zuerst ganz pragmatisch: **Lücken füllen, Notebook ausführen, Resultate erhalten**.  
  Wenn der Code läuft, lies ihn nochmals **als Ganzes** durch, damit du verstehst, wie die Teile zusammenspielen (Elementebene, Assemblierung, Randbedingungen, Lösung).

- **Verstehen statt nur “Copy-Paste”**: Schau dir die Funktionen und Datenstrukturen vollständig an und überlege dir bei jeder Zeile: *Was kommt rein, was geht raus, und warum macht das Sinn?*

- **Anpassen**: Ändere danach gezielt das Modell für deine Problemstellung:
  - Geometrie (Knoten, Elemente)
  - Material und Querschnitt
  - Lagerungen und Lasten  
  Kleine Änderungen zuerst, dann schrittweise komplexer.