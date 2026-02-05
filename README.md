# Finite-Elemente-Methode (FEM) mit Python

Willkommen im FEM-Kosmos. In diesem Repository lernst du mittels verschiedener Notebooks die Finite-Elemente-Methode nicht über “hier ist die Formel, glaub mir”, sondern indem du sie Schritt für Schritt selbst zusammenbaust. Wir starten klein, bleiben logisch, und am Schluss löst dein Code deine mechanischen Probleme, bevor er überhaupt weiss, dass er FEM macht.

Die Notebooks sind für Studierende in meinem FEM-Kurs an der ZHAW gedacht und bauen aufeinander auf. Du brauchst keine Programmierkarriere. Du brauchst nur Neugier, ein bisschen Geduld und die Bereitschaft, ein paar `...` durch echte Formeln zu ersetzen.

Viel Spass 
Sebastian

---

## Überblick

### Notebook 0: Warm-up
Python-Grundlagen und Jupyter-Workflow, damit du dich später auf die Mechanik konzentrieren kannst.
[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=00_Jupyter_Python.ipynb)  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/00_Jupyter_Python.ipynb)  

### Notebook 1: Matrixsteifigkeitsmethode
Von lokaler Elementsteifigkeit über Transformation bis zur globalen Strukturmatrix und zu den Verschiebungen/Kräften.

[![Open in JupyterLite](https://img.shields.io/badge/Open%20in-JupyterLite-blue)](https://Boscij.github.io/FEM/lab/index.html?path=01_Matrixsteifigkeitsmethode.ipynb)  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Boscij/FEM/blob/main/content/01_Matrixsteifigkeitsmethode.ipynb)  
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