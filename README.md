# 🩻 Liver Segmentation Tool

## ⚠️ ¡IMPORTANTE!

Para el correcto uso de esta herramienta, los estudios de TAC deben haber pasado por un **protocolo de anonimización**, eliminando toda información personal y cualquier archivo no DICOM.  
👉 En este repositorio encontrarás el archivo **`Anonimizar.md`**, donde se explica paso a paso cómo realizar este proceso correctamente.

---

## Descripción

Esta aplicación permite realizar la **segmentación automática del hígado** a partir de estudios **DICOM** de TAC utilizando la herramienta [**TotalSegmentator**](https://github.com/wasserth/TotalSegmentator?tab=readme-ov-file).

Fue desarrollada para **facilitar el uso de TotalSegmentator**, ofreciendo una **interfaz gráfica simple** que permite seleccionar una carpeta con múltiples pacientes y obtener automáticamente las segmentaciones correspondientes del hígado en formato `.nii`.

📘 **Autores:**  
- Helena Caparrós Castellano  
- Alejandro Cabello Bonal  

---

## ⚙️ Requisitos previos

Antes de ejecutar la herramienta, asegúrate de tener instalado:

1. **Python 3.x**  
   👉 [Descargar desde aquí](https://www.python.org/downloads/)  
   Durante la instalación, marca la opción **“Add to PATH”**.

2. **Microsoft Visual C++ Build Tools**  
   👉 [Descargar desde aquí](https://visualstudio.microsoft.com/visual-cpp-build-tools/)  
   Durante la instalación, selecciona:
   - ✅ *Desktop development with C++*  
   - ✅ *Windows 10/11 SDK*

---

## 🧩 Instalación de dependencias

Abre una terminal (CMD o PowerShell) y ejecuta:

```bash
pip install numpy
pip install SimpleITK
pip install totalsegmentator
pip install torch
```

---

## ▶️ Ejecución del programa

1. Guarda el archivo del programa (`LiverSegmentation.py`) en tu carpeta de usuario, por ejemplo:
   ```
   C:\Users\TuUsuario\
   ```

2. En la terminal, ejecuta:

   ```bash
   python LiverSegmentation.py
   ```

3. Se abrirá una ventana donde deberás **seleccionar la carpeta raíz** que contenga las carpetas de los pacientes (cada una con sus archivos DICOM), estos archivos deben de estar en formato: nombre_del_archivo [fecha].

4. El programa procesará cada carpeta automáticamente, mostrando una **barra de progreso** y el nombre del estudio que está siendo segmentado.

<img width="531" height="185" alt="image" src="https://github.com/user-attachments/assets/fb67b467-65ce-4dc6-8ef5-d1bd7a1e5a65" />


5. Al finalizar, aparecerá un mensaje indicando que todas las segmentaciones se completaron correctamente.

---

## 💾 Salida de resultados

Las segmentaciones generadas se guardan en las **mismas carpetas donde se encuentran los archivos DICOM**, con nombres como:

```
Liver_<NombrePaciente> [<Fecha>].nii
```

Por ejemplo:
```
Liver_EOM_1 [05082009].nii
```

---

## 🧠 Funcionamiento interno

- El programa busca automáticamente las carpetas que contienen archivos `.dcm`.
- Convierte los DICOM a formato `.nii` y los reorienta al espacio estándar RAS.
- Utiliza la función `totalsegmentator()` con los parámetros:
  - `roi_subset=["liver"]`
  - `ml=True`, `fast=True`, `device="cpu"`
  - `output_type="nii"`

---

## 🖥️ Interfaz gráfica

Durante el procesamiento, el usuario verá:
- Una ventana con una **barra de progreso** y el nombre del TAC actual.
- Un mensaje final indicando la **finalización exitosa** del proceso.

---

## 📚 Créditos

Este proyecto está basado en la herramienta **[TotalSegmentator](https://github.com/wasserth/TotalSegmentator)** desarrollada por **Fabian Isensee et al.**

El presente código fue adaptado con fines docentes y de optimización para la segmentación hepática automatizada.

---

