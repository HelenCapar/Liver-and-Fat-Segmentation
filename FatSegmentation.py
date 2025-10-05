import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import SimpleITK as sitk
from totalsegmentator.python_api import totalsegmentator
import threading
import queue
import json
from pathlib import Path
import sys
import multiprocessing

# Agrega al inicio del archivo, después de los imports:
if getattr(sys, 'frozen', False):
    # Si estamos en un ejecutable
    multiprocessing.freeze_support()
    # Asegurar que las rutas sean absolutas
    os.chdir(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable))


# ----------------------------
# Funciones de gestión de licencia
# ----------------------------

def verificar_licencia():
    """Verifica si existe una licencia válida."""
    config_path = Path.home() / ".totalsegmentator" / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                if config.get("license_number", "").strip():
                    return True
        except:
            pass
    return False

def pedir_licencia():
    """Muestra ventana para ingresar licencia."""
    license_window = tk.Toplevel()
    license_window.title("Licencia TotalSegmentator")
    license_window.geometry("400x150")
    
    tk.Label(license_window, text="Ingresa tu licencia de TotalSegmentator:").pack(pady=10)
    license_entry = tk.Entry(license_window, width=40)
    license_entry.pack(pady=5)
    
    resultado = [False]
    
    def guardar_licencia():
        license_number = license_entry.get().strip()
        if not license_number:
            messagebox.showerror("Error", "¡La licencia no puede estar vacía!")
            return
        
        config_path = Path.home() / ".totalsegmentator" / "config.json"
        config_path.parent.mkdir(exist_ok=True)
        
        config_data = {
            "license_number": license_number,
            "totalseg_id": f"totalseg_{os.urandom(4).hex().upper()}",
            "send_usage_stats": False
        }
        
        try:
            with open(config_path, "w") as f:
                json.dump(config_data, f, indent=4)
            resultado[0] = True
            license_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la licencia:\n{e}")
    
    tk.Button(license_window, text="Guardar", command=guardar_licencia).pack(pady=10)
    license_window.grab_set()
    license_window.wait_window()
    
    return resultado[0]

# ----------------------------
# Funciones de procesamiento mejoradas
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

def procesar_estructura(root_folder, progress_window, progress_var, status_var, task_name="tissue_4_types"):
    carpetas = encontrar_carpetas_con_dicom(root_folder)
    total = len(carpetas)
    
    for i, dicom_folder in enumerate(carpetas, 1):
        nombre_carpeta = os.path.basename(dicom_folder)
        parent_folder = os.path.dirname(dicom_folder)  # Carpeta padre (EOM_70)
        status_var.set(f"Procesando: {nombre_carpeta}")
        progress_var.set((i / total) * 100)
        progress_window.update()
        
        try:
            # Procesamiento DICOM
            reader = sitk.ImageSeriesReader()
            series_IDs = reader.GetGDCMSeriesIDs(dicom_folder)
            if not series_IDs:
                continue

            series_file_names = reader.GetGDCMSeriesFileNames(dicom_folder, series_IDs[0])
            reader.SetFileNames(series_file_names)
            image = reader.Execute()

            # Reorientar y guardar temporalmente
            image_ras = reorient_to_RAS(image)
            temp_path = os.path.join(tempfile.gettempdir(), f"temp_{nombre_carpeta}.nii")
            sitk.WriteImage(image_ras, temp_path)

            # Extraer nombre base y fecha
            if '[' in nombre_carpeta and ']' in nombre_carpeta:
                nombre_base = nombre_carpeta.split('[')[0].strip()  # "EOM_70"
                fecha = nombre_carpeta.split('[')[1].replace(']', '').strip()  # "04062005"
                output_name = f"Fat_{nombre_base} [{fecha}].nii"  # Nombre deseado
            else:
                output_name = f"Fat_{nombre_carpeta}.nii"

            # Guardar en la carpeta padre (EOM_70)
            output_path = os.path.join(parent_folder, output_name)
            
            # Segmentación con parámetros para output .nii
            totalsegmentator(
                input=temp_path,
                output=output_path,
                task=task_name,
                ml=True,
                device="cpu",
                output_type="nii"  # Forzar salida como .nii
            )
            
            # Limpieza
            os.remove(temp_path)
            
        except Exception as e:
            print(f"❌ Error en {nombre_carpeta}: {str(e)}")

# ----------------------------
# Interfaz gráfica mejorada
# ----------------------------

def run_app():
    # Configuración más robusta de la ventana principal
    root = tk.Tk()
    root.title("Segmentación DICOM")
    root.withdraw()  # Oculta la ventana principal inmediatamente
    
    # Verificar licencia
    if not verificar_licencia():
        if not pedir_licencia():
            root.destroy()
            return

    # Selección de carpeta
    folder_selected = filedialog.askdirectory(title="Selecciona la carpeta raíz con los pacientes")
    if not folder_selected:
        root.destroy()
        return

    # Ventana de progreso
    progress_window = tk.Toplevel()
    progress_window.title("Procesando segmentaciones")
    progress_window.geometry("500x150")
    progress_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Evita cerrar la ventana
    
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
# Bloque principal mejorado
# ----------------------------

if __name__ == "__main__":
    # Prevención de ejecución múltiple en .exe
    if getattr(sys, 'frozen', False):
        # Si estamos en un ejecutable
        multiprocessing.freeze_support()
    
    run_app()