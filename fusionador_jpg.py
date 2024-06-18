import os
from PIL import Image
import pdfrw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def natural_sort_key(s):
    """Clave de ordenación natural para ordenar números en cadenas."""
    import re
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def convertir_a_pdf(carpeta, nombre_pdf):
    imagenes = [imagen for imagen in os.listdir(carpeta) if imagen.lower().endswith(('.png', '.jpg', '.jpeg'))]
    imagenes = sorted(imagenes, key=natural_sort_key)

    pdf_writer = pdfrw.PdfWriter()

    for imagen_nombre in imagenes:
        imagen_path = os.path.join(carpeta, imagen_nombre)

        # Abrir la imagen y obtener su tamaño
        img = Image.open(imagen_path)
        width, height = img.size

        # Crear un PDF temporal para la imagen
        pdf_temporal = f"{imagen_nombre[:-4]}.pdf"
        c = canvas.Canvas(pdf_temporal, pagesize=(width, height))
        c.drawImage(imagen_path, 0, 0, width, height)
        c.save()

        # Agregar la página PDF temporal al escritor de PDF
        pdf_reader = pdfrw.PdfReader(pdf_temporal)
        pdf_writer.addpages(pdf_reader.pages)

        # Eliminar el PDF temporal
        os.remove(pdf_temporal)

    # Guardar el archivo PDF resultante
    pdf_writer.write(nombre_pdf)


# Carpeta que contiene las imágenes
carpeta_imagenes = "data"

# Nombre del archivo PDF de salida
nombre_pdf = "cap47.pdf"

convertir_a_pdf(carpeta_imagenes, nombre_pdf)