from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Defina sua própria chave secreta para segurança

usuarios = [
    {'nome': 'Aluno', 'tipo': 'aluno', 'email': 'aluno@example.com', 'senha': 'senha_aluno', 'telefone': '123456789', 'serie': '10'},
    {'nome': 'Professor', 'tipo': 'professor', 'email': 'professor@example.com', 'senha': 'senha_professor', 'telefone': '987654321', 'disciplina': 'Matemática'}
]
agendamentos = []
caixa_registros = []

# Função para encontrar um usuário pelo email
def encontrar_usuario_por_email(email):
    for usuario in usuarios:
        if usuario['email'] == email:
            return usuario
    return None

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = encontrar_usuario_por_email(email)
        if usuario and usuario['senha'] == senha:
            session['email'] = email
            flash('Login bem-sucedido!', 'success')
            if usuario['tipo'] == 'professor':
                return redirect(url_for('relatorio'))
            else:
                return redirect(url_for('agenda'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
    return render_template('login.html')

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        if tipo == 'aluno':
            serie = request.form['serie']
            usuarios.append({'nome': nome, 'tipo': tipo, 'email': email, 'senha': senha, 'telefone': telefone, 'serie': serie})
        elif tipo == 'professor':
            disciplina = request.form['disciplina']
            usuarios.append({'nome': nome, 'tipo': tipo, 'email': email, 'senha': senha, 'telefone': telefone, 'disciplina': disciplina})
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

# Rota para a página de agenda
@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if 'email' in session:
        if request.method == 'POST':
            data = request.form['data']
            disciplina = request.form['disciplina']
            atividade = request.form['atividade']
            agendamentos.append({'data': data, 'disciplina': disciplina, 'atividade': atividade, 'aluno': session['email']})
            flash('Agendamento realizado com sucesso!', 'success')
        return render_template('agenda.html', agendamentos=agendamentos)
    else:
        flash('Faça o login para acessar esta página.', 'danger')
        return redirect(url_for('login'))

# Rota para o relatório diário dos agendamentos (apenas para professores)
@app.route('/relatorio', methods=['GET'])
def relatorio():
    if 'email' in session:
        email = session['email']
        usuario = encontrar_usuario_por_email(email)
        if usuario and usuario['tipo'] == 'professor':
            return render_template('relatorio.html', agendamentos=agendamentos)
    flash('Acesso não autorizado. Faça o login como professor.', 'danger')
    return redirect(url_for('login'))

# Rota para o caixa (registro de atividades dos estudantes)
@app.route('/caixa', methods=['GET', 'POST'])
def caixa():
    if 'email' in session:
        if request.method == 'POST':
            data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            descricao = request.form['descricao']
            valor = float(request.form['valor'])
            caixa_registros.append({'data': data, 'descricao': descricao, 'valor': valor})
            flash('Atividade registrada no caixa com sucesso!', 'success')
        return render_template('caixa.html', caixa_registros=caixa_registros)
    else:
        flash('Faça o login para acessar esta página.', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
