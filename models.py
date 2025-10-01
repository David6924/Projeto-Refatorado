from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
import copy

# =====================
#  MODELS ORIGINAIS
# =====================

@dataclass
class Fornecedor:
    """dados de contato de um fornecedor"""
    id: int
    nome: str
    empresa: str
    telefone: str
    email: str
    morada: str

    def __str__(self):
        """isso vai ser usado para exibir o fornecedor em uma lista"""
        return f"{self.id} - {self.nome} ({self.empresa})"


@dataclass
class Localizacao:
    # repsresenta uma localização física no inventário, como um armazém ou uma loja mesmo
    id: int
    nome: str
    endereco: str = ""

    def __str__(self):
         #aquela mesma parada lá, de exibir a localização em uma lista
        return f"{self.id} - {self.nome}"


@dataclass
class ComponenteKit:
    """Representa um item que compõe um kit."""
    produto: 'Produto' # Referência ao objeto Produto do componente
    quantidade: int # Quantidade deste componente necessária para montar UM kit


@dataclass
class Produto:
    """Produto no inventário."""
    id: int
    nome: str
    descricao: str
    categoria: str
    fornecedor: Fornecedor
    codigo_barras: str
    preco_compra: float
    preco_venda: float
    ponto_ressuprimento: int # Para produtos individuais, é o estoque mínimo
    tipoProduto: str = "individual"  # individual ou kit
    # Para produtos individuais, armazena a quantidade por nome de localização
    estoque_por_local: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    # Para kits, armazena a lista de seus componentes
    componentes: List[ComponenteKit] = field(default_factory=list)

    def recalcular_preco_compra(self):
        """Recalcula o preço de compra de um kit."""
        if self.tipoProduto == 'kit':
            self.preco_compra = sum(c.produto.preco_compra * c.quantidade for c in self.componentes)

    def get_estoque_total(self) -> int:
        """Calcula o estoque total."""
        if self.tipoProduto == 'individual':
            return sum(self.estoque_por_local.values())
        elif self.tipoProduto == 'kit':
            if not self.componentes:
                return 0
            try:
                return min(c.produto.get_estoque_total() // c.quantidade for c in self.componentes)
            except ZeroDivisionError:
                return 0

    def __str__(self):
        """representação em string para listas e seleções"""
        estoque_total = self.get_estoque_total()
        if self.tipoProduto == 'kit':
            return f"{self.id} - {self.nome} (Kit) (Estoque Montável: {estoque_total})"
        else:
            return f"{self.id} - {self.nome} (Estoque Total: {estoque_total})"


@dataclass
class ItemOrdemCompra:
    """nisso, nós vamos representar um item dentro de uma ordem de Compra"""
    # ou seja, um produto que está sendo comprado através do fornecedo
    produto: Produto
    quantidade: int
    preco_unitario: float

    @property
    def subtotal(self) -> float:
        """calculo do valor subtotal do item da ordem de compra"""
        return self.quantidade * self.preco_unitario


@dataclass
class OrdemCompra:
    """aqui, nós ja temoos a nossa tal ordem de compra kkkkk ai meu deus eu tô ficando louco"""
    id: int
    fornecedor: Fornecedor
    itens: List[ItemOrdemCompra]
    status: str # pendente, recebida, cancelada
    data_criacao: datetime = field(default_factory=datetime.now)

    @property
    def valor_total(self) -> float:
        return sum(item.subtotal for item in self.itens)

    def __str__(self):
        """Representação em string para listas e seleções."""
        # Usando ,.2f para formatar o número com separador de milhar e duas casas decimais
        valor_formatado = f"R$ {self.valor_total:,.2f}"
        data_formatada = self.data_criacao.strftime('%d/%m/%Y')
        return (f"OC #{self.id} | {data_formatada} | "
                f"Fornecedor: {self.fornecedor.empresa} | "
                f"{valor_formatado} | Status: {self.status}")


@dataclass
class ItemVenda:
    produto: Produto
    quantidade: int
    preco_venda_unitario: float

    @property
    def subtotal(self) -> float:
        return self.quantidade * self.preco_venda_unitario


@dataclass
class Venda:
    id: int
    cliente: str
    itens: List[ItemVenda]
    data: datetime = field(default_factory=datetime.now)

    @property
    def valor_total(self) -> float:
        return sum(item.subtotal for item in self.itens)

    def __str__(self):
        valor_formatado = f"R$ {self.valor_total:,.2f}"
        data_formatada = self.data.strftime('%d/%m/%Y')
        return f"Venda #{self.id} | Data: {data_formatada} | Cliente: {self.cliente} | Valor: {valor_formatado}"


@dataclass
class ItemDevolucao:
    """representa um produto específico dentro de um processo de devolução"""
    produto: Produto
    quantidade: int
    motivo_devolucao: str
    condicao_produto: str

    @property
    def subtotal(self) -> float:
        """vai caclcular o valor do item devolvido (que é baseado no preço de venda da compra original)"""
        return self.quantidade * self.produto.preco_venda


@dataclass
class Transacao:
    """representa o movimento financeiro associado a uma devolução oi troca"""
    id: int
    devolucao_id: int
    tipo: str # "reembolso", "credito", "pagamento_troca"
    valor: float
    data: datetime = field(default_factory=datetime.now)


@dataclass
class Devolucao:
    """representa o processo geral de devolução ou troca"""
    id: int
    venda_original: Venda
    cliente_nome: str
    itens: List[ItemDevolucao]
    status: str # solicitada, em analise, aprovada, concluida
    data: datetime = field(default_factory=datetime.now)
    observacoes: str = ""
    transacao: Optional[Transacao] = None
    nova_venda_troca: Optional[Venda] = None

    @property
    def valor_total_devolvido(self) -> float:
        return sum(item.subtotal for item in self.itens)

    def __str__(self):
        valor_formatado = f"R$ {self.valor_total_devolvido:,.2f}"
        data_formatada = self.data.strftime('%d/%m/%Y')
        return (f"Devolução #{self.id} | {data_formatada} | "
                f"Venda Orig.: #{self.venda_original.id} | Cliente: {self.cliente_nome} | "
                f"Status: {self.status}")


@dataclass
class HistoricoMovimento:
    produto: Produto
    tipo: str
    quantidade: int
    localizacao: Localizacao
    data: datetime = field(default_factory=datetime.now)


# =====================
# PADRÃO 1: SINGLETON
# =====================

class GeradorID:
    """
    Singleton para geração de IDs únicos.
    Garante que não haja conflitos de IDs entre entidades.
    """
    _instancia: Optional['GeradorID'] = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """Inicializa os contadores de IDs"""
        self._contadores = {
            'produto': 0,
            'fornecedor': 0,
            'localizacao': 0,
            'venda': 0,
            'ordem_compra': 0,
            'devolucao': 0,
            'transacao': 0
        }

    def proximo_id(self, tipo: str) -> int:
        """Retorna o próximo ID disponível para o tipo especificado"""
        if tipo not in self._contadores:
            raise ValueError(f"Tipo '{tipo}' não é válido. Tipos válidos: {list(self._contadores.keys())}")
        self._contadores[tipo] += 1
        return self._contadores[tipo]

    def definir_id_inicial(self, tipo: str, valor: int):
        """Define o valor inicial do contador (útil para importar dados existentes)"""
        if tipo not in self._contadores:
            raise ValueError(f"Tipo '{tipo}' não é válido")
        self._contadores[tipo] = valor

    def obter_contador_atual(self, tipo: str) -> int:
        """Retorna o valor atual do contador sem incrementar"""
        if tipo not in self._contadores:
            raise ValueError(f"Tipo '{tipo}' não é válido")
        return self._contadores[tipo]


# =====================
# PADRÃO 2: FACTORY METHOD
# =====================

class ProdutoFactory(ABC):
    """
    Classe abstrata para Factory Method de produtos.
    Define a interface para criação de produtos.
    """
    
    @abstractmethod
    def criar_produto(
        self,
        nome: str,
        descricao: str,
        categoria: str,
        fornecedor: Fornecedor,
        codigo_barras: str,
        preco_compra: float,
        preco_venda: float,
        ponto_ressuprimento: int,
        **kwargs
    ) -> Produto:
        """Método abstrato para criação de produtos"""
        pass

    def _validar_dados_comuns(self, preco_compra: float, preco_venda: float, ponto_ressuprimento: int):
        """Valida dados comuns a todos os produtos"""
        if preco_compra < 0:
            raise ValueError("Preço de compra não pode ser negativo")
        if preco_venda < 0:
            raise ValueError("Preço de venda não pode ser negativo")
        if preco_venda < preco_compra:
            raise ValueError(f"Preço de venda (R$ {preco_venda:.2f}) não pode ser menor "
                           f"que preço de compra (R$ {preco_compra:.2f})")
        if ponto_ressuprimento < 0:
            raise ValueError("Ponto de ressuprimento não pode ser negativo")


class ProdutoIndividualFactory(ProdutoFactory):
    """Factory para criação de produtos individuais"""

    def criar_produto(
        self,
        nome: str,
        descricao: str,
        categoria: str,
        fornecedor: Fornecedor,
        codigo_barras: str,
        preco_compra: float,
        preco_venda: float,
        ponto_ressuprimento: int,
        **kwargs
    ) -> Produto:
        """Cria um produto individual com validações"""
        
        # Validações
        self._validar_dados_comuns(preco_compra, preco_venda, ponto_ressuprimento)
        
        # Gera ID único
        gerador = GeradorID()
        novo_id = gerador.proximo_id('produto')
        
        return Produto(
            id=novo_id,
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            fornecedor=fornecedor,
            codigo_barras=codigo_barras,
            preco_compra=preco_compra,
            preco_venda=preco_venda,
            ponto_ressuprimento=ponto_ressuprimento,
            tipoProduto="individual"
        )


class ProdutoKitFactory(ProdutoFactory):
    """Factory para criação de kits de produtos"""

    def criar_produto(
        self,
        nome: str,
        descricao: str,
        categoria: str,
        fornecedor: Fornecedor,
        codigo_barras: str,
        preco_compra: float,  # Será recalculado
        preco_venda: float,
        ponto_ressuprimento: int,
        componentes: List[ComponenteKit] = None,
        **kwargs
    ) -> Produto:
        """Cria um kit de produtos com validações e cálculo automático de preço de compra"""
        
        # Validações específicas de kit
        if not componentes:
            raise ValueError("Kit deve ter pelo menos um componente")
        
        if preco_venda < 0:
            raise ValueError("Preço de venda não pode ser negativo")
        
        if ponto_ressuprimento < 0:
            raise ValueError("Ponto de ressuprimento não pode ser negativo")
        
        # Gera ID único
        gerador = GeradorID()
        novo_id = gerador.proximo_id('produto')
        
        # Cria o kit
        kit = Produto(
            id=novo_id,
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            fornecedor=fornecedor,
            codigo_barras=codigo_barras,
            preco_compra=0,  # Será calculado
            preco_venda=preco_venda,
            ponto_ressuprimento=ponto_ressuprimento,
            tipoProduto="kit",
            componentes=componentes
        )
        
        # Calcula automaticamente o preço de compra
        kit.recalcular_preco_compra()
        
        # Valida margem de lucro
        if kit.preco_venda < kit.preco_compra:
            raise ValueError(
                f"Preço de venda (R$ {kit.preco_venda:.2f}) é menor que "
                f"o custo dos componentes (R$ {kit.preco_compra:.2f}). "
                f"Margem: R$ {kit.preco_venda - kit.preco_compra:.2f}"
            )
        
        return kit


# =====================
# PADRÃO 3: BUILDER
# =====================

class VendaBuilder:
    """
    Builder para construção fluente e validada de Vendas.
    Permite criar vendas passo a passo com validações.
    """

    def __init__(self):
        self._id: Optional[int] = None
        self._cliente: str = ""
        self._itens: List[ItemVenda] = []
        self._data: Optional[datetime] = None

    def com_id(self, id_: int) -> 'VendaBuilder':
        """Define o ID da venda"""
        if id_ <= 0:
            raise ValueError("ID deve ser maior que zero")
        self._id = id_
        return self

    def com_id_automatico(self) -> 'VendaBuilder':
        """Gera automaticamente um ID único"""
        gerador = GeradorID()
        self._id = gerador.proximo_id('venda')
        return self

    def com_cliente(self, cliente: str) -> 'VendaBuilder':
        """Define o cliente da venda"""
        if not cliente or not cliente.strip():
            raise ValueError("Nome do cliente não pode ser vazio")
        self._cliente = cliente.strip()
        return self

    def com_data(self, data: datetime) -> 'VendaBuilder':
        """Define a data da venda"""
        self._data = data
        return self

    def adicionar_item(self, produto: Produto, quantidade: int, 
                       preco_unitario: Optional[float] = None) -> 'VendaBuilder':
        """
        Adiciona um item à venda.
        Se preco_unitario não for fornecido, usa o preço de venda do produto.
        """
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        # Verifica estoque disponível
        estoque_disponivel = produto.get_estoque_total()
        if estoque_disponivel < quantidade:
            raise ValueError(
                f"Estoque insuficiente para '{produto.nome}'. "
                f"Disponível: {estoque_disponivel}, Solicitado: {quantidade}"
            )
        
        preco = preco_unitario if preco_unitario is not None else produto.preco_venda
        
        if preco <= 0:
            raise ValueError("Preço unitário deve ser maior que zero")
        
        item = ItemVenda(produto, quantidade, preco)
        self._itens.append(item)
        return self

    def limpar_itens(self) -> 'VendaBuilder':
        """Remove todos os itens da venda"""
        self._itens = []
        return self

    def build(self) -> Venda:
        """Constrói a venda com todas as validações"""
        if self._id is None:
            raise ValueError("ID da venda não foi definido. Use com_id() ou com_id_automatico()")
        
        if not self._cliente:
            raise ValueError("Cliente não foi definido. Use com_cliente()")
        
        if not self._itens:
            raise ValueError("Venda deve ter pelo menos um item. Use adicionar_item()")
        
        venda = Venda(
            id=self._id,
            cliente=self._cliente,
            itens=self._itens.copy()
        )
        
        if self._data:
            venda.data = self._data
        
        return venda


class OrdemCompraBuilder:
    """
    Builder para construção fluente de Ordens de Compra.
    """

    def __init__(self, fornecedor: Fornecedor):
        if not fornecedor:
            raise ValueError("Fornecedor é obrigatório")
        self._fornecedor = fornecedor
        self._id: Optional[int] = None
        self._itens: List[ItemOrdemCompra] = []
        self._status = "pendente"
        self._data: Optional[datetime] = None

    def com_id_automatico(self) -> 'OrdemCompraBuilder':
        """Gera automaticamente um ID único"""
        gerador = GeradorID()
        self._id = gerador.proximo_id('ordem_compra')
        return self

    def adicionar_item(self, produto: Produto, quantidade: int,
                       preco_unitario: Optional[float] = None) -> 'OrdemCompraBuilder':
        """
        Adiciona um item à ordem de compra.
        Se preco_unitario não for fornecido, usa o preço de compra do produto.
        """
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        preco = preco_unitario if preco_unitario is not None else produto.preco_compra
        
        if preco < 0:
            raise ValueError("Preço unitário não pode ser negativo")
        
        item = ItemOrdemCompra(produto, quantidade, preco)
        self._itens.append(item)
        return self

    def definir_status(self, status: str) -> 'OrdemCompraBuilder':
        """Define o status da ordem"""
        status_validos = ["pendente", "recebida", "cancelada"]
        if status not in status_validos:
            raise ValueError(f"Status deve ser um de: {', '.join(status_validos)}")
        self._status = status
        return self

    def com_data(self, data: datetime) -> 'OrdemCompraBuilder':
        """Define a data da ordem"""
        self._data = data
        return self

    def build(self) -> OrdemCompra:
        """Constrói a ordem de compra com validações"""
        if self._id is None:
            raise ValueError("ID não foi definido. Use com_id_automatico()")
        
        if not self._itens:
            raise ValueError("Ordem de compra deve ter pelo menos um item")
        
        ordem = OrdemCompra(
            id=self._id,
            fornecedor=self._fornecedor,
            itens=self._itens.copy(),
            status=self._status
        )
        
        if self._data:
            ordem.data_criacao = self._data
        
        return ordem


# =====================
# PADRÃO 4: PROTOTYPE
# =====================

class ProdutoPrototype:
    """
    Mixin para adicionar capacidade de clonagem a produtos.
    """
    
    @staticmethod
    def clonar(produto: Produto) -> Produto:
        """Cria uma cópia profunda do produto"""
        return copy.deepcopy(produto)
    
    @staticmethod
    def clonar_como_variacao(
        produto: Produto,
        novo_nome: str,
        novo_codigo_barras: str,
        ajustes: Optional[Dict] = None
    ) -> Produto:
        """
        Clona o produto criando uma variação.
        Útil para criar produtos similares (ex: tamanhos, cores diferentes).
        
        Args:
            produto: Produto original a ser clonado
            novo_nome: Nome da variação
            novo_codigo_barras: Código de barras único da variação
            ajustes: Dict com atributos adicionais a ajustar (ex: {'preco_venda': 45.00})
        """
        gerador = GeradorID()
        clone = copy.deepcopy(produto)
        
        # Ajusta dados básicos
        clone.id = gerador.proximo_id('produto')
        clone.nome = novo_nome
        clone.codigo_barras = novo_codigo_barras
        
        # Limpa o estoque do clone (novo produto, estoque zerado)
        clone.estoque_por_local = defaultdict(int)
        
        # Aplica ajustes personalizados
        if ajustes:
            for attr, valor in ajustes.items():
                if hasattr(clone, attr):
                    setattr(clone, attr, valor)
                else:
                    raise ValueError(f"Atributo '{attr}' não existe em Produto")
        
        # Recalcula preço de compra se for kit
        if clone.tipoProduto == 'kit':
            clone.recalcular_preco_compra()
        
        return clone


class OrdemCompraPrototype:
    """
    Prototype para clonagem de Ordens de Compra.
    Útil para criar ordens recorrentes baseadas em ordens anteriores.
    """
    
    @staticmethod
    def clonar(ordem: OrdemCompra, **ajustes) -> OrdemCompra:
        """
        Clona uma ordem de compra com possíveis ajustes.
        
        Args:
            ordem: Ordem original
            **ajustes: Atributos a serem sobrescritos (ex: status='pendente')
        """
        gerador = GeradorID()
        clone = copy.deepcopy(ordem)
        
        # Gera novo ID
        clone.id = gerador.proximo_id('ordem_compra')
        
        # Reseta data para atual
        clone.data_criacao = datetime.now()
        
        # Aplica ajustes personalizados
        for key, value in ajustes.items():
            if hasattr(clone, key):
                setattr(clone, key, value)
            else:
                raise ValueError(f"Atributo '{key}' não existe em OrdemCompra")
        
        return clone
    
    @staticmethod
    def clonar_como_recorrente(ordem: OrdemCompra) -> OrdemCompra:
        """
        Cria uma nova ordem baseada em uma anterior (ordem recorrente).
        Sempre com status 'pendente' e data atual.
        """
        return OrdemCompraPrototype.clonar(ordem, status='pendente')


