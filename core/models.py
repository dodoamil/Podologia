from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone / WhatsApp")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Endereço")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações Especiais", help_text="Ex: diabético, sensibilidade, alergias, etc.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('A', 'Agendado'),
        ('C', 'Concluído'),
        ('X', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    data_hora = models.DateTimeField(verbose_name="Data e Horário")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

class Atendimento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='atendimentos')
    agendamento = models.OneToOneField(Agendamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='atendimento')
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data do Atendimento")
    procedimento = models.CharField(max_length=200, verbose_name="Procedimento Realizado", help_text="Descreva brevemente o que foi feito")
    profissional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True, verbose_name="Como foi o atendimento?")

    def __str__(self):
        return f"Atendimento: {self.cliente.nome} - {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Histórico de Atendimentos"

class Pagamento(models.Model):
    FORMA_PGTO_CHOICES = [
        ('PIX', 'Pix'),
        ('DIN', 'Dinheiro'),
        ('CC', 'Cartão de Crédito'),
        ('CD', 'Cartão de Débito'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    atendimento = models.OneToOneField(Atendimento, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=3, choices=FORMA_PGTO_CHOICES)
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Pgto {self.cliente.nome} - R$ {self.valor}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Financeiro"


class FichaAnamnese(models.Model):
    TIPO_PE_CHOICES = [
        ('N', 'Normal'),
        ('P', 'Plano (Chato)'),
        ('C', 'Cavo'),
    ]
    TIPO_PISADA_CHOICES = [
        ('N', 'Neutra'),
        ('P', 'Pronada (Para dentro)'),
        ('S', 'Supinada (Para fora)'),
    ]

    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='anamnese')
    data_preenchimento = models.DateTimeField(auto_now_add=True, verbose_name='Data de Preenchimento')
    
    # Histórico Médico
    diabetico = models.BooleanField(default=False, verbose_name='Diabético?')
    hipertenso = models.BooleanField(default=False, verbose_name='Hipertenso?')
    problema_circulacao = models.BooleanField(default=False, verbose_name='Problemas de Circulação?')
    problema_cicatrizacao = models.BooleanField(default=False, verbose_name='Problemas de Cicatrização?')
    alergias = models.TextField(null=True, blank=True, verbose_name='Alergias (Quais?)')
    cirurgias_anteriores = models.TextField(null=True, blank=True, verbose_name='Cirurgias Anteriores')
    medicamentos_continuos = models.TextField(null=True, blank=True, verbose_name='Uso de Medicamentos Mencionados')
    
    # Hábitos e Biomecânica
    pratica_esporte = models.BooleanField(default=False, verbose_name='Pratica Esportes?')
    tipo_calcado_diario = models.CharField(max_length=200, null=True, blank=True, verbose_name='Tipos de Calçados mais usados no Dia a Dia')
    tipo_pe = models.CharField(max_length=1, choices=TIPO_PE_CHOICES, default='N', verbose_name='Tipo de Pé')
    tipo_pisada = models.CharField(max_length=1, choices=TIPO_PISADA_CHOICES, default='N', verbose_name='Tipo de Pisada')
    
    # Queixa
    alteracoes_unhas = models.TextField(null=True, blank=True, verbose_name='Alterações nas Unhas (Onicocriptose, etc)')
    queixa_principal = models.TextField(verbose_name='Queixa Principal / Motivo da Consulta')

    def __str__(self):
        return f'Anamnese - {self.cliente.nome}'

    class Meta:
        verbose_name = 'Ficha de Anamnese'
        verbose_name_plural = 'Fichas de Anamnese'


class Material(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome do Material/Insumo')
    unidade_medida = models.CharField(max_length=50, verbose_name='Unidade de Medida', help_text='Ex: Unidade, Caixa, Pacote, ML')
    quantidade_atual = models.IntegerField(default=0, verbose_name='Quantidade Atual', help_text='Atualizado automaticamente pelas movimentações')
    estoque_minimo = models.IntegerField(default=5, verbose_name='Estoque Mínimo Ideal')

    def __str__(self):
        return f'{self.nome} - Saldo: {self.quantidade_atual} {self.unidade_medida}'

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Estoque de Materiais'

class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTO = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMENTO, verbose_name='Tipo de Movimentação')
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name='Data da Movimentação')
    motivo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Motivo (Opcional)', help_text='Ex: Compra, Reposição, Descarte, Uso no Atendimento X')

    def save(self, *args, **kwargs):
        if self.pk is None: # Apenas atualiza o saldo em novas movimentações
            if self.tipo == 'E':
                self.material.quantidade_atual += self.quantidade
            elif self.tipo == 'S':
                self.material.quantidade_atual -= self.quantidade
            self.material.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.material.nome} ({self.quantidade})'

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Histórico de Movimentações'
