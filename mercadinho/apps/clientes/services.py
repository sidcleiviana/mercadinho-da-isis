import random
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.configuracoes.models import Configuracao
from apps.core.models import Expediente
from apps.core.services import obter_expediente
from apps.produtos.models import Produto
from apps.vendas.models import Venda
from apps.vendas.services import (
    adicionar_produto_por_codigo,
    cancelar_venda,
    iniciar_venda,
)

from .models import (
    AtendimentoVirtual,
    ClienteVirtual,
    EventoCliente,
    InteracaoConversa,
    PedidoVirtual,
)


INTERVALO_MINIMO_CHEGADA_MINUTOS = 2
INTERVALO_MAXIMO_CHEGADA_MINUTOS = 8

NOMES_MENINAS = [
    "Ísis",
    "Alice",
    "Helena",
    "Laura",
    "Valentina",
    "Sofia",
    "Cecilia",
    "Manuela",
    "Luna",
    "Liz",
    "Beatriz",
    "Júlia",
    "Maria",
    "Heloísa",
    "Clara",
    "Elisa",
    "Aurora",
    "Catarina",
    "Melissa",
    "Bianca",
    "Ana",
    "Fernanda",
]

NOMES_MENINOS = [
    "Miguel",
    "Arthur",
    "Theo",
    "Davi",
    "Bernardo",
    "Gabriel",
    "Lucas",
    "Pedro",
    "Rafael",
    "Enzo",
    "Samuel",
    "Heitor",
    "Matheus",
    "Henrique",
    "Benjamin",
    "Caio",
    "Joaquim",
    "Nicolas",
    "Felipe",
    "Daniel",
    "Carlos",
    "Joao",
    "Gustavo",
]

NOMES_INICIAIS = NOMES_MENINAS + NOMES_MENINOS

MENSAGENS_CHEGADA = [
    "{nome} acabou de entrar no mercadinho.",
    "{nome} está procurando produtos.",
    "{nome} veio comprar doces.",
    "{nome} entrou na fila.",
    "{nome} está esperando atendimento.",
    "{nome} quer comprar um carrinho.",
    "{nome} está escolhendo produtos.",
    "{nome} acabou de chegar.",
    "{nome} entrou no mercado.",
    "{nome} veio conhecer o mercadinho.",
]

MENSAGENS_ATENDIMENTO = [
    "{nome} está no balcão escolhendo produtos.",
    "{nome} começou a conversar no atendimento.",
    "{nome} está fazendo uma comprinha.",
    "{nome} foi chamado para o atendimento.",
]

MENSAGENS_DESISTENCIA = [
    "{nome} foi embora depois de esperar um pouco.",
    "{nome} esperou bastante e saiu da fila.",
    "{nome} decidiu voltar outro dia.",
    "{nome} desistiu após tempo de espera.",
]

MENSAGENS_CANCELAMENTO = [
    "{nome} saiu do atendimento e foi embora.",
    "{nome} decidiu voltar mais tarde.",
    "{nome} encerrou o atendimento sem compra.",
]

MENSAGENS_ATENDIDO = [
    "{nome} terminou a compra feliz.",
    "{nome} foi atendido com carinho.",
    "{nome} saiu com a comprinha pronta.",
    "{nome} adorou o atendimento.",
]

MENSAGENS_COMPRA = [
    "{nome} comprou {quantidade} produto(s).",
    "{nome} saiu feliz com {quantidade} produto(s).",
    "{nome} levou {quantidade} produto(s) do mercadinho.",
    "{nome} finalizou uma compra com {quantidade} produto(s).",
]


def garantir_clientes_iniciais():
    for nome in NOMES_INICIAIS:
        ClienteVirtual.objects.get_or_create(nome=nome, defaults={"ativo": True})


def obter_configuracao_clientes():
    configuracao = Configuracao.objects.order_by("id").first()
    if configuracao:
        return {
            "quantidade_maxima": configuracao.quantidade_maxima_clientes_virtuais_por_dia,
            "tempo_espera_minutos": configuracao.tempo_maximo_espera,
            "horario_abertura": configuracao.horario_abertura,
            "horario_fechamento": configuracao.horario_fechamento,
            "intervalo_minimo_chegada": INTERVALO_MINIMO_CHEGADA_MINUTOS,
            "intervalo_maximo_chegada": INTERVALO_MAXIMO_CHEGADA_MINUTOS,
        }
    return {
        "quantidade_maxima": 12,
        "tempo_espera_minutos": 10,
        "horario_abertura": time(8, 0),
        "horario_fechamento": time(18, 0),
        "intervalo_minimo_chegada": INTERVALO_MINIMO_CHEGADA_MINUTOS,
        "intervalo_maximo_chegada": INTERVALO_MAXIMO_CHEGADA_MINUTOS,
    }


def expediente_esta_aberto():
    return obter_expediente().status == Expediente.Status.ABERTO


def _intervalo_do_dia(agora, configuracao):
    abertura = timezone.make_aware(
        datetime.combine(agora.date(), configuracao["horario_abertura"]),
        timezone.get_current_timezone(),
    )
    fechamento = timezone.make_aware(
        datetime.combine(agora.date(), configuracao["horario_fechamento"]),
        timezone.get_current_timezone(),
    )
    inicio = max(agora, abertura)
    if fechamento <= inicio:
        fechamento = inicio + timedelta(hours=1)
    return inicio, fechamento


def gerar_atendimentos_do_dia(agora=None):
    agora = agora or timezone.now()
    if not expediente_esta_aberto():
        return []

    garantir_clientes_iniciais()
    return []


def clientes_previstos_hoje():
    configuracao = obter_configuracao_clientes()
    total_clientes = ClienteVirtual.objects.filter(ativo=True).count()
    return min(configuracao["quantidade_maxima"], total_clientes)


def atendimentos_do_dia(agora=None):
    agora = agora or timezone.now()
    return AtendimentoVirtual.objects.filter(horario_programado__date=agora.date())


def clientes_restantes_hoje(agora=None):
    gerar_atendimentos_do_dia(agora)
    return max(clientes_previstos_hoje() - atendimentos_do_dia(agora).count(), 0)


def _intervalo_ate_proximo_cliente(agora, quantidade_gerada):
    configuracao = obter_configuracao_clientes()
    minimo = configuracao["intervalo_minimo_chegada"]
    maximo = max(configuracao["intervalo_maximo_chegada"], minimo)
    rng = random.Random(f"{agora.date().isoformat()}:{quantidade_gerada}")
    return timedelta(minutes=rng.randint(minimo, maximo))


def _momento_base_para_proximo_cliente(agora):
    expediente = obter_expediente()
    ultimo_encerrado = (
        atendimentos_do_dia(agora)
        .filter(
            status__in=[
                AtendimentoVirtual.Status.FINALIZADO,
                AtendimentoVirtual.Status.DESISTIU,
            ],
            horario_finalizacao__isnull=False,
        )
        .order_by("-horario_finalizacao", "-id")
        .first()
    )
    if ultimo_encerrado:
        return ultimo_encerrado.horario_finalizacao
    return expediente.aberto_em or agora


def _cliente_disponivel_para_chegada(agora):
    clientes_usados = atendimentos_do_dia(agora).values_list("cliente_virtual_id", flat=True)
    clientes_base = ClienteVirtual.objects.filter(ativo=True).exclude(id__in=clientes_usados)
    clientes = list(clientes_base.order_by("nome", "id"))
    if not clientes:
        return None

    gerados = len(clientes_usados)
    genero_preferido = "menina" if gerados % 2 == 0 else "menino"
    nomes_genero = set(NOMES_MENINAS if genero_preferido == "menina" else NOMES_MENINOS)
    clientes_genero = [cliente for cliente in clientes if cliente.nome in nomes_genero]
    candidatos = clientes_genero or clientes

    ultimos_clientes = list(
        AtendimentoVirtual.objects.select_related("cliente_virtual")
        .order_by("-horario_programado", "-id")
        .values_list("cliente_virtual__nome", flat=True)[:3]
    )
    sem_repeticao_recente = [
        cliente for cliente in candidatos if cliente.nome not in ultimos_clientes
    ]
    if sem_repeticao_recente:
        candidatos = sem_repeticao_recente

    rng = random.Random(f"{agora.date().isoformat()}:{gerados}:cliente:{genero_preferido}")
    return candidatos[rng.randrange(len(candidatos))]


def _mensagem_variada(modelos, atendimento, agora, **contexto):
    contexto.setdefault("nome", atendimento.cliente_virtual.nome)
    seed = f"{agora.date().isoformat()}:{atendimento.pk}:{atendimento.cliente_virtual.nome}"
    rng = random.Random(seed)
    return rng.choice(modelos).format(**contexto)


def existe_cliente_ativo_no_fluxo(agora=None):
    return AtendimentoVirtual.objects.filter(
        status__in=[
            AtendimentoVirtual.Status.AGUARDANDO,
            AtendimentoVirtual.Status.EM_ATENDIMENTO,
        ]
    ).exists()


def registrar_evento(atendimento, tipo, mensagem, data=None):
    data = data or timezone.now()
    evento, _ = EventoCliente.objects.get_or_create(
        atendimento=atendimento,
        tipo=tipo,
        defaults={"mensagem": mensagem, "data": data},
    )
    return evento


def processar_chegadas(agora=None):
    agora = agora or timezone.now()
    if not expediente_esta_aberto():
        return []

    gerar_atendimentos_do_dia(agora)
    if existe_cliente_ativo_no_fluxo(agora):
        return []

    gerados = atendimentos_do_dia(agora).count()
    if gerados >= clientes_previstos_hoje():
        return []

    momento_base = _momento_base_para_proximo_cliente(agora)
    if agora < momento_base + _intervalo_ate_proximo_cliente(agora, gerados):
        return []

    cliente = _cliente_disponivel_para_chegada(agora)
    if cliente is None:
        return []

    with transaction.atomic():
        atendimento = AtendimentoVirtual.objects.create(
            cliente_virtual=cliente,
            horario_programado=agora,
            status=AtendimentoVirtual.Status.AGUARDANDO,
            valor_total=Decimal("0.00"),
        )
        evento = registrar_evento(
            atendimento,
            EventoCliente.Tipo.ENTROU_FILA,
            _mensagem_variada(MENSAGENS_CHEGADA, atendimento, agora),
            data=agora,
        )
    return [evento]


def processar_desistencias(agora=None):
    agora = agora or timezone.now()
    if not expediente_esta_aberto():
        return []

    configuracao = obter_configuracao_clientes()
    limite = agora - timedelta(minutes=configuracao["tempo_espera_minutos"])
    atendimentos = AtendimentoVirtual.objects.filter(
        status=AtendimentoVirtual.Status.AGUARDANDO,
        horario_programado__lte=limite,
    ).select_related("cliente_virtual")

    eventos = []
    with transaction.atomic():
        for atendimento in atendimentos:
            atendimento.status = AtendimentoVirtual.Status.DESISTIU
            atendimento.horario_finalizacao = agora
            atendimento.save(update_fields=["status", "horario_finalizacao", "atualizado_em"])
            eventos.append(
                registrar_evento(
                    atendimento,
                    EventoCliente.Tipo.DESISTIU,
                    _mensagem_variada(MENSAGENS_DESISTENCIA, atendimento, agora),
                    data=agora,
                )
            )
    return eventos


def processar_fluxo_clientes(agora=None):
    agora = agora or timezone.now()
    if not expediente_esta_aberto():
        return {"chegadas": [], "desistencias": []}
    desistencias = processar_desistencias(agora)
    if desistencias:
        return {"chegadas": [], "desistencias": desistencias}
    chegadas = processar_chegadas(agora)
    return {"chegadas": chegadas, "desistencias": desistencias}


def fila_ativa(agora=None):
    agora = agora or timezone.now()
    processar_fluxo_clientes(agora)
    return AtendimentoVirtual.objects.filter(
        status=AtendimentoVirtual.Status.AGUARDANDO,
    ).select_related("cliente_virtual").order_by("horario_programado", "id")


def eventos_recentes(limite=10):
    return EventoCliente.objects.select_related(
        "atendimento", "atendimento__cliente_virtual"
    ).order_by("-data", "-id")[:limite]


def atendimento_em_andamento():
    return (
        AtendimentoVirtual.objects.filter(status=AtendimentoVirtual.Status.EM_ATENDIMENTO)
        .select_related("cliente_virtual", "venda")
        .first()
    )


def iniciar_atendimento(atendimento_id, agora=None):
    agora = agora or timezone.now()
    if not expediente_esta_aberto():
        raise ValidationError("Abra o expediente antes de iniciar um atendimento.")

    with transaction.atomic():
        if AtendimentoVirtual.objects.select_for_update().filter(
            status=AtendimentoVirtual.Status.EM_ATENDIMENTO
        ).exists():
            raise ValidationError("Ja existe um atendimento em andamento.")

        atendimento = AtendimentoVirtual.objects.select_for_update().select_related(
            "cliente_virtual", "venda"
        ).get(pk=atendimento_id)

        if atendimento.status != AtendimentoVirtual.Status.AGUARDANDO:
            raise ValidationError("Apenas clientes aguardando podem ser atendidos.")
        if atendimento.horario_programado > agora:
            raise ValidationError("Este cliente ainda nao entrou na fila.")

        venda = atendimento.venda
        if venda is None:
            venda = iniciar_venda(tipo_cliente=Venda.TipoCliente.VIRTUAL)

        atendimento.status = AtendimentoVirtual.Status.EM_ATENDIMENTO
        atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.INICIADO
        atendimento.horario_inicio = agora
        atendimento.venda = venda
        atendimento.save(
            update_fields=[
                "status",
                "estado_conversa",
                "horario_inicio",
                "venda",
                "atualizado_em",
            ]
        )
        registrar_evento(
            atendimento,
            EventoCliente.Tipo.ATENDIMENTO_INICIADO,
            _mensagem_variada(MENSAGENS_ATENDIMENTO, atendimento, agora),
            data=agora,
        )
        preparar_conversa(atendimento, agora)
    return atendimento


def finalizar_atendimento_por_venda(venda, agora=None):
    agora = agora or timezone.now()
    try:
        atendimento = AtendimentoVirtual.objects.select_related("cliente_virtual").get(
            venda=venda
        )
    except AtendimentoVirtual.DoesNotExist:
        return None

    if atendimento.status != AtendimentoVirtual.Status.EM_ATENDIMENTO:
        return atendimento

    with transaction.atomic():
        atendimento = AtendimentoVirtual.objects.select_for_update().get(pk=atendimento.pk)
        atendimento.status = AtendimentoVirtual.Status.FINALIZADO
        atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.CONCLUIDO
        atendimento.horario_finalizacao = agora
        atendimento.valor_total = venda.valor_total
        atendimento.save(
            update_fields=[
                "status",
                "estado_conversa",
                "horario_finalizacao",
                "valor_total",
                "atualizado_em",
            ]
        )
        quantidade_produtos = sum(item.quantidade for item in venda.itens.all())
        mensagem = _mensagem_variada(MENSAGENS_ATENDIDO, atendimento, agora)
        if quantidade_produtos:
            mensagem = _mensagem_variada(
                MENSAGENS_COMPRA,
                atendimento,
                agora,
                quantidade=quantidade_produtos,
            )
        registrar_evento(
            atendimento,
            EventoCliente.Tipo.ATENDIDO,
            mensagem,
            data=agora,
        )
    return atendimento


def cancelar_atendimento(atendimento, agora=None):
    agora = agora or timezone.now()
    with transaction.atomic():
        atendimento = AtendimentoVirtual.objects.select_for_update().select_related(
            "cliente_virtual", "venda"
        ).get(pk=atendimento.pk)
        if atendimento.status != AtendimentoVirtual.Status.EM_ATENDIMENTO:
            raise ValidationError("Apenas atendimentos em andamento podem ser cancelados.")

        if atendimento.venda and atendimento.venda.status == Venda.Status.EM_ANDAMENTO:
            cancelar_venda(atendimento.venda)

        atendimento.status = AtendimentoVirtual.Status.DESISTIU
        atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.CONCLUIDO
        atendimento.horario_finalizacao = agora
        atendimento.save(
            update_fields=[
                "status",
                "estado_conversa",
                "horario_finalizacao",
                "atualizado_em",
            ]
        )
        registrar_evento(
            atendimento,
            EventoCliente.Tipo.DESISTIU,
            _mensagem_variada(MENSAGENS_CANCELAMENTO, atendimento, agora),
            data=agora,
        )
    return atendimento


def cancelar_atendimento_por_venda(venda, agora=None):
    try:
        atendimento = AtendimentoVirtual.objects.get(venda=venda)
    except AtendimentoVirtual.DoesNotExist:
        return None

    if atendimento.status == AtendimentoVirtual.Status.EM_ATENDIMENTO:
        atendimento.status = AtendimentoVirtual.Status.DESISTIU
        atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.CONCLUIDO
        atendimento.horario_finalizacao = agora or timezone.now()
        atendimento.save(
            update_fields=[
                "status",
                "estado_conversa",
                "horario_finalizacao",
                "atualizado_em",
            ]
        )
        registrar_evento(
            atendimento,
            EventoCliente.Tipo.DESISTIU,
            _mensagem_variada(MENSAGENS_CANCELAMENTO, atendimento, atendimento.horario_finalizacao),
            data=atendimento.horario_finalizacao,
        )
    return atendimento


def registrar_interacao(atendimento, origem, acao, mensagem, data=None):
    return InteracaoConversa.objects.create(
        atendimento=atendimento,
        origem=origem,
        acao=acao,
        mensagem=mensagem,
        data=data or timezone.now(),
    )


def produto_solicitado_atual(atendimento):
    return (
        PedidoVirtual.objects.filter(atendimento=atendimento)
        .select_related("produto")
        .order_by("id")
        .first()
    )


def proximo_produto_para_pedido(produto_atual=None):
    produtos = list(Produto.objects.filter(ativo=True).order_by("nome", "id"))
    if not produtos:
        return None
    if produto_atual is None:
        return produtos[0]
    for indice, produto in enumerate(produtos):
        if produto.pk == produto_atual.pk:
            return produtos[(indice + 1) % len(produtos)]
    return produtos[0]


def preparar_conversa(atendimento, agora=None):
    agora = agora or timezone.now()
    atendimento = AtendimentoVirtual.objects.select_related("cliente_virtual").get(
        pk=atendimento.pk
    )
    if atendimento.status != AtendimentoVirtual.Status.EM_ATENDIMENTO:
        raise ValidationError("A conversa exige atendimento em andamento.")

    pedido = produto_solicitado_atual(atendimento)
    if pedido is None:
        produto = proximo_produto_para_pedido()
        if produto is None:
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.SISTEMA,
                InteracaoConversa.Acao.INICIAR,
                "Nao ha produtos cadastrados para este atendimento.",
                data=agora,
            )
            atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.FINALIZANDO
            atendimento.save(update_fields=["estado_conversa", "atualizado_em"])
            return atendimento
        pedido = PedidoVirtual.objects.create(
            atendimento=atendimento,
            produto=produto,
            quantidade=1,
        )

    if not atendimento.interacoes.exists():
        registrar_interacao(
            atendimento,
            InteracaoConversa.Origem.SISTEMA,
            InteracaoConversa.Acao.INICIAR,
            f"Cliente pede {pedido.quantidade} unidade(s) de {pedido.produto.nome}.",
            data=agora,
        )

    if atendimento.estado_conversa == AtendimentoVirtual.EstadoConversa.INICIADO:
        atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.EM_NEGOCIACAO
        atendimento.save(update_fields=["estado_conversa", "atualizado_em"])
    return atendimento


def opcoes_conversa(atendimento):
    if atendimento.status != AtendimentoVirtual.Status.EM_ATENDIMENTO:
        return []
    if atendimento.estado_conversa == AtendimentoVirtual.EstadoConversa.EM_NEGOCIACAO:
        return [
            InteracaoConversa.Acao.SIM_TEMOS,
            InteracaoConversa.Acao.NAO_TEMOS,
            InteracaoConversa.Acao.VER_OUTROS_PRODUTOS,
            InteracaoConversa.Acao.CANCELAR_ATENDIMENTO,
        ]
    if atendimento.estado_conversa == AtendimentoVirtual.EstadoConversa.ADICIONANDO_PRODUTOS:
        return [
            InteracaoConversa.Acao.FINALIZAR_COMPRA,
            InteracaoConversa.Acao.CANCELAR_ATENDIMENTO,
        ]
    if atendimento.estado_conversa == AtendimentoVirtual.EstadoConversa.FINALIZANDO:
        return [
            InteracaoConversa.Acao.CANCELAR_ATENDIMENTO,
        ]
    return []


def contexto_conversa(atendimento):
    preparar_conversa(atendimento)
    atendimento.refresh_from_db()
    return {
        "atendimento": atendimento,
        "pedido": produto_solicitado_atual(atendimento),
        "interacoes": atendimento.interacoes.all(),
        "opcoes": opcoes_conversa(atendimento),
    }


def responder_conversa(atendimento_id, acao, agora=None):
    agora = agora or timezone.now()
    with transaction.atomic():
        atendimento = (
            AtendimentoVirtual.objects.select_for_update()
            .select_related("cliente_virtual", "venda")
            .get(pk=atendimento_id)
        )
        if atendimento.status != AtendimentoVirtual.Status.EM_ATENDIMENTO:
            raise ValidationError("Apenas atendimentos em andamento aceitam respostas.")

        if acao not in opcoes_conversa(atendimento):
            raise ValidationError("Resposta indisponivel para o estado atual da conversa.")

        pedido = produto_solicitado_atual(atendimento)
        if acao == InteracaoConversa.Acao.SIM_TEMOS:
            if pedido is None:
                raise ValidationError("Nenhum produto solicitado para adicionar.")
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.OPERADORA,
                acao,
                f"Sim, temos {pedido.produto.nome}.",
                data=agora,
            )
            for _ in range(pedido.quantidade):
                adicionar_produto_por_codigo(atendimento.venda, pedido.produto.codigo_barras)
            atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.ADICIONANDO_PRODUTOS
            atendimento.save(update_fields=["estado_conversa", "atualizado_em"])
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.SISTEMA,
                InteracaoConversa.Acao.VER_OUTROS_PRODUTOS,
                "Produto adicionado a venda. A compra pode ser finalizada.",
                data=agora,
            )
            return atendimento

        if acao == InteracaoConversa.Acao.NAO_TEMOS:
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.OPERADORA,
                acao,
                "Nao temos esse produto.",
                data=agora,
            )
            if atendimento.venda and atendimento.venda.status == Venda.Status.EM_ANDAMENTO:
                cancelar_venda(atendimento.venda)
            atendimento.status = AtendimentoVirtual.Status.FINALIZADO
            atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.CONCLUIDO
            atendimento.horario_finalizacao = agora
            atendimento.valor_total = Decimal("0.00")
            atendimento.save(
                update_fields=[
                    "status",
                    "estado_conversa",
                    "horario_finalizacao",
                    "valor_total",
                    "atualizado_em",
                ]
            )
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.SISTEMA,
                InteracaoConversa.Acao.NAO_TEMOS,
                "Atendimento encerrado sem venda.",
                data=agora,
            )
            return atendimento

        if acao == InteracaoConversa.Acao.VER_OUTROS_PRODUTOS:
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.OPERADORA,
                acao,
                "Vamos verificar outros produtos.",
                data=agora,
            )
            produto_atual = pedido.produto if pedido else None
            proximo_produto = proximo_produto_para_pedido(produto_atual)
            if proximo_produto is None:
                raise ValidationError("Nao ha produtos cadastrados para sugerir.")
            if pedido:
                pedido.produto = proximo_produto
                pedido.quantidade = 1
                pedido.save(update_fields=["produto", "quantidade", "atualizado_em"])
            else:
                pedido = PedidoVirtual.objects.create(
                    atendimento=atendimento,
                    produto=proximo_produto,
                    quantidade=1,
                )
            atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.EM_NEGOCIACAO
            atendimento.save(update_fields=["estado_conversa", "atualizado_em"])
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.SISTEMA,
                InteracaoConversa.Acao.INICIAR,
                f"Cliente pede {pedido.quantidade} unidade(s) de {pedido.produto.nome}.",
                data=agora,
            )
            return atendimento

        if acao == InteracaoConversa.Acao.FINALIZAR_COMPRA:
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.OPERADORA,
                acao,
                "Finalizar compra.",
                data=agora,
            )
            atendimento.estado_conversa = AtendimentoVirtual.EstadoConversa.FINALIZANDO
            atendimento.save(update_fields=["estado_conversa", "atualizado_em"])
            return atendimento

        if acao == InteracaoConversa.Acao.CANCELAR_ATENDIMENTO:
            registrar_interacao(
                atendimento,
                InteracaoConversa.Origem.OPERADORA,
                acao,
                "Cancelar atendimento.",
                data=agora,
            )
            cancelar_atendimento(atendimento, agora)
            return atendimento

    return atendimento
