import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens que serão reconhecidos pelo lexer
tokens = (
    'ELEMENTO',  # Elementos básicos: aqua, fira, ventus, terra
    'ESTADO',    # Estados da matéria: matera, gaser, fluidus
    'EFEITO',    # Efeitos adicionais: danum, curam, parali, sonium, reparo
)

# Regras para o reconhecimento dos tokens
t_ELEMENTO = r'aqua|fira|ventus|terra'   # Expressões regulares para elementos
t_ESTADO = r'matera|gaser|fluidus'       # Expressões regulares para estados da matéria
t_EFEITO = r'danum|curam|parali|sonium|reparo'  # Expressões regulares para efeitos

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Função para tratar caracteres ilegais
def t_error(t):
    t.lexer.skip(len(t.value))  # Ignorar todo o token inválido
    raise ValueError(f"Caractere ilegal '{t.value[0]}'")

# Construir o lexer
lexer = lex.lex()

# Gramática do parser

# Regra principal para um encantamento
def p_encantamento(p):
    '''
    encantamento : ELEMENTO estados efeitos  
                 | ELEMENTO efeitos          
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])  # Encantamento com estado
    else:
        p[0] = (p[1], None, p[2])  # Encantamento sem estado (fira)

# Regra para estados da matéria
def p_estados(p):
    '''
    estados : ESTADO  
    '''
    p[0] = p[1]

# Regra para efeitos
def p_efeitos(p):
    '''
    efeitos : EFEITO                
            | EFEITO EFEITO         
            | EFEITO EFEITO EFEITO  
    '''
    p[0] = p[1:]

# Função para tratar erros de sintaxe
def p_error(p):
    raise SyntaxError("Erro de sintaxe!")

# Construir o parser
parser = yacc.yacc()

# Função para compilar e verificar o encantamento
def compile_spell(spell):
    lexer.input(spell)
    
    tokens_invalidos = []
    valid_tokens = []
    
    # Verificar tokens inválidos e coletar tokens válidos
    while True:
        try:
            tok = lexer.token()
            if not tok:
                break
            if tok.type == 'ERROR':
                tokens_invalidos.append(tok.value)
            else:
                valid_tokens.append(tok.value)
        except ValueError as e:
            return f"Erro: {str(e)}"
    
    if tokens_invalidos:
        return f"Erro: Caractere(s) ilegal(is) encontrado(s): {', '.join(tokens_invalidos)}."

    # Recriar a string de entrada apenas com os tokens válidos para o parser
    valid_spell = ' '.join(valid_tokens)
    
    try:
        result = parser.parse(valid_spell)
    except (SyntaxError, ValueError) as e:
        return f"Erro: {str(e)}"
    
    if result:
        elemento, estado, efeitos = result
        
        # Verificação se fira tem estado da matéria
        if elemento == 'fira' and estado is not None:
            return "Erro: Encantamentos de fogo não devem especificar o estado da matéria."
        
        # Verificação se outros elementos têm estado da matéria
        if elemento != 'fira' and estado is None:
            return "Erro: Encantamentos de água, vento e terra precisam especificar o estado da matéria."
        
        # Verificação de efeitos repetidos ou únicos
        if len(efeitos) != len(set(efeitos)) and len(set(efeitos)) != 1:
            return "Erro: Todos os efeitos devem ser iguais ou todos diferentes."

        # Geração da tradução direta se o encantamento for válido
        return generate_translation(elemento, estado, efeitos)
    else:
        return "Erro: Encantamento inválido."

# Função para gerar a tradução direta do encantamento
def generate_translation(elemento, estado, efeitos):
    forma_elemento = {
        'aqua': 'Círculo',
        'fira': 'Triângulo',
        'ventus': 'Linha',
        'terra': 'Quadrado'
    }
    
    forma_estado = {
        'matera': 'Retângulo',
        'gaser': 'Losango',
        'fluidus': 'Oval'
    }
    
    forma_efeito = {
        'danum': 'Estrela',
        'curam': 'Coração',
        'parali': 'Cruz',
        'sonium': 'Lua',
        'reparo': 'Seta'
    }

    # Construção da tradução direta
    translation = f"{forma_elemento[elemento]}"
    if estado:
        translation += f" {forma_estado[estado]}"
    for efeito in efeitos:
        translation += f" {forma_efeito[efeito]}"
    
    return translation

# Loop para permitir que o usuário insira encantamentos
while True:
    spell = input("Insira o encantamento mágico (ou 'sair' para finalizar): ")
    if spell.lower() == 'sair':
        break
    print(compile_spell(spell))