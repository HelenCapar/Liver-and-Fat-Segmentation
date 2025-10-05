# 🩻 Liver and Fat Segmentation Tool

## ⚠️ ¡IMPORTANTE!

Para garantizar un procesamiento correcto, los estudios de TAC deben haberse sometido previamente a un **protocolo de anonimización y limpieza**, eliminando toda información identificable del paciente y cualquier archivo **no DICOM** incluido en la descarga original del estudio.

👉 En este repositorio encontrarás el archivo **`Anonimizar.md`**, donde se explica paso a paso cómo realizar este proceso correctamente.

---

## Descripción

Esta aplicación permite realizar la **segmentación automática del hígado o de la grasa visceral (VAT) y subcutánea (SAT)** a partir de estudios **DICOM** de TAC utilizando la herramienta [**TotalSegmentator**](https://github.com/wasserth/TotalSegmentator?tab=readme-ov-file).

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
pip install tk
```

---


## <img width="64" height="44" alt="image" src="https://github.com/user-attachments/assets/6c4970e8-2cde-42c2-91e7-6e073e81e111" /> Ejecución del programa **LiverSegmentation**


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


## <img width="64" height="38" alt="image" src="https://github.com/user-attachments/assets/1d5d0488-b94e-4371-a2a9-1da2db258d8c" /> Ejecución del programa **FatSegmentation**

El funcionamiento del programa **FatSegmentation** es prácticamente idéntico al de **LiverSegmentation**, con la única diferencia de que **requiere una licencia** para poder utilizar la segmentación del tejido **subcutáneo (SAT)** y **visceral (VAT)** mediante [**TotalSegmentator**](https://github.com/wasserth/TotalSegmentator?tab=readme-ov-file).

Al ejecutar el programa por primera vez, se abrirá automáticamente una ventana solicitando la **clave de licencia**.  
Esta licencia debe solicitarse a traves de la pagina [**TotalSegmentator**](https://github.com/wasserth/TotalSegmentator?tab=readme-ov-file), donde se indica el procedimiento en su README.
Cada licencia es **única para cada usuario** y, una vez recibida por correo electrónico, puede introducirse directamente en el campo correspondiente de la ventana emergente.

<img width="495" height="216" alt="Captura de pantalla 2025-10-05 183402" src="https://github.com/user-attachments/assets/9c092162-d3fd-48e0-8807-df858f7090cf" />

Una vez introducida y validada la licencia, el programa continuará con el mismo flujo de trabajo que **LiverSegmentation**:

1. Solicitar la carpeta raíz que contenga las carpetas de los pacientes con sus estudios DICOM.  
2. Procesar automáticamente cada carpeta mostrando una **barra de progreso** y el nombre del estudio que se está segmentando.  
3. Guardar los resultados de la segmentación de **grasa subcutánea y visceral** en formato `.nii` dentro de las carpetas correspondientes.


## 💾 Salida de resultados

Las segmentaciones generadas se guardan en las **mismas carpetas donde se encuentran los archivos DICOM**, con nombres como:

```
Liver_<NombrePaciente> [<DiaMesAño>].nii
Fat_<NombrePaciente> [<DiaMesAño>].nii
```
Por ejemplo:
```
Liver_EOM_1 [05082009].nii
Fat_EOM_1 [05082009].nii
```

---


## 🖥️ Interfaz gráfica

Durante el procesamiento, el usuario verá:
- Una ventana con una **barra de progreso** y el nombre del TAC actual.
- Un mensaje final indicando la **finalización exitosa** del proceso.

---

## 📚 Créditos

Este proyecto está basado en la herramienta [**TotalSegmentator**](https://github.com/wasserth/TotalSegmentator), desarrollada por **Fabian Isensee et al.**

El código aquí presentado ha sido adaptado con fines **docentes y de investigación**, para facilitar la segmentación automática hepática y del tejido adiposo (subcutáneo y visceral).

---

> 🧾 **Aviso sobre la licencia**
>
> La segmentación de tejido adiposo (SAT y VAT) utiliza componentes del software *TotalSegmentator* que requieren una **licencia académica no comercial**.  
> Cada usuario debe solicitar su propia licencia gratuita en la página oficial de [TotalSegmentator](https://github.com/wasserth/TotalSegmentator) antes de ejecutar este módulo.  
>
> Este repositorio **no incluye** ningún archivo, modelo, ni licencia de *TotalSegmentator*, y **no redistribuye** su software.  
> El uso del mismo está sujeto a los términos de su licencia original.


