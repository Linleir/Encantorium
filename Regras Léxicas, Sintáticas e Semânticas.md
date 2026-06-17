### 1. Análise Léxica (Lexer)
Implementada com `ply.lex`, identifica os seguintes tokens:
* **Elementos:** `aqua`, `fira`, `ventus`, `terra`
* **Estados:** `matera`, `gaser`, `fluidus`
* **Efeitos:** `danum`, `curam`, `parali`, `sonium`, `reparo`
* **Operadores:** `et` (Conjunção), `intra` (Inclusão), `vel` (Órbita)

### 2. Análise Sintática (Parser)
Implementada com `ply.yacc` (LALR).
* **Precedência:** Hierarquia estrita (`INTENSIDADE` > `ET` > `INTRA` > `VEL`) para garantir um comportamento determinístico, sem a necessidade de parênteses.
* **Gramática:** O Parser constrói uma AST que dita a estrutura geométrica final (onde os nós mais profundos formam o núcleo e os operadores `vel` geram órbitas).

### 3. Análise Semântica
O compilador realiza verificações críticas antes da renderização:
* **Limite de Satélites:** Restrição semântica que impede sistemas com mais de 4 satélites (`vel`), evitando colisões geométricas.
* **Validação de Efeitos:** Verifica se o número de efeitos é compatível com os vértices da forma geométrica do elemento base.

### 4. Geração de Código e Renderização
* O motor de renderização inspeciona os nós da AST para calcular coordenadas cartesianas dinâmicas.
* Implementação de otimização `screen.tracer(3)` para renderização rápida e fluida.
