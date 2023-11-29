from datetime import datetime, timedelta

def calculate_fecha_limite(fecha_reclamo):
        delta_dias = 15

        fecha_limite = fecha_reclamo
        dias_habiles = 0

        while dias_habiles < delta_dias:
            fecha_limite += timedelta(days=1)
            if fecha_limite.weekday() not in [5, 6]:
                dias_habiles += 1

        return fecha_limite

def date_now():
     return datetime.now()