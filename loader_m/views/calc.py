class Medicao:
    def __init__(self, temp, umid, temp2):
        self.temperatura = temp
        self.umidade = umid
        self.temperatura2 = temp2

def array_medicoes(meds, med):
    from collections import deque
    fila = deque(meds)
    fila.append(med)
    if len(fila) > 10:
        fila.popleft()
    return fila

def get_media(meds):
    try:
        if len(meds) > 0:
            temps = 0
            temps2 = 0
            umids = 0
            for med in meds:
                temps = temps+med.temperatura
                temps2 = temps2+med.temperatura2
                umids = umids+med.umidade
            if temps != 0:
                temps = temps/len(meds)
            if temps2 != 0:
                temps2 = temps2/len(meds)
            if umids != 0:
                umids = umids/len(meds)
            return Medicao(round(temps,2),round(umids,2),round(temps2,2))
        else:
            return Medicao(0,0,0)
    except Exception as e:
        print('erro', e)
        return Medicao(0,0,0)