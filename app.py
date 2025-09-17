#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTF (Capture The Flag) Web Application
======================================

Uma aplicação Flask educacional com 4 fases demonstrando vulnerabilidades web comuns:
1. HTML Injection com comentários ocultos
2. Broken Access Control (BAC) 
3. SQL Injection simples
4. Insecure Direct Object Reference (IDOR)

Autor: Educacional - Demonstração de Vulnerabilidades Web
"""

from flask import Flask, request, render_template, redirect, url_for, session, make_response
import os

app = Flask(__name__)

# Configuração da chave secreta para sessões
# VULNERABILIDADE EDUCACIONAL: Em produção, nunca use chave hardcoded
app.secret_key = os.getenv('SESSION_SECRET', 'chave_super_secreta_ctf_2025')

# Flags do CTF - formato especificado
FLAGS = {
    'fase1': 'flag{comentario_oculto}',
    'fase2': 'flag{privilegio_elevado}', 
    'fase3': 'flag{login_invalido}',
    'fase4': 'flag{caminho_secreto}'
}

# Simulação de banco de dados para demonstração
FAKE_USERS_DB = {
    '1': {'nome': 'Usuario Comum', 'nivel': 'user'},
    '1337': {'nome': 'Administrador', 'nivel': 'admin', 'flag': FLAGS['fase2']}
}

# Inicializar progresso do usuário na sessão
def init_session():
    if 'completed_phases' not in session:
        session['completed_phases'] = []
    if 'current_phase' not in session:
        session['current_phase'] = 1

@app.route('/')
def home():
    """Página principal com navegação para as fases do CTF"""
    init_session()
    return render_template('home.html', 
                         completed_phases=session.get('completed_phases', []),
                         current_phase=session.get('current_phase', 1))

# ===== FASE 1: HTML INJECTION E COMENTÁRIO OCULTO =====
@app.route('/fase1', methods=['GET', 'POST'])
def fase1():
    """
    VULNERABILIDADE: HTML Injection
    
    Esta função não sanitiza a entrada do usuário, permitindo injeção de HTML.
    A flag está oculta em um comentário HTML que só aparece quando o usuário
    consegue quebrar a estrutura HTML existente através de injeção.
    """
    init_session()
    
    if request.method == 'POST':
        # VULNERABILIDADE: Não há sanitização da entrada do usuário
        # Isso permite HTML Injection quando o usuário submete HTML válido
        feedback = request.form.get('feedback', '')
        
        # Comentário oculto com flag que só aparece com HTML injection específico
        hidden_comment = f"<!-- DICA SECRETA: {FLAGS['fase1']} -->"
        
        # A flag só aparece se o usuário conseguir quebrar o input HTML
        # Exemplo: "><script>alert('html injection')</script><!--
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CTF - Fase 1: Feedback</title>
        </head>
        <body>
            <h1>Obrigado pelo seu feedback!</h1>
            <p>Seu feedback: <input type="text" value="{feedback}"{hidden_comment if '>' in feedback and '<' in feedback else ''}></p>
            <a href="/">Voltar ao início</a>
            <!-- Se você conseguiu quebrar o HTML acima, a flag deve ter aparecido! -->
        </body>
        </html>
        """
        return response_html
    
    return render_template('fase1.html')

@app.route('/validate_flag', methods=['POST'])
def validate_flag():
    """Validação de flags para progressão entre fases"""
    init_session()
    
    phase = int(request.form.get('phase', 0))
    submitted_flag = request.form.get('flag', '').strip()
    
    # Verificar se a flag está correta
    key = f'fase{phase}'
    if key in FLAGS and submitted_flag == FLAGS[key]:
        # Marcar fase como completa
        if phase not in session['completed_phases']:
            session['completed_phases'].append(phase)
            session['current_phase'] = phase + 1
            session.permanent = True
        
        return redirect(url_for('home'))
    
    return render_template('error.html', message="Flag incorreta! Tente novamente.")

# ===== FASE 2: BROKEN ACCESS CONTROL (BAC) =====
@app.route('/fase2')
def fase2():
    """Interface para acessar perfis de usuário"""
    init_session()
    if 1 not in session.get('completed_phases', []):
        return render_template('error.html', message="Complete a Fase 1 primeiro!")
    
    return render_template('fase2.html')

@app.route('/perfil')
def perfil():
    """
    VULNERABILIDADE: Broken Access Control
    
    Esta função não valida se o usuário tem permissão para acessar
    diferentes IDs de usuário. Permite escalação de privilégios
    simplesmente mudando o parâmetro 'id' na URL.
    """
    user_id = request.args.get('id', '1')
    
    # VULNERABILIDADE: Não há controle de acesso!
    # Qualquer usuário pode acessar qualquer ID apenas mudando a URL
    if user_id in FAKE_USERS_DB:
        user_info = FAKE_USERS_DB[user_id]
        
        # A flag só aparece para o admin (id=1337)
        is_admin = user_info.get('nivel') == 'admin'
        flag = user_info.get('flag') if is_admin else None
        
        return render_template('perfil.html', 
                             user=user_info, 
                             user_id=user_id,
                             is_admin=is_admin,
                             flag=flag)
    
    return render_template('error.html', message="Usuário não encontrado!")

# ===== FASE 3: SQL INJECTION =====
@app.route('/fase3', methods=['GET', 'POST'])
def fase3():
    """
    VULNERABILIDADE: SQL Injection
    
    Esta função simula um sistema de login vulnerável a SQL injection.
    A consulta SQL é construída de forma insegura, permitindo que
    atacantes manipulem a lógica da consulta.
    """
    init_session()
    if 2 not in session.get('completed_phases', []):
        return render_template('error.html', message="Complete a Fase 2 primeiro!")
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABILIDADE: SQL Injection
        # NUNCA faça isso em produção! Use prepared statements/parametrized queries
        sql_query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
        
        # Simular resultado da consulta SQL vulnerável
        # A injeção ' OR '1'='1'-- faz a consulta sempre retornar True
        if "' OR '1'='1'" in username or "' OR '1'='1'" in password:
            # Login bem-sucedido via SQL injection!
            return render_template('fase3_success.html', 
                                 flag=FLAGS['fase3'],
                                 sql_query=sql_query)
        elif username == 'admin' and password == 'senha123':
            # Login legítimo (mas não é o objetivo do desafio)
            return render_template('fase3_success.html', 
                                 flag=FLAGS['fase3'],
                                 sql_query=sql_query)
        else:
            return render_template('fase3.html', 
                                 error="Credenciais inválidas!",
                                 sql_query=sql_query)
    
    return render_template('fase3.html')

# ===== FASE 4: INSECURE DIRECT OBJECT REFERENCE (IDOR) =====
@app.route('/fase4')
def fase4():
    """Interface para visualizar documentos"""
    init_session()
    if 3 not in session.get('completed_phases', []):
        return render_template('error.html', message="Complete a Fase 3 primeiro!")
    
    return render_template('fase4.html')

@app.route('/documento')
def documento():
    """
    VULNERABILIDADE: Insecure Direct Object Reference (IDOR)
    
    Esta função permite acesso direto a arquivos sem validação adequada.
    Um atacante pode manipular o parâmetro 'file' para acessar arquivos
    não autorizados do sistema.
    """
    filename = request.args.get('file', 'doc1.txt')
    
    # VULNERABILIDADE: Não há validação do caminho do arquivo!
    # Em produção, sempre use werkzeug.utils.safe_join() e valide permissões
    
    # Simulação de arquivos disponíveis
    files_content = {
        'doc1.txt': 'Este é o documento público número 1.\nConteúdo: Informações gerais da empresa.',
        'doc2.txt': 'Este é o documento público número 2.\nConteúdo: Políticas de uso.',
        'flag.txt': f'DOCUMENTO CONFIDENCIAL!\nFlag secreta: {FLAGS["fase4"]}\nParabéns, você explorou IDOR!',
        '../flag.txt': f'DOCUMENTO CONFIDENCIAL!\nFlag secreta: {FLAGS["fase4"]}\nVocê conseguiu fazer path traversal!',
        'admin/flag.txt': f'DOCUMENTO ADMINISTRATIVO!\nFlag secreta: {FLAGS["fase4"]}\nVulnerabilidade IDOR explorada com sucesso!'
    }
    
    if filename in files_content:
        content = files_content[filename]
        return render_template('documento.html', filename=filename, content=content)
    
    return render_template('error.html', message=f"Arquivo '{filename}' não encontrado!")

# ===== ROTAS AUXILIARES =====
@app.route('/reset')
def reset_progress():
    """Resetar progresso do CTF"""
    session.clear()
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Página não encontrada!"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message="Erro interno do servidor!"), 500

if __name__ == '__main__':
    # Criar diretório de templates se não existir
    os.makedirs('templates', exist_ok=True)
    
    # Executar aplicação Flask
    # NOTA: Em produção, use um servidor WSGI como Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)