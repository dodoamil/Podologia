from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Agendamento, Atendimento, Pagamento, FichaAnamnese, Material, MovimentacaoEstoque

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


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_atual', 'unidade_medida', 'estoque_minimo', 'status_estoque')
    search_fields = ('nome',)
    readonly_fields = ('quantidade_atual',)

    def status_estoque(self, obj):
        if obj.quantidade_atual <= obj.estoque_minimo:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ Abaixo do Mínimo')
        return format_html('<span style="color: green;">{}</span>', 'Normal')
    status_estoque.short_description = 'Status'

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('material', 'tipo', 'quantidade', 'data', 'motivo')
    list_filter = ('tipo', 'data')
    search_fields = ('material__nome', 'motivo')
