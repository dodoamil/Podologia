import datetime
from .models import Cliente

def aniversariantes_hoje(request):
    hoje = datetime.date.today()
    aniversariantes = Cliente.objects.filter(data_nascimento__day=hoje.day, data_nascimento__month=hoje.month)
    return {'aniversariantes_hoje': aniversariantes}
