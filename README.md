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

### 🧠 3. Strategy (Comportamental)

Aplicação no código:

Implementa diferentes estratégias de cálculo de descontos em vendas.

**Estratégias:**

* Sem desconto
* Desconto por valor (10% para compras acima de R$1000)
* Descont por quantidade (5% para mais de 9 itens).

### 🧱 4. Singleton (Criacional)

Aplicação no código:

Classe GeradorID gera IDs únicos para todos os tipos de entidades (produto, venda, ordem de compra, etc).

### 🏭 5. Factory Method (Criacional)

Aplicação no código:

ProdutoFactory é uma classe abstrata que define o método criar_produto().
Subclasses:
ProdutoIndividualFactory: cria produtos unitários;
ProdutoKitFactory: cria kits compostos por outros produtos.

### 🧰 6. Builder (Criacional)

Aplicação no código:

VendaBuilder: constrói objetos Venda de forma fluente e validada.
OrdemCompraBuilder: constrói objetos OrdemCompra com segurança e legibilidade.

### 🧬 7. Prototype (Criacional)

Aplicação no código:

ProdutoPrototype: clona produtos, inclusive criando variações (ex: “Camisa Azul” → “Camisa Vermelha”).
OrdemCompraPrototype: clona ordens de compra para gerar ordens recorrentes.

### 🎨 8. Decorator (Estrutural)

Aplicação no código:

Adiciona funcionalidades extras a relatórios sem modificar suas classes originais.

### 🔌 9. Adapter (Estrutural)

Aplicação no código:
Permite adaptar diferentes formatos de relatório (ex: JSON, CSV, TXT) para uma interface comum (FormatoRelatorio).
A classe AdaptadorRelatorio converte a chamada genérica em comandos específicos.

### 🌉 10. Bridge (Estrutural)

Aplicação no código:

Separa a abstração da implementação nos relatórios.
A classe Relatorio atua como controle, enquanto o formato (FormatoRelatorio) é a implementação.

