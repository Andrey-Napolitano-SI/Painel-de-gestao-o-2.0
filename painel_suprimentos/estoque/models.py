from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):

    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('BAIXO', 'BAIXO'),
        ('CRITICO', 'CRITICO'),
    ]

    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    minimo = models.IntegerField()
    local = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):

    TIPO_CHOICES = [
        ('ENTRADA', 'ENTRADA'),
        ('SAIDA', 'SAIDA'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    responsavel = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto} - {self.tipo}'


class Chamado(models.Model):

    CATEGORIAS = (
        ('SUPORTE', 'Suporte'),
        ('REQUISICAO', 'Requisição'),
    )

    STATUS = (
        ('ABERTO', 'Aberto'),
        ('ANDAMENTO', 'Em andamento'),
        ('FINALIZADO', 'Finalizado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=200)

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS
    )

    descricao = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='ABERTO'
    )

    data_abertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo