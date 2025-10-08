# Projeto-Refatorado

$\triangleright$ **Análise do projeto da matéria de projeto de software do repositório de Luiz Miguel de Belo Bonfin (luizwhirl)**

## 📆 Objetivo da primeira semana :
$\diamond$ Efetuar a análise do código escrito verificando as aplicações exigidas pelo projeto 

### 📌 Funcionalidades implementadas

- 🟢 **Product Catalog Management;**
- 🟢 **Stock Level Tracking;**
- 🟢 **Reorder Alerts;**
- 🟢 **Supplier Management;**
- 🟢 **Purchase Order Creation;**
- 🟢 **Barcode Scanning;**
- 🟢 **Inventory Valuation;**
- 🟢 **Sales and Purchase History;**
- 🟢 **Multi-Location Management;**
- 🟢 **Inventory Reports.**

#### 📑 Analise : 

  Durante a analise do projeto orientado a objetos, do aluno Luiz Miguel de Belo Bonfin, foi conferido através da analise sistematica do programa apresentado que todas as implementações requeridas no projeto foram implementadas corretamente, sem a necessidade de incluir funcionalidades ausentes. 

## 📆 Objetivo da segunda e terceira semana :

$\diamond$ Adição de padrões de projetos no código 

# ⚙️ Padrões de Projeto Utilizados
### 🧩 1. Observer (Comportamental)

Aplicação no código:

A classe Produto mantém uma lista de observadores (_observadores_estoque).
Quando o estoque chega a zero, todos os observadores são notificados via o método _notificar_estoque_zerado().
Observador: AlertaEstoqueBaixo, que imprime alertas quando o estoque acaba.

### 🔗 2. Chain of Responsibility (Comportamental)

Implementada para aprovar devoluções com base em seu valor.
Classes: atendente, Gerente, Diretor — cada uma tem um limite de aprovação.
O processo flui até que alguém na cadeia aprove a devolução.

### 🧱 3. Singleton (Criacional)

Aplicação no código:

Classe GeradorID gera IDs únicos para todos os tipos de entidades (produto, venda, ordem de compra, etc).

### 🏭 4. Factory Method (Criacional)

Aplicação no código:

ProdutoFactory é uma classe abstrata que define o método criar_produto().
Subclasses:
ProdutoIndividualFactory: cria produtos unitários;
ProdutoKitFactory: cria kits compostos por outros produtos.

### 🧰 5. Builder (Criacional)

Aplicação no código:

VendaBuilder: constrói objetos Venda de forma fluente e validada.
OrdemCompraBuilder: constrói objetos OrdemCompra com segurança e legibilidade.

### 🧬 6. Prototype (Criacional)

Aplicação no código:

ProdutoPrototype: clona produtos, inclusive criando variações (ex: “Camisa Azul” → “Camisa Vermelha”).
OrdemCompraPrototype: clona ordens de compra para gerar ordens recorrentes.



