import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import SimpleITK as sitk
from totalsegmentator.python_api import totalsegmentator
import threading
import queue
import sys
import multiprocessing


# Configuración para ejecutables
if getattr(sys, 'frozen', False):
    multiprocessing.freeze_support()
    os.chdir(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable))

# ----------------------------
# Funciones de procesamiento
# ----------------------------

def encontrar_carpetas_con_dicom(base_path):
    """Busca recursivamente carpetas que contengan archivos .dcm."""
    carpetas = set()
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith('.dcm'):
                carpetas.add(root)
                break
    return sorted(list(carpetas))

def reorient_to_RAS(sitk_image):
    """Reorienta la imagen al espacio estándar RAS."""
    img_array = sitk.GetArrayFromImage(sitk_image)
    img_array_ras = img_array[:, :, ::-1]
    img_array_ras = np.flip(img_array_ras, axis=2)
    new_img = sitk.GetImageFromArray(img_array_ras)
    new_img.SetSpacing(sitk_image.GetSpacing())
    new_img.SetOrigin(sitk_image.GetOrigin())
    new_img.SetDirection(np.eye(3).flatten())
    return new_img

def procesar_estructura(root_folder, progress_window, progress_var, status_var):
    """Procesa carpetas con DICOMs mostrando progreso."""
    carpetas = encontrar_carpetas_con_dicom(root_folder)
    total = len(carpetas)
    
    for i, dicom_folder in enumerate(carpetas, 1):
        nombre_carpeta = os.path.basename(dicom_folder)
        parent_folder = os.path.dirname(dicom_folder)  # Carpeta padre 
        status_var.set(f"Procesando: {nombre_carpeta}")
        progress_var.set((i / total) * 100)
        progress_window.update()
        
        try:
            reader = sitk.ImageSeriesReader()
            series_IDs = reader.GetGDCMSeriesIDs(dicom_folder)
            if not series_IDs:
                continue

            series_file_names = reader.GetGDCMSeriesFileNames(dicom_folder, series_IDs[0])
            reader.SetFileNames(series_file_names)
            image = reader.Execute()

            image_ras = reorient_to_RAS(image)
            temp_path = os.path.join(tempfile.gettempdir(), f"temp_{nombre_carpeta}.nii")
            sitk.WriteImage(image_ras, temp_path)

            # Extraer el nombre base y la fecha
            if '[' in nombre_carpeta and ']' in nombre_carpeta:
                nombre_base = nombre_carpeta.split('[')[0].strip()
                fecha = nombre_carpeta.split('[')[1].replace(']', '').strip() 
                output_name = f"Liver_{nombre_base} [{fecha}].nii"  # Sin compresión (.nii)
            else:
                output_name = f"Liver_{nombre_carpeta}.nii"  # Por si no tiene formato esperado

            # Guardar en la carpeta padre, no en la subcarpeta con fecha
            output_path = os.path.join(parent_folder, output_name)
            
            totalsegmentator(
                input=temp_path,
                output=output_path,
                roi_subset=["liver"], 
                ml=True,
                fast=True,
                device="cpu",
                output_type="nii"  # Forzar salida como .nii (no .nii.gz)
            )
            
            os.remove(temp_path)
            
        except Exception as e:
            print(f"❌ Error en {nombre_carpeta}: {str(e)}")

# ----------------------------
# Interfaz gráfica
# ----------------------------

def run_app():
    root = tk.Tk()
    root.title("Segmentación DICOM")
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Selecciona la carpeta raíz con los pacientes")
    if not folder_selected:
        root.destroy()
        return

    progress_window = tk.Toplevel()
    progress_window.title("Procesando segmentaciones")
    progress_window.geometry("500x150")
    progress_window.protocol("WM_DELETE_WINDOW", lambda: None)
    
    status_var = tk.StringVar(value="Preparando...")
    progress_var = tk.DoubleVar(value=0)
    
    tk.Label(progress_window, textvariable=status_var, font=('Arial', 10)).pack(pady=10)
    ttk.Progressbar(progress_window, variable=progress_var, maximum=100, length=400).pack(pady=5)
    tk.Label(progress_window, text="Por favor espere...").pack(pady=5)

    q = queue.Queue()

    def ejecutar():
        try:
            procesar_estructura(folder_selected, progress_window, progress_var, status_var)
            q.put(("ok", "¡Todas las segmentaciones completadas!"))
        except Exception as e:
            q.put(("error", str(e)))

    def revisar_cola():
        try:
            tipo, mensaje = q.get_nowait()
            progress_window.destroy()
            root.destroy()
            if tipo == "ok":
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)
        except queue.Empty:
            root.after(100, revisar_cola)

    threading.Thread(target=ejecutar, daemon=True).start()
    revisar_cola()
    root.mainloop()

# ----------------------------
# Bloque principal
# ----------------------------

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        multiprocessing.freeze_support()
    
    run_app()

