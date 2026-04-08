from django.contrib import admin
from .models import Cliente, Agendamento, Atendimento, Pagamento, FichaAnamnese

class FichaAnamneseInline(admin.StackedInline):
    model = FichaAnamnese
    can_delete = False
    verbose_name_plural = 'fichas de anamnese'

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'data_nascimento')
    search_fields = ('nome', 'telefone')
    inlines = (FichaAnamneseInline,)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_hora', 'status')
    list_filter = ('status', 'data_hora')
    search_fields = ('cliente__nome',)

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'procedimento', 'profissional')
    list_filter = ('data', 'profissional')
    search_fields = ('cliente__nome', 'procedimento')

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor', 'forma_pagamento', 'pago', 'data_pagamento')
    list_filter = ('pago', 'forma_pagamento', 'data_pagamento')
    search_fields = ('cliente__nome',)
