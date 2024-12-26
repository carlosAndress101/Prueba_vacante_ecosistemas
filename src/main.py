from Class.comisiones import Comisiones
import os


if __name__ == "__main__":
    directorio = os.path.dirname(os.path.abspath(__file__))
    comisiones = Comisiones(directorio)
    comisiones.run()
