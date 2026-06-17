# Compilador Encantorium

Este projeto foi desenvolvido para o trabalho final da disciplina de **Compiladores**.

O objetivo é demonstrar, de forma prática, conceitos de:

- Análise léxica
- Análise sintática
- Análise semântica

Para isso, foi criado um pequeno compilador baseado em **PLY**, utilizando a linguagem **Python**.

## Sobre o compilador

O compilador interpreta sentenças mágicas fictícias formadas por:

- Elementos
- Estados da matéria
- Efeitos

A partir de uma entrada válida, como:

```txt
aqua matera curam reparo
```
## Tokens aceitos

O compilador reconhece três tipos de tokens:

- **ELEMENTO:** `aqua`, `fira`, `ventus`, `terra`
- **ESTADO:** `matera`, `gaser`, `fluidus`
- **EFEITO:** `danum`, `curam`, `parali`, `sonium`, `reparo`

Cada token é traduzido para um símbolo textual correspondente, como `Círculo`, `Triângulo`, `Retângulo`, `Estrela`, entre outros.

O programa reconhece os tokens, valida a estrutura gramatical da sentença, aplica regras semânticas e transforma em um símbolo geométrico diferente.

## Regras da linguagem

A linguagem criada possui regras próprias, como:

- Alguns elementos exigem um estado da matéria.
- O elemento `fira` é uma exceção e não utiliza estado da matéria.
- O encantamento deve possuir de um a três efeitos.
- Os efeitos devem respeitar as regras semânticas definidas no compilador.

## Materiais incluídos

O projeto também inclui:

- Tabela de produções e ações semânticas
- Árvore de derivação
- Árvore de derivação anotada
- Exemplos de execução do compilador
aqua matera curam reparo
