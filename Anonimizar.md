# 🧩 Protocolo de Anonimización de TACS

Antes de realizar la segmentación con la herramienta *Liver Segmentation Tool*, es **obligatorio anonimizar los TACS** para eliminar cualquier dato sensible o información identificable del paciente.

A continuación se describe el procedimiento paso a paso:

---

## 🪶 1. Descargar el programa de anonimización

Descarga el programa **Dicom Cleaner** desde el siguiente enlace:  
👉 [https://www.softpedia.com/get/Science-CAD/Dicom-Cleaner.shtml](https://www.softpedia.com/get/Science-CAD/Dicom-Cleaner.shtml)

Este software es gratuito y permite limpiar los metadatos de los archivos DICOM.

---

## ⚙️ 2. Abrir Dicom Cleaner

1.Al ejecutar el programa, se abrirá una interfaz principal con varias pestañas en la parte inferior.

2.Selecciona las siguientes pestañas de la parte inferior de la interfaz: 

<img width="1443" height="170" alt="image" src="https://github.com/user-attachments/assets/b4370920-4e5c-4b77-aae1-28360e76d34b" />


3.Selecciona las pestañas correspondientes para editar los campos de **Nombre del Paciente** e **ID del Paciente**.


---

## 🧾 3. Configuración de los campos

Rellena los campos de la siguiente manera:

- **Nombre del paciente:** `EOM_XXXX`  
  Donde `XXXX` es el número correspondiente al ID del paciente.  
  *(Debe coincidir con el archivo original sin anonimizar)*

- **ID del paciente:** `DDMMAAAA`  
  Donde se indica la **fecha del estudio** en el formato DíaMesAño (por ejemplo, `05082009`).

---

## 📂 4. Proceso de anonimización

1. **Importar** el estudio DICOM que se desea anonimizar usando el botón **Import**.  
2. **Limpiar** los datos presionando el botón **Clean**.  
3. **Exportar** los archivos ya anonimizados seleccionando la carpeta donde se guardarán mediante el botón **Export**.

---



## ✅ Resultado final

Cada carpeta de paciente debe contener únicamente archivos DICOM **anonimizados**, con nombres estandarizados según el formato indicado.

Una vez completado este proceso, los datos estarán listos para su segmentación automática con *Liver Segmentation Tool*.
