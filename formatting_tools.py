def cash(amount):
    if amount >= 0:
        return '$ %s' % round(amount, 2)
    else:
        return '-$ %s' % round(amount*-1, 2)

def month(value):
    month_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return month_list[value-1]

def parse_mode(mode):
    modes = {'==': 'igual',
             '!=': 'diferente',
             '<': 'menor que',
             '>': 'mayor que',
             '<=': 'menor o igual',
             '>=': 'mayor o igual'}
    return modes.get(mode, mode)
