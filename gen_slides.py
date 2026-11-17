# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

NAVY   = RGBColor(0x1F, 0x3B, 0x63)
NAVY2  = RGBColor(0x2E, 0x4A, 0x7A)
BLUE   = RGBColor(0x2B, 0x6C, 0xB0)
LIGHT  = RGBColor(0xEE, 0xF2, 0xF8)
LIGHT2 = RGBColor(0xF7, 0xF9, 0xFC)
GRAY   = RGBColor(0x55, 0x5F, 0x6E)
DARK   = RGBColor(0x1E, 0x1E, 0x24)
GREEN  = RGBColor(0x1E, 0x7A, 0x46)
GREENL = RGBColor(0xE3, 0xF4, 0xEA)
RED    = RGBColor(0xB0, 0x30, 0x30)
REDL   = RGBColor(0xF9, 0xE8, 0xE8)
AMBER  = RGBColor(0xB0, 0x7A, 0x1E)
AMBERL = RGBColor(0xFB, 0xF1, 0xDC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def _txt(shape):
    tf = shape.text_frame
    tf.word_wrap = True
    return tf


def rect(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, line_w=Pt(1)):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = line_w
    sp.shadow.inherit = False
    return sp


def text(s, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True):
    """paras: lista de dicts {t, size, bold, color, font, italic, after, bullet, align}"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    first = True
    for p in paras:
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        t = p.get('t', '')
        if p.get('bullet'):
            t = '•  ' + t
        r = para.add_run()
        r.text = t
        r.font.size = Pt(p.get('size', 18))
        r.font.bold = p.get('bold', False)
        r.font.italic = p.get('italic', False)
        r.font.name = p.get('font', 'Arial')
        if p.get('color'):
            r.font.color.rgb = p['color']
        para.space_after = Pt(p.get('after', 6))
        para.space_before = Pt(p.get('before', 0))
        para.alignment = p.get('align', align)
    return tb


def header(s, title, kicker=None):
    rect(s, 0, 0, 13.333, 1.05, fill=NAVY)
    rect(s, 0, 1.05, 13.333, 0.06, fill=BLUE)
    text(s, 0.7, 0.12, 11.5, 0.9, [
        {'t': title, 'size': 30, 'bold': True, 'color': WHITE},
    ], anchor=MSO_ANCHOR.MIDDLE)
    if kicker:
        text(s, 10.6, 0.12, 2.3, 0.9, [
            {'t': kicker, 'size': 13, 'color': RGBColor(0xAA, 0xC4, 0xE8), 'align': PP_ALIGN.RIGHT},
        ], anchor=MSO_ANCHOR.MIDDLE)


def card(s, x, y, w, h, fill=LIGHT2, line=RGBColor(0xD5, 0xDE, 0xEA), shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    return rect(s, x, y, w, h, fill=fill, line=line, shape=shape, line_w=Pt(1.25))


def chip(s, x, y, w, h, label, fill, tcolor=WHITE, size=15):
    c = rect(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = _txt(c)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.15)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = tcolor
    r.font.name = 'Arial'
    return c


def pnum(n):
    return {'t': str(n), 'size': 13, 'color': RGBColor(0x9A, 0xA7, 0xB8), 'align': PP_ALIGN.RIGHT}


def footer_num(s, n):
    text(s, 12.2, 7.1, 0.9, 0.35, [pnum(n)])


# ============================ SLIDES ============================

# ---- 1. Capa ----
s = slide()
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
rect(s, 0, 5.9, 13.333, 0.07, fill=BLUE)
rect(s, 0.9, 1.5, 0.14, 3.6, fill=BLUE, shape=MSO_SHAPE.RECTANGLE)
text(s, 1.4, 1.7, 10.5, 3.2, [
    {'t': 'Cache de Conteúdo', 'size': 54, 'bold': True, 'color': WHITE, 'after': 4},
    {'t': 'com HashMap', 'size': 54, 'bold': True, 'color': RGBColor(0x7F, 0xB3, 0xE8), 'after': 26},
    {'t': 'Spring Boot 4.x · JDK 21 · Spring Data JPA · H2', 'size': 22, 'color': RGBColor(0xAA, 0xC4, 0xE8)},
])
text(s, 1.4, 6.15, 10.5, 1.2, [
    {'t': 'João Pedro Santos Pinheiro — RA 04251097', 'size': 24, 'bold': True, 'color': WHITE, 'after': 4},
    {'t': 'Téc. Avançadas de Back-end · SPTECH · AVL2 · 2026', 'size': 17, 'color': RGBColor(0x99, 0xB3, 0xD4)},
])

# ---- 2. O problema ----
s = slide()
header(s, 'O problema', 'por que cache?')
# dois cards de "dor"
card(s, 0.7, 1.5, 5.9, 2.1)
text(s, 1.0, 1.7, 5.3, 1.8, [
    {'t': 'Fonte LENTA', 'size': 24, 'bold': True, 'color': RED, 'after': 6},
    {'t': 'Banco sobrecarregado, serviço externo ou processamento pesado', 'size': 17, 'color': GRAY},
])
card(s, 6.7, 1.5, 5.9, 2.1)
text(s, 7.0, 1.7, 5.3, 1.8, [
    {'t': 'MESMAS consultas', 'size': 24, 'bold': True, 'color': AMBER, 'after': 6},
    {'t': 'Muitos usuários pedem os mesmos conteúdos várias vezes', 'size': 17, 'color': GRAY},
])
# seta + solução
text(s, 0.7, 3.9, 12, 0.5, [
    {'t': 'Buscar tudo de novo a cada requisição = tempo e recursos desperdiçados', 'size': 19, 'italic': True, 'color': GRAY, 'align': PP_ALIGN.CENTER},
])
big = card(s, 1.7, 4.5, 10, 1.9, fill=NAVY, line=NAVY)
text(s, 2.0, 4.75, 9.4, 1.5, [
    {'t': 'SOLUÇÃO → CACHE', 'size': 26, 'bold': True, 'color': WHITE, 'align': PP_ALIGN.CENTER, 'after': 6},
    {'t': 'Guardar temporariamente o resultado da busca e reutilizar nas próximas requisições', 'size': 18, 'color': RGBColor(0xCC, 0xDD, 0xEE), 'align': PP_ALIGN.CENTER},
])
footer_num(s, 2)

# ---- 3. O que é cache ----
s = slide()
header(s, 'O que é cache?')
card(s, 0.7, 1.5, 12, 1.7, fill=LIGHT)
text(s, 1.1, 1.75, 11.2, 1.3, [
    {'t': 'Espaço que guarda TEMPORARIAMENTE informações já consultadas.', 'size': 24, 'bold': True, 'color': NAVY, 'after': 6},
    {'t': 'Na próxima consulta igual, o sistema usa a cópia guardada — sem ir à fonte de novo.', 'size': 19, 'color': GRAY},
])
examples = [
    ('Navegador', 'guarda imagens e arquivos de sites'),
    ('CDN', 'cópias de arquivos perto do usuário'),
    ('Banco de dados', 'cache de queries frequentes'),
    ('Aplicação', 'cache em memória — nosso caso'),
]
x = 0.7
for nome, desc in examples:
    card(s, x, 3.7, 2.85, 2.9)
    chip(s, x + 0.35, 4.0, 2.15, 0.55, nome.upper(), NAVY, size=14)
    text(s, x + 0.2, 4.8, 2.45, 1.6, [
        {'t': desc, 'size': 15, 'color': GRAY, 'align': PP_ALIGN.CENTER, 'after': 4},
    ])
    x += 3.05
text(s, 0.7, 6.85, 12, 0.5, [
    {'t': 'Objetivo: diminuir tempo de resposta e evitar consultas repetidas', 'size': 18, 'bold': True, 'color': NAVY, 'align': PP_ALIGN.CENTER},
])
footer_num(s, 3)

# ---- 4. HIT vs MISS ----
s = slide()
header(s, 'HIT, MISS e hit ratio')
# HIT card
card(s, 0.7, 1.6, 5.8, 3.6, fill=GREENL, line=GREEN)
chip(s, 1.05, 1.9, 2.2, 0.6, 'HIT', GREEN, size=20)
text(s, 1.05, 2.7, 5.1, 2.3, [
    {'t': 'Conteúdo ESTÁ no cache e dentro do TTL', 'size': 18, 'bold': True, 'after': 8},
    {'t': 'Resposta vem direto da memória → rápido', 'size': 17, 'color': GRAY},
])
# MISS card
card(s, 6.8, 1.6, 5.8, 3.6, fill=REDL, line=RED)
chip(s, 7.15, 1.9, 2.2, 0.6, 'MISS', RED, size=20)
text(s, 7.15, 2.7, 5.1, 2.3, [
    {'t': 'Não está no cache OU TTL venceu', 'size': 18, 'bold': True, 'after': 8},
    {'t': 'Busca na fonte (lenta) e guarda no cache', 'size': 17, 'color': GRAY},
])
# hit ratio
card(s, 0.7, 5.5, 11.9, 1.4, fill=NAVY, line=NAVY)
text(s, 1.1, 5.7, 11.1, 1.1, [
    {'t': 'HIT RATIO = hits / (hits + misses)', 'size': 22, 'bold': True, 'color': WHITE, 'after': 2},
    {'t': 'Percentual de consultas atendidas pelo cache  ·  ex.: 8 hits + 2 misses = 80%', 'size': 16, 'color': RGBColor(0xCC, 0xDD, 0xEE)},
])
footer_num(s, 4)

# ---- 5. TTL ----
s = slide()
header(s, 'TTL — Time To Live')
card(s, 0.7, 1.6, 12, 1.5, fill=LIGHT)
text(s, 1.1, 1.8, 11.2, 1.1, [
    {'t': 'Tempo de vida de cada item no cache (configurado: 60 s).', 'size': 24, 'bold': True, 'color': NAVY, 'after': 4},
    {'t': 'Passou o TTL → item vencido → próxima consulta é MISS.', 'size': 18, 'color': GRAY},
])
# timeline visual
rect(s, 1.2, 3.6, 10.9, 0.9, fill=RGBColor(0xD9, 0xE2, 0xEE), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, 1.2, 3.6, 7.0, 0.9, fill=GREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(s, 1.45, 3.78, 6.5, 0.6, [
    {'t': 'válido no cache', 'size': 15, 'bold': True, 'color': WHITE, 'align': PP_ALIGN.CENTER},
])
text(s, 8.3, 3.78, 3.5, 0.6, [
    {'t': 'expirado → MISS', 'size': 15, 'bold': True, 'color': RED, 'align': PP_ALIGN.CENTER},
])
text(s, 1.2, 4.6, 1.2, 0.4, [{'t': 't=0', 'size': 13, 'color': GRAY}])
text(s, 8.0, 4.6, 1.6, 0.4, [{'t': 't=60s', 'size': 13, 'color': GRAY, 'align': PP_ALIGN.CENTER}])
text(s, 10.4, 4.6, 1.6, 0.4, [{'t': 'agora', 'size': 13, 'color': GRAY, 'align': PP_ALIGN.RIGHT}])
card(s, 0.7, 5.4, 12, 1.5, fill=AMBERL, line=AMBER)
text(s, 1.1, 5.6, 11.2, 1.2, [
    {'t': 'Por que o dado fica "velho" (stale)?', 'size': 20, 'bold': True, 'color': AMBER, 'after': 4},
    {'t': 'Alguém alterou o conteúdo no banco, mas a cópia antiga continua no cache. O TTL limita isso — a invalidação resolve de vez.', 'size': 16, 'color': GRAY},
])
footer_num(s, 5)

# ---- 6. Políticas ----
s = slide()
header(s, 'Políticas de remoção (eviction)')
text(s, 0.7, 1.3, 12, 0.5, [
    {'t': 'Cache cheio → qual item sai para entrar o novo?', 'size': 19, 'color': GRAY},
])
rows = [
    ('FIFO', 'First In, First Out', 'Sai o que ENTROU primeiro', 'ordem de chegada importa', GRAY),
    ('LRU', 'Least Recently Used', 'Sai o usado há MAIS TEMPO', 'padrão geral — reuso recente', NAVY),
    ('LFU', 'Least Frequently Used', 'Sai o com MENOS acessos', 'poucos itens "quentes"', GRAY),
]
x = 0.7
for nome, sigla_full, como, quando, cor in rows:
    highlight = (nome == 'LRU')
    card(s, x, 2.0, 3.95, 3.3, fill=(NAVY if highlight else LIGHT2), line=(NAVY if highlight else RGBColor(0xD5, 0xDE, 0xEA)))
    chip(s, x + 0.4, 2.3, 1.5, 0.6, nome, (WHITE if highlight else cor), size=20,
         tcolor=(WHITE if highlight else cor))
    text(s, x + 0.3, 2.95, 3.35, 0.4, [
        {'t': sigla_full, 'size': 13, 'italic': True, 'color': (RGBColor(0xAA, 0xC4, 0xE8) if highlight else GRAY), 'align': PP_ALIGN.CENTER},
    ])
    text(s, x + 0.3, 3.35, 3.35, 1.9, [
        {'t': como, 'size': 16, 'bold': True, 'color': (WHITE if highlight else RGBColor(0x22, 0x22, 0x22)), 'after': 8, 'align': PP_ALIGN.CENTER},
        {'t': quando, 'size': 14, 'color': (RGBColor(0xCC, 0xDD, 0xEE) if highlight else GRAY), 'align': PP_ALIGN.CENTER},
    ])
    x += 4.15
card(s, 1.9, 5.6, 9.5, 1.2, fill=LIGHT)
text(s, 2.2, 5.8, 8.9, 0.9, [
    {'t': 'NOSSO PROJETO → LRU', 'size': 20, 'bold': True, 'color': NAVY, 'align': PP_ALIGN.CENTER, 'after': 4},
    {'t': 'Least Recently Used · limite de 5 itens · ao encher, remove o item acessado há mais tempo', 'size': 16, 'color': GRAY, 'align': PP_ALIGN.CENTER},
])
footer_num(s, 6)

# ---- 7. Invalidação ----
s = slide()
header(s, 'Invalidação de cache')
# fluxo
steps = [('PUT /conteudos/{id}', 'atualiza no banco'), ('DELETE /conteudos/{id}', 'remove do banco'), ('cache.remover(id)', 'cópia antiga sai')]
x = 0.9
for i, (a, b) in enumerate(steps):
    chip(s, x, 1.9, 3.6, 0.9, a, NAVY if i < 2 else RED, size=15)
    text(s, x, 2.85, 3.6, 0.5, [{'t': b, 'size': 14, 'color': GRAY, 'align': PP_ALIGN.CENTER}])
    if i < 2:
        text(s, x + 3.65, 2.1, 0.6, 0.6, [{'t': '→', 'size': 30, 'bold': True, 'color': BLUE, 'align': PP_ALIGN.CENTER}])
    x += 4.35
card(s, 0.7, 3.7, 12, 1.5, fill=REDL, line=RED)
text(s, 1.1, 3.9, 11.2, 1.2, [
    {'t': 'Sem invalidação → usuário continua vendo a versão antiga (stale)', 'size': 20, 'bold': True, 'color': RED, 'after': 4},
    {'t': 'Banco e cache precisam mostrar informações compatíveis', 'size': 16, 'color': GRAY},
])
card(s, 0.7, 5.5, 12, 1.4, fill=NAVY, line=NAVY)
text(s, 1.1, 5.7, 11.2, 1.1, [
    {'t': 'Por que é um dos problemas mais difíceis?', 'size': 20, 'bold': True, 'color': WHITE, 'after': 4},
    {'t': 'Com várias instâncias/servidores, cada cache local precisa ser avisado — manter consistência é complexo.', 'size': 16, 'color': RGBColor(0xCC, 0xDD, 0xEE)},
])
footer_num(s, 7)

# ---- 8. Local vs distribuído ----
s = slide()
header(s, 'Cache local vs. distribuído')
card(s, 0.7, 1.6, 5.9, 5.0, fill=LIGHT2)
chip(s, 1.05, 1.9, 3.4, 0.6, 'LOCAL — nossa escolha', NAVY, size=16)
for t in ['ConcurrentHashMap na memória da aplicação',
          'Simples e rápido',
          'Cada instância tem seu próprio cache',
          'Não compartilha entre servidores',
          'Suficiente para app pequena / 1 instância']:
    text(s, 1.1, 2.8 + [0,1,2,3,4][['ConcurrentHashMap na memória da aplicação','Simples e rápido','Cada instância tem seu próprio cache','Não compartilha entre servidores','Suficiente para app pequena / 1 instância'].index(t)] * 0.75, 5.3, 0.5,
         [{'t': t, 'size': 17, 'bullet': True, 'color': RGBColor(0x22,0x22,0x22), 'after': 0}])
card(s, 6.8, 1.6, 5.9, 5.0, fill=LIGHT2)
chip(s, 7.15, 1.9, 4.0, 0.6, 'DISTRIBUÍDO — ex.: Redis', BLUE, size=16)
items2 = ['Fica separado da aplicação',
          'Compartilhado por vários servidores',
          'Faz sentido quando o sistema escala',
          'Necessário com múltiplas instâncias']
for i, t in enumerate(items2):
    text(s, 7.2, 2.8 + i * 0.75, 5.3, 0.5,
         [{'t': t, 'size': 17, 'bullet': True, 'color': RGBColor(0x22,0x22,0x22), 'after': 0}])
footer_num(s, 8)

# ---- 9. Nossa solução ----
s = slide()
header(s, 'Nossa solução — arquitetura', 'Spring Boot · JPA · H2')
classes = [
    ('ConteudoController', 'recebe requisições · converte DTO', NAVY),
    ('ConteudoService', 'cache + repositório · sleep 2s na fonte', NAVY2),
    ('ConteudoCache', 'ConcurrentHashMap · LRU · TTL · estatísticas', BLUE),
    ('ConteudoRepository → Conteudo', 'banco H2 · a "fonte lenta"', GRAY),
]
y = 1.6
for i, (name, desc, cor) in enumerate(classes):
    card(s, 1.5, y, 10.3, 0.95, fill=LIGHT2, line=RGBColor(0xC9, 0xD4, 0xE4))
    rect(s, 1.5, y, 0.18, 0.95, fill=cor)
    text(s, 1.95, y + 0.1, 7.5, 0.8, [
        {'t': name, 'size': 19, 'bold': True, 'color': NAVY, 'after': 1},
        {'t': desc, 'size': 14, 'color': GRAY},
    ])
    if i < 3:
        text(s, 6.0, y + 0.95, 1.5, 0.35, [{'t': '▼', 'size': 16, 'color': BLUE, 'align': PP_ALIGN.CENTER}])
    y += 1.28
text(s, 0.7, 6.9, 12, 0.5, [
    {'t': 'Regra da disciplina: service trabalha com entidade · conversão p/ DTO fica na controller', 'size': 15, 'italic': True, 'color': GRAY, 'align': PP_ALIGN.CENTER},
])
footer_num(s, 9)

# ---- 10. Provas / resultados ----
s = slide()
header(s, 'Provas — resultados reais dos testes', 'Postman/curl + console')
# terminal escuro com evidências
rect(s, 0.7, 1.5, 7.6, 5.4, fill=DARK, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, 0.7, 1.5, 7.6, 0.55, fill=RGBColor(0x2C, 0x2C, 0x34), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(s, 1.0, 1.62, 7.0, 0.4, [
    {'t': '● ● ●   respostas HTTP', 'size': 13, 'color': RGBColor(0x99, 0x99, 0xAA), 'font': 'Consolas'},
])
lines = [
    ('GET /conteudos/1  →  X-Cache: MISS   ~2,02 s', REDL if False else RGBColor(0xFF, 0x9C, 0x9C)),
    ('GET /conteudos/1  →  X-Cache: HIT    ~0,007 s', RGBColor(0x9C, 0xE6, 0xA8)),
    ('TTL 60s → após 62s: GET id=3 → MISS ~2,01 s', RGBColor(0xFF, 0xD1, 0x8A)),
    ('PUT id=3 → próxima busca → MISS (invalidação)', RGBColor(0xFF, 0xD1, 0x8A)),
    ('DELETE id=2 → 204 · busca seguinte → 404', RGBColor(0xFF, 0xD1, 0x8A)),
]
y = 2.3
for t, c in lines:
    text(s, 1.0, y, 7.0, 0.55, [
        {'t': t, 'size': 15, 'font': 'Consolas', 'color': c, 'after': 0},
    ])
    y += 0.62
text(s, 1.0, 5.55, 7.0, 1.2, [
    {'t': 'Log do console (SLF4J):', 'size': 13, 'font': 'Consolas', 'color': RGBColor(0x99,0x99,0xAA), 'after': 4},
    {'t': 'INFO  ConteudoCache : Cache MISS - id=3 - 2015 ms', 'size': 13, 'font': 'Consolas', 'color': RGBColor(0xDD,0xDD,0xDD), 'after': 2},
    {'t': 'INFO  ConteudoCache : Cache HIT  - id=3 - 1 ms', 'size': 13, 'font': 'Consolas', 'color': RGBColor(0xDD,0xDD,0xDD)},
])
# stats card à direita
card(s, 8.6, 1.5, 4.0, 5.4, fill=LIGHT2)
chip(s, 8.9, 1.8, 3.4, 0.6, 'ESTATÍSTICAS', NAVY, size=15)
stats = [
    ('tamanho', '4 / 5'),
    ('hits', '13'),
    ('misses', '12'),
    ('evictions', '1'),
    ('hit ratio', '0.52'),
]
y = 2.7
for k, v in stats:
    text(s, 8.9, y, 1.7, 0.5, [{'t': k, 'size': 15, 'color': GRAY}])
    text(s, 10.5, y, 1.0, 0.5, [{'t': v, 'size': 18, 'bold': True, 'color': NAVY, 'align': PP_ALIGN.RIGHT}])
    y += 0.62
text(s, 8.9, 5.9, 3.4, 0.8, [
    {'t': 'GET /cache/estatisticas', 'size': 12, 'font': 'Consolas', 'color': GRAY, 'align': PP_ALIGN.CENTER},
])
footer_num(s, 10)

# ---- 11. Conclusão ----
s = slide()
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
rect(s, 0, 0, 13.333, 0.07, fill=BLUE)
text(s, 1, 0.7, 11.3, 1.0, [
    {'t': 'Conclusão', 'size': 44, 'bold': True, 'color': WHITE},
])
pts = [
    ('Consultas repetidas ficam ~300× mais rápidas', 'MISS ~2s → HIT ~7ms'),
    ('Cache precisa de limite + validade + invalidação', 'LRU · TTL 60s · PUT/DELETE'),
    ('ConcurrentHashMap + AtomicLong = seguro p/ concorrência', 'sem @Cacheable, sem Redis — versão "light"'),
    ('Para várias instâncias → cache distribuído (Redis)', 'local deixa de bastar ao escalar'),
]
y = 1.9
for titulo, sub in pts:
    card(s, 1.3, y, 10.7, 1.05, fill=RGBColor(0x27, 0x3D, 0x66), line=RGBColor(0x3A, 0x56, 0x8C), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, 1.7, y + 0.12, 9.9, 0.85, [
        {'t': titulo, 'size': 20, 'bold': True, 'color': WHITE, 'after': 2},
        {'t': sub, 'size': 14, 'color': RGBColor(0xAA, 0xC4, 0xE8)},
    ])
    y += 1.3
text(s, 1, 6.9, 11.3, 0.5, [
    {'t': 'João Pedro Santos Pinheiro · RA 04251097 · SPTECH', 'size': 15, 'color': RGBColor(0x88, 0x9C, 0xBE), 'align': PP_ALIGN.CENTER},
])

prs.save('Apresentacao_Cache_HashMap_v4.pptx')
print('salvo')
