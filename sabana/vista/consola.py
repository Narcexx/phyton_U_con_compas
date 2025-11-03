def mostrar_mapa(sabana):
    ancho = sabana.ancho
    alto = sabana.alto
    mapa = [["." for _ in range(ancho)] for _ in range(alto)]

    # colocar comidas
    for c in sabana.comidas:
        x, y = c.posicion
        if c.tipo == "pasto":
            mapa[y][x] = "P"
        elif c.tipo == "carne":
            mapa[y][x] = "C"
        elif c.tipo == "insectos":
            mapa[y][x] = "I"

    # colocar animales
    for a in sabana.animales:
        x, y = a.posicion
        letra = a.__class__.__name__[0].upper()  # E, L o C
        mapa[y][x] = letra

    # mostrar mapa
    print("\nSABANA:")
    for fila in mapa:
        print(" ".join(fila))