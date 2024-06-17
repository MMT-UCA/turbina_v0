from tomllib import load

class Datos:
    @classmethod
    def cargar_datos(cls, file_path):
        with open(file_path, "rb") as f:
            data = load(f)
        
        for section, values in data.items():
            for key, value in values.items():
                setattr(cls, key, value)

Datos.cargar_datos("Datos.toml")





