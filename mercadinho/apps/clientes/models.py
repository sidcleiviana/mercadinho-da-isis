from django.db import models

from apps.core.models import ModeloBase
from apps.produtos.models import Produto
from apps.vendas.models import Venda


class ClienteVirtual(ModeloBase):
    nome = models.CharField(max_length=120, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cliente Virtual"
        verbose_name_plural = "Clientes Virtuais"

    def __str__(self):
        return self.nome


class AtendimentoVirtual(ModeloBase):
    class Status(models.TextChoices):
        AGUARDANDO = "aguardando", "Aguardando"
        EM_ATENDIMENTO = "em_atendimento", "Em Atendimento"
        FINALIZADO = "finalizado", "Finalizado"
        DESISTIU = "desistiu", "Desistiu"

    class EstadoConversa(models.TextChoices):
        INICIADO = "iniciado", "Iniciado"
        EM_NEGOCIACAO = "em_negociacao", "Em Negociacao"
        ADICIONANDO_PRODUTOS = "adicionando_produtos", "Adicionando Produtos"
        FINALIZANDO = "finalizando", "Finalizando"
        CONCLUIDO = "concluido", "Concluido"

    cliente_virtual = models.ForeignKey(
        ClienteVirtual,
        on_delete=models.PROTECT,
        related_name="atendimentos",
    )
    horario_programado = models.DateTimeField()
    horario_inicio = models.DateTimeField(null=True, blank=True)
    horario_finalizacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    estado_conversa = models.CharField(
        max_length=24,
        choices=EstadoConversa.choices,
        default=EstadoConversa.INICIADO,
    )
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    venda = models.OneToOneField(
        Venda,
        on_delete=models.PROTECT,
        related_name="atendimento_virtual",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["horario_programado", "id"]
        verbose_name = "Atendimento Virtual"
        verbose_name_plural = "Atendimentos Virtuais"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(valor_total__gte=0),
                name="atendimento_virtual_valor_total_nao_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.cliente_virtual} - {self.get_status_display()}"


class PedidoVirtual(ModeloBase):
    atendimento = models.ForeignKey(
        AtendimentoVirtual,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="pedidos_virtuais",
    )
    quantidade = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Pedido Virtual"
        verbose_name_plural = "Pedidos Virtuais"

    def __str__(self):
        return f"{self.atendimento} - {self.produto} x {self.quantidade}"


class EventoCliente(ModeloBase):
    class Tipo(models.TextChoices):
        ENTROU_FILA = "entrou_fila", "Entrou na fila"
        AGUARDANDO = "aguardando", "Aguardando"
        ATENDIMENTO_INICIADO = "atendimento_iniciado", "Atendimento iniciado"
        ATENDIDO = "atendido", "Atendido"
        DESISTIU = "desistiu", "Desistiu"

    atendimento = models.ForeignKey(
        AtendimentoVirtual,
        on_delete=models.PROTECT,
        related_name="eventos",
        null=True,
        blank=True,
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    mensagem = models.CharField(max_length=255)
    data = models.DateTimeField()

    class Meta:
        ordering = ["-data", "-id"]
        verbose_name = "Evento de Cliente"
        verbose_name_plural = "Eventos de Clientes"

    def __str__(self):
        return self.mensagem


class InteracaoConversa(ModeloBase):
    class Origem(models.TextChoices):
        SISTEMA = "sistema", "Sistema"
        OPERADORA = "operadora", "Operadora"

    class Acao(models.TextChoices):
        INICIAR = "iniciar", "Iniciar"
        SIM_TEMOS = "sim_temos", "Sim, temos"
        NAO_TEMOS = "nao_temos", "Nao temos"
        VER_OUTROS_PRODUTOS = "ver_outros_produtos", "Ver outros produtos"
        FINALIZAR_COMPRA = "finalizar_compra", "Finalizar compra"
        CANCELAR_ATENDIMENTO = "cancelar_atendimento", "Cancelar atendimento"

    atendimento = models.ForeignKey(
        AtendimentoVirtual,
        on_delete=models.PROTECT,
        related_name="interacoes",
    )
    origem = models.CharField(max_length=12, choices=Origem.choices)
    acao = models.CharField(max_length=24, choices=Acao.choices)
    mensagem = models.CharField(max_length=255)
    data = models.DateTimeField()

    class Meta:
        ordering = ["data", "id"]
        verbose_name = "Interacao de Conversa"
        verbose_name_plural = "Interacoes de Conversa"

    def __str__(self):
        return self.mensagem
