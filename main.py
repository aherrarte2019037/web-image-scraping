import re
import csv

def cargar_buffer(entrada, inicio, tamano_buffer):
    buffer = entrada[inicio:inicio + tamano_buffer]
    if len(buffer) < tamano_buffer:
        buffer += "eof"
    return buffer

def encontrar_producto(buffer):
    """
    Busca un producto (nombre e imagen) en el buffer actual.
    Retorna una tupla (nombre, imagen, caracteres_procesados) o (None, None, 0)
    """
    # Patrón para título del producto - ajustado a la estructura HTML
    patron_titulo = re.compile(r'<h2 class="product-name">\s*<a[^>]*>([^<]+)</a>\s*</h2>')
    match_titulo = patron_titulo.search(buffer)
    
    if not match_titulo:
        return None, None, 0
        
    # Patrón para imagen
    inicio_busqueda = match_titulo.start()
    # Buscamos hacia atrás desde el título para encontrar la imagen asociada
    buffer_anterior = buffer[max(0, inicio_busqueda - 500):inicio_busqueda]
    patron_imagen = re.compile(r'<img\s+src="([^"]+)"[^>]*alt="product"')
    match_imagen = patron_imagen.search(buffer_anterior)
    
    if not match_imagen:
        return None, None, 0
        
    nombre = match_titulo.group(1).strip()
    imagen = match_imagen.group(1)
    chars_procesados = inicio_busqueda + match_titulo.end()
    
    return nombre, imagen, chars_procesados

def procesar_html(contenido_html, tamano_buffer=1024):
    """
    Procesa el HTML usando buffers y retorna lista de productos.
    """
    productos = []
    inicio = 0
    
    while True:
        buffer = cargar_buffer(contenido_html, inicio, tamano_buffer)
        
        if buffer == "eof":
            break
            
        nombre, imagen, chars_procesados = encontrar_producto(buffer)
        
        if nombre and imagen:
            productos.append((nombre, imagen))
            inicio += chars_procesados
        else:
            # Si no encontramos producto, avanzamos la mitad del buffer
            inicio += tamano_buffer // 2
            
    return productos

def exportar_productos(productos, archivo_salida):
    """
    Exporta la lista de productos a un archivo CSV.
    """
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nombre del Producto", "URL de la Imagen"])
        writer.writerows(productos)

def main():
    # Cargar archivo HTML
    with open('template.html', 'r', encoding='utf-8') as f:
        contenido_html = f.read()
    
    # Procesar HTML y encontrar productos
    productos = procesar_html(contenido_html)
    
    # Exportar resultados
    exportar_productos(productos, 'products.csv')
    
    print(f"Se han exportado {len(productos)} productos al archivo products.csv")
    # Mostrar algunos ejemplos de los productos encontrados
    for i, (nombre, imagen) in enumerate(productos[:5], 1):
        print(f"\nProducto {i}:")
        print(f"Nombre: {nombre}")
        print(f"Imagen: {imagen}")

if __name__ == "__main__":
    main()