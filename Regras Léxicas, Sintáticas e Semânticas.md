# Encantorium: Compilador de Sistemas Mágicos Dinâmicos

**Disciplina:** Compiladores (2026_1)

---

## 1. Visão Geral
O *Encantorium* é uma DSL (Domain Specific Language) que traduz sentenças mágicas em círculos mágicos complexos. O objetivo deste projeto foi aplicar na prática os conceitos fundamentais de compiladores — **análise léxica, sintática e semântica** — transformando texto estruturado em representações gráficas (renderização via `turtle`).



## 2. Arquitetura do Compilador

### 2.1 Análise Léxica
O compilador utiliza expressões regulares para identificar os tokens:

* **Elementos:** `aqua`, `fira`, `ventus`, `terra`
* **Estados:** `matera`, `gaser`, `fluidus`
* **Efeitos:** `danum`, `curam`, `parali`, `sonium`, `reparo`
* **Intensidade:** `maxima`, `minima`
* **Operadores:** `et` (Conjunção), `intra` (Inclusão), `vel` (Órbita)

---

## 3. Regras Sintáticas

* **Precedência:** Definida no objeto `precedence` para evitar ambiguidades. A ordem de força, do mais forte para o mais fraco, é:
    * `INTENSIDADE` (Direita).
    * `ET` (Esquerda).
    * `INTRA` (Esquerda).
    * `VEL` (Esquerda).
* **Estrutura de Operações:** O compilador aceita operações binárias (`binop`), operações unárias (`INTENSIDADE`), agrupamentos e encantamentos base.
* **Produções de Encantamento:** Um encantamento deve conter um `ELEMENTO`, opcionalmente um `ESTADO`, e uma `lista_efeitos` (que deve ter pelo menos um `EFEITO`).

---

## 4. Regras Semânticas
As regras semânticas validam o "significado" e a consistência da sentença, verificando restrições que a sintaxe sozinha não consegue detectar.

* **Limite de Efeitos por Elemento:** O número de efeitos aplicados não pode exceder a quantidade de vértices da forma geométrica do elemento:
    * `fira` (triângulo): máx 3 efeitos.
    * `terra` (quadrado): máx 4 efeitos.
    * `ventus` (hexágono): máx 6 efeitos.
    * `aqua` (octógono): máx 8 efeitos.
* **Limite de Satélites:** O compilador valida recursivamente a estrutura de operadores `vel`. Se a contagem total de satélites (níveis de recursividade do operador `vel`) exceder 4, uma exceção é lançada e a compilação é interrompida.

---

## 5. Guia de Instalação e Execução

1. **Dependências:**
   ```bash
   pip install ply
