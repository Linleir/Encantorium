import ply.lex as lex
import ply.yacc as yacc
import turtle
import math
import tkinter as tk

# Flag global de erro: setada por t_error ou p_error durante a compilação.
# Impede que o desenho ocorra quando o parser recuperou de um erro silenciosamente.
_houve_erro = False

# ==========================================
# 1. ANÁLISE LÉXICA (Scanner)
# ==========================================
tokens = ('ELEMENTO', 'ESTADO', 'EFEITO', 'INTENSIDADE', 'ET', 'INTRA', 'VEL', 'LPAREN', 'RPAREN')

t_ELEMENTO = r'aqua|fira|ventus|terra'
t_ESTADO = r'matera|gaser|fluidus'
t_EFEITO = r'danum|curam|parali|sonium|reparo'
t_INTENSIDADE = r'maxima|minima'
t_ET = r'et'
t_INTRA = r'intra' 
t_VEL = r'vel'      
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_error(t_lex):
    global _houve_erro
    _houve_erro = True
    lbl_status.config(text=f"Erro léxico: Símbolo '{t_lex.value[0]}' desconhecido.", fg="#ff4444")
    t_lex.lexer.skip(1)

lexer = lex.lex()

# ==========================================
# 2. ANÁLISE SINTÁTICA E PRECEDÊNCIA (Parser)
# ==========================================
precedence = (('left', 'VEL'), ('left', 'INTRA'), ('left', 'ET'), ('right', 'INTENSIDADE'))

def p_expressao_magica_binop(p):
    '''expressao_magica : expressao_magica VEL expressao_magica
                        | expressao_magica INTRA expressao_magica
                        | expressao_magica ET expressao_magica'''
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

def p_lista_efeitos_recursivo(p):
    'lista_efeitos : EFEITO lista_efeitos'
    p[0] = [p[1]] + p[2]

def p_lista_efeitos_base(p):
    'lista_efeitos : EFEITO'
    p[0] = [p[1]]

def p_error(p):
    global _houve_erro
    _houve_erro = True
    if p:
        lbl_status.config(text=f"Erro de Sintaxe próximo a '{p.value}'", fg="#ff4444")
    else:
        lbl_status.config(text="Erro de Sintaxe: Sentença incompleta!", fg="#ff4444")

# write_tables=False é OBRIGATÓRIO para arquivos .exe!
import sys
# Se for o .exe, ele carrega o mapa salvo (optimize=1). Se for o código normal, ele cria o mapa.
if getattr(sys, 'frozen', False):
    parser = yacc.yacc(optimize=1) 
else:
    parser = yacc.yacc()

# ==========================================
# 3. GERAÇÃO DE CÓDIGO (Renderizador Gráfico)
# ==========================================
cores_elementos = {'aqua': '#0077be', 'fira': '#cc0000', 'terra': '#5c4033', 'ventus': '#a9a9a9'}
cores_efeitos = {'danum': '#ff0000', 'curam': '#00ff00', 'parali': '#800080', 'sonium': '#00008b', 'reparo': '#ffd700'}

def desenhar_circulo_centralizado(x, y, raio):
    t.penup()
    t.goto(x, y - raio)
    t.setheading(0)
    t.pendown()
    t.circle(raio)

def desenhar_anel_magico(x, y, raio, cor):
    t.color(cor)
    t.pensize(2)
    desenhar_circulo_centralizado(x, y, raio)
    t.pensize(1)
    desenhar_circulo_centralizado(x, y, raio - 8)

def desenhar_forma_inscrita(x, y, raio, lados, cor, rotacao):
    t.color(cor)
    t.pensize(2)
    angulo_passo = 360 / lados
    vertices = []

    t.penup()
    for i in range(lados + 1):
        angulo = rotacao + (i * angulo_passo)
        vx = x + raio * math.cos(math.radians(angulo))
        vy = y + raio * math.sin(math.radians(angulo))
        t.goto(vx, vy)
        if i == 0: t.pendown()
        if i < lados: vertices.append((vx, vy))
    return vertices

def desenhar_orbes_efeitos(vertices, efeitos):
    n_efeitos, n_vertices = len(efeitos), len(vertices)
    if n_vertices == 0: return
    
    for i in range(n_efeitos):
        vx, vy = vertices[i % n_vertices] 
        cor = cores_efeitos[efeitos[i]]
        
        t.penup()
        t.goto(vx, vy - 10)
        t.pendown()
        t.color(cor)
        t.begin_fill()
        t.circle(10)
        t.end_fill()
        
        t.penup()
        t.goto(vx, vy - 5)
        t.color("white")
        t.pendown()
        t.circle(5)

# ==========================================
# ANÁLISE SEMÂNTICA (Verificação de Restrições)
# ==========================================
# Mapeamento de elemento -> número máximo de efeitos (= número de vértices da forma)
# REGRA SEMÂNTICA: um feitiço não pode ter mais efeitos do que vértices disponíveis,
# pois cada orbe de efeito ocupa exatamente um vértice da forma inscrita.
MAX_EFEITOS = {'fira': 3, 'terra': 4, 'ventus': 6, 'aqua': 8}

class ErroSemantico(Exception):
    """Exceção lançada quando uma regra semântica é violada."""
    pass

def verificar_semantica(node):
    """
    Percorre a AST e verifica todas as restrições semânticas.
    Lança ErroSemantico com mensagem descritiva em caso de violação.
    Ação semântica: verificação de limite de efeitos por elemento.
    """
    if node[0] == 'spell':
        _, elem, est, ef_list = node
        max_permitido = MAX_EFEITOS.get(elem, 4)
        n_efeitos = len(ef_list)
        # AÇÃO SEMÂNTICA: n_efeitos <= max_permitido
        if n_efeitos > max_permitido:
            forma = {'fira': 'triângulo', 'terra': 'quadrado',
                     'ventus': 'hexágono', 'aqua': 'octógono'}.get(elem, 'forma')
            raise ErroSemantico(
                f"Erro Semântico: '{elem}' ({forma}) suporta no máximo "
                f"{max_permitido} efeito(s), mas recebeu {n_efeitos}."
            )

    elif node[0] == 'binop':
        _, op, left, right = node
        verificar_semantica(left)
        verificar_semantica(right)

    elif node[0] == 'unary':
        _, mod, child = node
        verificar_semantica(child)
        
def contar_profundidade(node):
    # Conta quantos níveis de 'vel' existem abaixo deste nó
    if isinstance(node, tuple) and node[0] == 'binop' and node[1] == 'vel':
        return 1 + contar_profundidade(node[2])
    return 0

def gerar_codigo_visual(node, raio_base=130, x=0, y=0, rotacao_base=90, desenhar_base=True):
    if node[0] == 'spell':
        _, elem, est, ef_list = node
        cor = cores_elementos.get(elem, 'black')
        
        if desenhar_base: desenhar_anel_magico(x, y, raio_base, cor)
            
        lados = {'fira': 3, 'terra': 4, 'ventus': 6, 'aqua': 8}.get(elem, 4)
        if est == 'matera': desenhar_circulo_centralizado(x, y, raio_base * 0.5)
        elif est == 'fluidus': rotacao_base += 15
            
        vertices = desenhar_forma_inscrita(x, y, raio_base, lados, cor, rotacao_base)
        desenhar_orbes_efeitos(vertices, ef_list)

    elif node[0] == 'binop':
        _, op, left, right = node
        if op == 'et':
            gerar_codigo_visual(left, raio_base, x, y, rotacao_base, True)
            gerar_codigo_visual(right, raio_base, x, y, rotacao_base + 180, False)
        elif op == 'intra':
            gerar_codigo_visual(left, raio_base, x, y, rotacao_base, True)
            gerar_codigo_visual(right, raio_base * 0.45, x, y, rotacao_base - 45, True)
        elif op == 'vel':
            # 1. Validação Semântica: Impedir mais de 4 satélites
            # O número total de satélites é a profundidade total da árvore
            total_satelites = contar_profundidade(node)
            if total_satelites > 4:
                lbl_status.config(text=f"Erro Semântico: Limite de 4 satélites excedido!", fg="#ff8800")
                raise ValueError("Limite de satélites excedido")
            
            # 2. Desenha o núcleo (branch da esquerda)
            gerar_codigo_visual(left, raio_base, x, y, rotacao_base, True)
            
            # 3. Calcula o índice deste satélite específico
            # Contamos quantos 'vel' existem no ramo da esquerda
            indice = contar_profundidade(left)
            
            # 4. Distribuição em 4 Extremidades FIXAS
            # 0=Direita, 1=Cima, 2=Esquerda, 3=Baixo
            dist = (raio_base * 1.8) + 20
            posicoes = [(dist, 0), (0, dist), (-dist, 0), (0, -dist)]
            dx, dy = posicoes[indice % 4]
            
            gerar_codigo_visual(right, raio_base * 0.3, x + dx, y + dy, rotacao_base, True)

    elif node[0] == 'unary':
        _, mod, child = node
        novo_raio = raio_base * 1.5 if mod == 'maxima' else raio_base * 0.6
        t.pensize(4 if mod == 'maxima' else 1)
        gerar_codigo_visual(child, novo_raio, x, y, rotacao_base)

# ==========================================
# 4. INTERFACE GRÁFICA (Tkinter + Chat)
# ==========================================
def conjurar_magia(event=None):
    global _houve_erro
    sentenca = entry_chat.get()
    if not sentenca.strip(): return
    
    # Limpa a tela para a nova magia e reseta status
    t.clear()
    lbl_status.config(text="Analisando feitiço...", fg="#00ff00")
    root.update()
    
    # Reseta a flag antes de cada compilação
    _houve_erro = False

    # FASE 1 — Análise Léxica + Sintática: constrói a AST
    ast = parser.parse(sentenca)
    
    # Se t_error ou p_error foram chamados, a flag estará True —
    # o parser pode ter recuperado e retornado uma AST parcial, mas
    # a sentença tinha erros e não deve ser desenhada.
    if _houve_erro:
        entry_chat.delete(0, tk.END)
        return

    if ast:
        # FASE 2 — Análise Semântica: verifica restrições antes de renderizar
        try:
            verificar_semantica(ast)
        except ErroSemantico as e:
            lbl_status.config(text=str(e), fg="#ff4444")
            entry_chat.delete(0, tk.END)
            return

        # FASE 3 — Geração de Código: só chega aqui se passou nas fases anteriores
        t.speed(0)
        gerar_codigo_visual(ast)
        lbl_status.config(text="Matriz Mágica gerada com sucesso!", fg="#00ff00")
    
    # Limpa a caixa de texto
    entry_chat.delete(0, tk.END)

# Configuração da Janela Principal
root = tk.Tk()
root.title("Encantorium - Compilador Mágico")
root.geometry("850x750")
root.configure(bg="#111111")

# Canvas (A tela onde o Turtle vai desenhar)
canvas = tk.Canvas(root, width=800, height=600, bg="#111111", highlightthickness=0)
canvas.pack(pady=10)

# Vinculando o Turtle ao Canvas do Tkinter
screen = turtle.TurtleScreen(canvas)
screen.bgcolor("#111111")
t = turtle.RawTurtle(screen)
t.hideturtle()

# Área do "Chat" (Frame inferior)
frame_inferior = tk.Frame(root, bg="#111111")
frame_inferior.pack(fill=tk.X, padx=20, pady=10)

entry_chat = tk.Entry(frame_inferior, font=("Consolas", 14), bg="#222222", fg="#00ff00", insertbackground="white")
entry_chat.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry_chat.bind("<Return>", conjurar_magia) # Aperta Enter para conjurar

btn_conjurar = tk.Button(frame_inferior, text="Conjurar Magia", font=("Arial", 12, "bold"), bg="#444444", fg="white", command=conjurar_magia)
btn_conjurar.pack(side=tk.RIGHT)

# Rótulo de status (Para mostrar os erros do Compilador no GUI)
lbl_status = tk.Label(root, text="Digite a sua sentença acima e pressione Enter.", font=("Arial", 11), bg="#111111", fg="gray")
lbl_status.pack(pady=5)

root.mainloop()