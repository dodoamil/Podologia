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
