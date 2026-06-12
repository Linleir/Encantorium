import ply.lex as lex
import ply.yacc as yacc

# ==========================================
# 1. ANÁLISE LÉXICA (Scanner)
# ==========================================
# Definição dos tokens baseados em expressões regulares

tokens = (
    'ELEMENTO',     # aqua, fira, ventus, terra
    'ESTADO',       # matera, gaser, fluidus
    'EFEITO',       # danum, curam, parali, sonium, reparo
    'INTENSIDADE',  # maxima, minima
    'ET',           # et (Conjunção E)
    'VEL',          # vel (Conjunção OU)
    'LPAREN',       # (
    'RPAREN'        # )
)

# Expressões Regulares para tokens simples
t_ELEMENTO = r'aqua|fira|ventus|terra'
t_ESTADO = r'matera|gaser|fluidus'
t_EFEITO = r'danum|curam|parali|sonium|reparo'
t_INTENSIDADE = r'maxima|minima'
t_ET = r'et'
t_VEL = r'vel'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' encontrado.")
    t.lexer.skip(1)

lexer = lex.lex()

# ==========================================
# 2. ANÁLISE SINTÁTICA E SEMÂNTICA (Parser)
# ==========================================

# Regras de Precedência para eliminação de ambiguidade
precedence = (
    ('left', 'VEL'),
    ('left', 'ET'),
    ('right', 'INTENSIDADE'), # Unário possui precedência maior
)

# Gramática Livre de Contexto (GLC) e Ações Semânticas

def p_expressao_magica_binop(p):
    '''expressao_magica : expressao_magica VEL expressao_magica
                        | expressao_magica ET expressao_magica'''
    # Ação Semântica: Criação de nó na Árvore Sintática (AST)
    p[0] = ('binop', p[2], p[1], p[3]) 

def p_expressao_magica_unary(p):
    'expressao_magica : INTENSIDADE expressao_magica'
    p[0] = ('unary', p[1], p[2])

def p_expressao_magica_group(p):
    'expressao_magica : LPAREN expressao_magica RPAREN'
    p[0] = p[2]

def p_expressao_magica_encantamento(p):
    'expressao_magica : encantamento'
    p[0] = p[1]

def p_encantamento_estado(p):
    'encantamento : ELEMENTO ESTADO lista_efeitos'
    p[0] = ('spell', p[1], p[2], p[3])

def p_encantamento_simples(p):
    'encantamento : ELEMENTO lista_efeitos'
    p[0] = ('spell', p[1], None, p[2])

# AUTOINCORPORAÇÃO: Permite encadeamento infinito de efeitos
def p_lista_efeitos_recursivo(p):
    'lista_efeitos : EFEITO lista_efeitos'
    p[0] = [p[1]] + p[2]

def p_lista_efeitos_base(p):
    'lista_efeitos : EFEITO'
    p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}'")
    else:
        print("Erro de sintaxe: fim de entrada inesperado.")

parser = yacc.yacc()

# ==========================================
# 3. GERAÇÃO DE CÓDIGO (Tradução da AST)
# ==========================================

def compilar_traducao(node):
    forma_elemento = {'aqua': 'Círculo', 'fira': 'Triângulo', 'ventus': 'Linha', 'terra': 'Quadrado'}
    forma_estado = {'matera': 'Retângulo', 'gaser': 'Losango', 'fluidus': 'Oval'}
    forma_efeito = {'danum': 'Estrela', 'curam': 'Coração', 'parali': 'Cruz', 'sonium': 'Lua', 'reparo': 'Seta'}

    if node[0] == 'spell':
        _, elem, est, ef_list = node
        
        # Validações Semânticas de Tipos/Regras
        if elem == 'fira' and est is not None:
            return "[ERRO: 'fira' não suporta estado da matéria]"
        if elem != 'fira' and est is None:
            return f"[ERRO: '{elem}' exige um estado da matéria]"
        
        trans = forma_elemento[elem]
        if est: trans += f" {forma_estado[est]}"
        for ef in ef_list: trans += f" {forma_efeito[ef]}"
        return f"[{trans}]"

    elif node[0] == 'binop':
        op = " + " if node[1] == 'et' else " OU "
        return f"({compilar_traducao(node[2])}{op}{compilar_traducao(node[3])})"

    elif node[0] == 'unary':
        mod = "AMPLIFICADO" if node[1] == 'maxima' else "REDUZIDO"
        return f"{mod}({compilar_traducao(node[2])})"

# ==========================================
# LOOP PRINCIPAL
# ==========================================
print("=== Compilador Encantorium 2.0 ===")
print("Dica de sentença válida: maxima aqua matera curam curam et fira danum")
while True:
    try:
        s = input('\nInsira o encantamento > ')
    except EOFError:
        break
    if not s or s.lower() == 'sair':
        break
    
    ast = parser.parse(s)
    if ast:
        resultado = compilar_traducao(ast)
        print(f"-> Tradução Compilada: {resultado}")
