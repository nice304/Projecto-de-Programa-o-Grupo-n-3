import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from collections import Counter

class BibliotecaApp:
    """Classe principal da aplicação Biblioteca ISCAT - VERSÃO FINAL COMPLETA"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca ISCAT - Sistema de Gestão Completo")
        self.root.geometry("1100x750")
        
        # Configurar ícone e tema
        self.root.configure(bg='#f0f0f0')
        
        # Configurar dados
        self.arquivo_livros = "biblioteca_livros.json"
        self.arquivo_usuarios = "biblioteca_usuarios.json"
        self.arquivo_emprestimos = "biblioteca_emprestimos.json"
        
        self.livros = self.carregar_dados(self.arquivo_livros)
        self.usuarios = self.carregar_dados(self.arquivo_usuarios)
        self.emprestimos = self.carregar_dados(self.arquivo_emprestimos)
        
        # Configurar menu principal
        self.criar_menu()
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(0, weight=1)
        
        # Tela inicial
        self.criar_tela_inicial()
    
    def criar_menu(self):
        """Cria o menu principal da aplicação"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Exportar Dados", command=self.exportar_dados)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        
        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        menu_cadastros.add_command(label="Livros", command=self.abrir_cadastro_livros)
        menu_cadastros.add_command(label="Usuários", command=self.abrir_cadastro_usuarios)
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Voltar à Tela Inicial", command=self.criar_tela_inicial)
        
        # Menu Empréstimos
        menu_emprestimos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Empréstimos", menu=menu_emprestimos)
        menu_emprestimos.add_command(label="Novo Empréstimo", command=self.abrir_novo_emprestimo)
        menu_emprestimos.add_command(label="Gerenciar Empréstimos", command=self.abrir_gerenciar_emprestimos)
        
        # Menu Consultas
        menu_consultas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Consultas", menu=menu_consultas)
        menu_consultas.add_command(label="Consulta de Livros", command=self.abrir_consulta_livros)
        menu_consultas.add_command(label="Ver Estoque", command=self.abrir_estoque)
        menu_consultas.add_command(label="Buscar Livro", command=self.abrir_busca_livros)
        
        # Menu Relatórios
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_relatorios.add_command(label="Livros Mais Emprestados", command=self.relatorio_livros_mais_emprestados)
        menu_relatorios.add_command(label="Histórico de Movimentação", command=self.abrir_historico_movimentacao)
        menu_relatorios.add_command(label="Situação do Acervo", command=self.relatorio_situacao_acervo)
        menu_relatorios.add_separator()
        menu_relatorios.add_command(label="Relatório Completo", command=self.relatorio_completo)
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Guia Rápido", command=self.mostrar_guia_rapido)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
    
    def criar_tela_inicial(self):
        """Cria a tela inicial do sistema"""
        # Limpar frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        # Frame de cabeçalho
        frame_cabecalho = ttk.Frame(self.frame_principal)
        frame_cabecalho.grid(row=0, column=0, pady=(0, 30), sticky=(tk.W, tk.E))
        
        # Título
        titulo = ttk.Label(
            frame_cabecalho, 
            text="📚 Biblioteca ISCAT",
            font=("Arial", 24, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0)
        
        subtitulo = ttk.Label(
            frame_cabecalho,
            text="Sistema Integrado de Gestão de Biblioteca",
            font=("Arial", 12),
            foreground="#7f8c8d"
        )
        subtitulo.grid(row=1, column=0, pady=(5, 0))
        
        # Frame de estatísticas
        frame_stats = ttk.LabelFrame(
            self.frame_principal, 
            text="📊 Dashboard - Visão Geral", 
            padding="20",
            relief="solid"
        )
        frame_stats.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Calcular estatísticas
        total_livros = sum(livro.get('quantidade', 0) for livro in self.livros.values())
        livros_unicos = len(self.livros)
        total_usuarios = len(self.usuarios)
        
        # Empréstimos ativos
        emprestimos_ativos = sum(1 for emp in self.emprestimos.values() if emp.get('status') == 'ativo')
        
        # Livros disponíveis
        livros_disponiveis = sum(
            1 for livro in self.livros.values() 
            if livro.get('quantidade', 0) > 0
        )
        
        # Exibir estatísticas em grid
        stats_data = [
            ("📖 Total de Livros", f"{total_livros} unidades"),
            ("📚 Títulos Diferentes", f"{livros_unicos} títulos"),
            ("👥 Usuários Cadastrados", f"{total_usuarios} usuários"),
            ("🔄 Empréstimos Ativos", f"{emprestimos_ativos} empréstimos"),
            ("✅ Livros Disponíveis", f"{livros_disponiveis} títulos"),
            ("📈 Taxa de Empréstimo", f"{(emprestimos_ativos/total_usuarios*100 if total_usuarios > 0 else 0):.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(frame_stats, text=label, font=("Arial", 10, "bold"), 
                     foreground="#34495e").grid(row=row, column=col, sticky=tk.W, pady=8, padx=(0, 10))
            ttk.Label(frame_stats, text=value, font=("Arial", 11), 
                     foreground="#2c3e50").grid(row=row, column=col+1, sticky=tk.W, pady=8)
        
        # Frame de botões rápidos
        frame_botoes = ttk.LabelFrame(self.frame_principal, text="⚡ Acesso Rápido", padding="15")
        frame_botoes.grid(row=2, column=0, pady=(0, 20))
        
        # Botões para funcionalidades principais
        botoes_rapidos = [
            ("📚 Gerenciar Livros", self.abrir_cadastro_livros),
            ("👥 Gerenciar Usuários", self.abrir_cadastro_usuarios),
            ("🔄 Novo Empréstimo", self.abrir_novo_emprestimo),
            ("📋 Empréstimos Ativos", self.abrir_gerenciar_emprestimos),
            ("🔍 Consultar Livros", self.abrir_consulta_livros),
            ("📊 Ver Relatórios", self.abrir_tela_relatorios)
        ]
        
        for i, (texto, comando) in enumerate(botoes_rapidos):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                frame_botoes,
                text=texto,
                command=comando,
                width=20
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        # Frame de últimas atividades
        frame_atividades = ttk.LabelFrame(self.frame_principal, text="📝 Últimas Atividades", padding="15")
        frame_atividades.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Obter últimas atividades
        atividades = self.obter_ultimas_atividades(5)
        
        if atividades:
            for i, atividade in enumerate(atividades):
                ttk.Label(frame_atividades, text=f"• {atividade}", 
                         font=("Arial", 9)).grid(row=i, column=0, sticky=tk.W, pady=2)
        else:
            ttk.Label(frame_atividades, text="Nenhuma atividade registrada.", 
                     font=("Arial", 9), foreground="#7f8c8d").grid(row=0, column=0, sticky=tk.W)
        
        # Centralizar conteúdo
        self.frame_principal.columnconfigure(0, weight=1)
    
    def obter_ultimas_atividades(self, limite=5):
        """Retorna as últimas atividades do sistema"""
        atividades = []
        
        # Adicionar últimos empréstimos
        emprestimos_recentes = sorted(
            self.emprestimos.items(),
            key=lambda x: x[1].get('data_emprestimo', ''),
            reverse=True
        )[:limite]
        
        for emp_id, emprestimo in emprestimos_recentes:
            usuario = self.usuarios.get(emprestimo.get('id_usuario', ''), {})
            livro = self.livros.get(emprestimo.get('isbn_livro', ''), {})
            
            if emprestimo.get('status') == 'ativo':
                atividades.append(
                    f"Empréstimo: {usuario.get('nome', '')} pegou '{livro.get('título', '')}'"
                )
            else:
                atividades.append(
                    f"Devolução: {usuario.get('nome', '')} devolveu '{livro.get('título', '')}'"
                )
        
        return atividades[:limite]
    
    def abrir_cadastro_livros(self):
        """Abre a tela de cadastro de livros"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaLivros(self.frame_principal, self)
    
    def abrir_cadastro_usuarios(self):
        """Abre a tela de cadastro de usuários"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaUsuarios(self.frame_principal, self)
    
    def abrir_novo_emprestimo(self):
        """Abre a tela de novo empréstimo"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaNovoEmprestimo(self.frame_principal, self)
    
    def abrir_gerenciar_emprestimos(self):
        """Abre a tela de gerenciamento de empréstimos"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaGerenciarEmprestimos(self.frame_principal, self)
    
    def abrir_consulta_livros(self):
        """Abre a tela de consulta de livros"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaConsultaEstoque(self.frame_principal, self)
    
    def abrir_estoque(self):
        """Abre a tela de visualização de estoque"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaEstoque(self.frame_principal, self)
    
    def abrir_busca_livros(self):
        """Abre a tela de busca de livros"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaBuscaLivros(self.frame_principal, self)
    
    def abrir_historico_movimentacao(self):
        """Abre a tela de histórico de movimentação"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaHistoricoMovimentacao(self.frame_principal, self)
    
    def abrir_tela_relatorios(self):
        """Abre a tela de relatórios"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        TelaRelatorios(self.frame_principal, self)
    
    def carregar_dados(self, arquivo):
        """Carrega os dados de um arquivo JSON"""
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    # Garantir que todos os usuários tenham histórico
                    if "usuarios" in arquivo:
                        for user_id, usuario in dados.items():
                            if 'historico' not in usuario:
                                usuario['historico'] = []
                    return dados
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def salvar_dados(self, dados, arquivo):
        """Salva os dados em um arquivo JSON"""
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados em {arquivo}: {str(e)}")
            return False
    
    def salvar_todos_dados(self):
        """Salva todos os dados do sistema"""
        success = True
        success = self.salvar_dados(self.livros, self.arquivo_livros) and success
        success = self.salvar_dados(self.usuarios, self.arquivo_usuarios) and success
        success = self.salvar_dados(self.emprestimos, self.arquivo_emprestimos) and success
        return success
    
    def gerar_id_unico(self, prefixo):
        """Gera um ID único baseado em um prefixo"""
        contador = 1
        while f"{prefixo}{contador:04d}" in self.emprestimos:
            contador += 1
        return f"{prefixo}{contador:04d}"
    
    def calcular_multa(self, data_devolucao_prevista):
        """Calcula multa por atraso (500 Kz por dia de atraso)"""
        try:
            hoje = datetime.now().date()
            data_prevista = datetime.strptime(data_devolucao_prevista, "%Y-%m-%d").date()
            
            if hoje > data_prevista:
                dias_atraso = (hoje - data_prevista).days
                return dias_atraso * 500.00
            return 0.00
        except (ValueError, TypeError):
            return 0.00
    
    def buscar_livros(self, termo):
        """Busca livros por título ou autor"""
        resultados = []
        termo_lower = termo.lower()
        
        for isbn, livro in self.livros.items():
            if (termo_lower in livro.get('título', '').lower() or 
                termo_lower in livro.get('autor', '').lower() or
                termo_lower in isbn.lower()):
                resultados.append((isbn, livro))
        
        return resultados
    
    def calcular_livros_mais_emprestados(self, limite=10):
        """Calcula os livros mais emprestados"""
        contagem = Counter()
        
        for emprestimo in self.emprestimos.values():
            isbn = emprestimo.get('isbn_livro')
            if isbn:
                contagem[isbn] += 1
        
        # Ordenar por frequência
        mais_emprestados = contagem.most_common(limite)
        
        # Adicionar informações dos livros
        resultado = []
        for isbn, count in mais_emprestados:
            livro = self.livros.get(isbn, {})
            resultado.append({
                'isbn': isbn,
                'título': livro.get('título', 'Desconhecido'),
                'autor': livro.get('autor', 'Desconhecido'),
                'emprestimos': count
            })
        
        return resultado
    
    def obter_movimentacao(self, limite_dias=30):
        """Obtém a movimentação dos últimos dias"""
        hoje = datetime.now()
        data_limite = hoje - timedelta(days=limite_dias)
        
        movimentacao = []
        
        for emp_id, emprestimo in self.emprestimos.items():
            try:
                data_emp = datetime.strptime(emprestimo.get('data_emprestimo', ''), "%Y-%m-%d")
                
                if data_emp >= data_limite:
                    usuario = self.usuarios.get(emprestimo.get('id_usuario', ''), {})
                    livro = self.livros.get(emprestimo.get('isbn_livro', ''), {})
                    
                    movimentacao.append({
                        'data': emprestimo.get('data_emprestimo'),
                        'tipo': 'EMPRÉSTIMO',
                        'usuario': usuario.get('nome', 'Desconhecido'),
                        'livro': livro.get('título', 'Desconhecido'),
                        'status': '🔄' if emprestimo.get('status') == 'ativo' else '✅'
                    })
                    
                    if emprestimo.get('status') == 'devolvido':
                        data_dev = emprestimo.get('data_devolucao_real', '')
                        if data_dev:
                            movimentacao.append({
                                'data': data_dev,
                                'tipo': 'DEVOLUÇÃO',
                                'usuario': usuario.get('nome', 'Desconhecido'),
                                'livro': livro.get('título', 'Desconhecido'),
                                'status': '✅'
                            })
            except (ValueError, TypeError):
                continue
        
        # Ordenar por data
        movimentacao.sort(key=lambda x: x['data'], reverse=True)
        
        return movimentacao
    
    def relatorio_livros_mais_emprestados(self):
        """Exibe relatório dos livros mais emprestados"""
        mais_emprestados = self.calcular_livros_mais_emprestados(10)
        
        if not mais_emprestados:
            messagebox.showinfo("Livros Mais Emprestados", "Não há dados de empréstimos disponíveis.")
            return
        
        relatorio = "📚 TOP 10 LIVROS MAIS EMPRESTADOS\n\n"
        relatorio += "Pos. | Título | Autor | Empréstimos\n"
        relatorio += "-" * 60 + "\n"
        
        for i, livro in enumerate(mais_emprestados, 1):
            relatorio += f"{i:2d}. | {livro['título'][:30]:30} | {livro['autor'][:20]:20} | {livro['emprestimos']:3d}\n"
        
        messagebox.showinfo("Relatório - Livros Mais Emprestados", relatorio)
    
    def relatorio_situacao_acervo(self):
        """Exibe relatório da situação do acervo"""
        total_livros = sum(livro.get('quantidade', 0) for livro in self.livros.values())
        livros_unicos = len(self.livros)
        
        # Contar por gênero
        generos = Counter()
        for livro in self.livros.values():
            genero = livro.get('gênero', 'Sem Gênero')
            generos[genero] += livro.get('quantidade', 0)
        
        # Livros disponíveis vs emprestados
        disponiveis = sum(
            livro.get('quantidade', 0) for livro in self.livros.values()
        )
        emprestados = sum(
            1 for emp in self.emprestimos.values() 
            if emp.get('status') == 'ativo'
        )
        
        relatorio = "📊 SITUAÇÃO DO ACERVO\n\n"
        relatorio += f"Total de Livros: {total_livros} unidades\n"
        relatorio += f"Títulos Diferentes: {livros_unicos}\n"
        relatorio += f"Livros Disponíveis: {disponiveis}\n"
        relatorio += f"Livros Emprestados: {emprestados}\n"
        relatorio += f"Taxa de Empréstimo: {(emprestados/disponiveis*100 if disponiveis > 0 else 0):.1f}%\n\n"
        
        relatorio += "📈 DISTRIBUIÇÃO POR GÊNERO\n"
        for genero, quantidade in generos.most_common():
            percentual = (quantidade / total_livros * 100) if total_livros > 0 else 0
            relatorio += f"  {genero}: {quantidade} ({percentual:.1f}%)\n"
        
        messagebox.showinfo("Relatório - Situação do Acervo", relatorio)
    
    def relatorio_completo(self):
        """Exibe relatório completo do sistema"""
        total_livros = sum(livro.get('quantidade', 0) for livro in self.livros.values())
        livros_unicos = len(self.livros)
        total_usuarios = len(self.usuarios)
        
        # Empréstimos totais
        total_emprestimos = len(self.emprestimos)
        emprestimos_ativos = sum(1 for emp in self.emprestimos.values() if emp.get('status') == 'ativo')
        emprestimos_devolvidos = total_emprestimos - emprestimos_ativos
        
        # Usuários por tipo
        tipos_usuarios = Counter()
        for usuario in self.usuarios.values():
            tipo = usuario.get('tipo', 'Desconhecido')
            tipos_usuarios[tipo] += 1
        
        relatorio = "📋 RELATÓRIO COMPLETO - BIBLIOTECA ISCAT\n\n"
        relatorio += "📚 ACERVO\n"
        relatorio += f"  • Total de Livros: {total_livros}\n"
        relatorio += f"  • Títulos Diferentes: {livros_unicos}\n\n"
        
        relatorio += "👥 USUÁRIOS\n"
        relatorio += f"  • Total de Usuários: {total_usuarios}\n"
        for tipo, quantidade in tipos_usuarios.most_common():
            relatorio += f"  • {tipo}: {quantidade}\n"
        relatorio += "\n"
        
        relatorio += "🔄 EMPRÉSTIMOS\n"
        relatorio += f"  • Total de Empréstimos: {total_emprestimos}\n"
        relatorio += f"  • Empréstimos Ativos: {emprestimos_ativos}\n"
        relatorio += f"  • Empréstimos Devolvidos: {emprestimos_devolvidos}\n"
        
        if total_emprestimos > 0:
            taxa_devolucao = (emprestimos_devolvidos / total_emprestimos * 100)
            relatorio += f"  • Taxa de Devolução: {taxa_devolucao:.1f}%\n"
        
        messagebox.showinfo("Relatório Completo", relatorio)
    
    def relatorio_usuarios_ativos(self):
        """Exibe relatório de usuários ativos (com empréstimos)"""
        usuarios_ativos = {}
        
        for emp in self.emprestimos.values():
            if emp.get('status') == 'ativo':
                usuario_id = emp.get('id_usuario', '')
                if usuario_id:
                    if usuario_id not in usuarios_ativos:
                        usuarios_ativos[usuario_id] = 0
                    usuarios_ativos[usuario_id] += 1
        
        if not usuarios_ativos:
            messagebox.showinfo("Usuários Ativos", "Não há usuários com empréstimos ativos.")
            return
        
        relatorio = "👥 USUÁRIOS COM EMPRÉSTIMOS ATIVOS\n\n"
        for usuario_id, qtd_emprestimos in usuarios_ativos.items():
            usuario = self.usuarios.get(usuario_id, {})
            relatorio += f"Nome: {usuario.get('nome', 'Desconhecido')}\n"
            relatorio += f"Tipo: {usuario.get('tipo', 'Desconhecido')}\n"
            relatorio += f"Empréstimos ativos: {qtd_emprestimos}\n"
            relatorio += "-" * 40 + "\n"
        
        messagebox.showinfo("Relatório - Usuários Ativos", relatorio)
    
    def relatorio_livros_emprestados(self):
        """Exibe relatório de livros emprestados"""
        emprestimos_ativos = [emp for emp in self.emprestimos.values() if emp.get('status') == 'ativo']
        
        if not emprestimos_ativos:
            messagebox.showinfo("Livros Emprestados", "Não há livros emprestados no momento.")
            return
        
        relatorio = "📚 LIVROS EMPRESTADOS ATIVOS\n\n"
        for emp in emprestimos_ativos:
            livro = self.livros.get(emp.get('isbn_livro', ''), {})
            usuario = self.usuarios.get(emp.get('id_usuario', ''), {})
            
            relatorio += f"Livro: {livro.get('título', 'Desconhecido')}\n"
            relatorio += f"Usuário: {usuario.get('nome', 'Desconhecido')}\n"
            relatorio += f"Data Empréstimo: {emp.get('data_emprestimo', 'N/A')}\n"
            relatorio += f"Data Devolução: {emp.get('data_devolucao_prevista', 'N/A')}\n"
            relatorio += "-" * 40 + "\n"
        
        messagebox.showinfo("Relatório - Livros Emprestados", relatorio)
    
    def exportar_dados(self):
        """Exporta dados para arquivo de texto"""
        try:
            with open("biblioteca_exportacao.txt", "w", encoding='utf-8') as f:
                f.write("EXPORTAÇÃO DE DADOS - BIBLIOTECA ISCAT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("LIVROS CADASTRADOS:\n")
                f.write("-" * 40 + "\n")
                for isbn, livro in self.livros.items():
                    f.write(f"ISBN: {isbn}\n")
                    f.write(f"Título: {livro.get('título', '')}\n")
                    f.write(f"Autor: {livro.get('autor', '')}\n")
                    f.write(f"Gênero: {livro.get('gênero', '')}\n")
                    f.write(f"Quantidade: {livro.get('quantidade', 0)}\n")
                    f.write("-" * 40 + "\n")
                
                f.write("\n\nUSUÁRIOS CADASTRADOS:\n")
                f.write("-" * 40 + "\n")
                for user_id, usuario in self.usuarios.items():
                    f.write(f"ID: {user_id}\n")
                    f.write(f"Nome: {usuario.get('nome', '')}\n")
                    f.write(f"Tipo: {usuario.get('tipo', '')}\n")
                    f.write(f"Data Cadastro: {usuario.get('data_cadastro', '')}\n")
                    f.write("-" * 40 + "\n")
                
                f.write("\n\nEMPREÉSTIMOS ATIVOS:\n")
                f.write("-" * 40 + "\n")
                for emp_id, emprestimo in self.emprestimos.items():
                    if emprestimo.get('status') == 'ativo':
                        f.write(f"ID Empréstimo: {emp_id}\n")
                        f.write(f"Usuário: {emprestimo.get('id_usuario', '')}\n")
                        f.write(f"Livro: {emprestimo.get('isbn_livro', '')}\n")
                        f.write(f"Data Empréstimo: {emprestimo.get('data_emprestimo', '')}\n")
                        f.write(f"Data Devolução Prevista: {emprestimo.get('data_devolucao_prevista', '')}\n")
                        f.write("-" * 40 + "\n")
            
            messagebox.showinfo("Exportação", "Dados exportados com sucesso para 'biblioteca_exportacao.txt'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")
    
    def mostrar_guia_rapido(self):
        """Exibe guia rápido do sistema"""
        guia = """
        📖 GUIA RÁPIDO - BIBLIOTECA ISCAT
        
        1. 📚 CADASTRO DE LIVROS
           • Adicione novos livros com título, autor, ISBN, gênero e quantidade
           • Edite ou exclua livros existentes
           • Verifique se um livro já existe
        
        2. 👥 CONTROLE DE USUÁRIOS
           • Cadastre usuários (Aluno, Professor, Funcionário, Visitante)
           • Consulte histórico de empréstimos por usuário
        
        3. 🔄 SISTEMA DE EMPRÉSTIMOS
           • Realize novos empréstimos
           • Registre devoluções
           • Controle prazos e multas (500 Kz/dia de atraso)
        
        4. 🔍 CONSULTAS E ESTOQUE
           • Consulte todos os livros cadastrados
           • Veja livros disponíveis e indisponíveis
           • Busque livros por título ou autor
        
        5. 📊 RELATÓRIO
           • Livros mais emprestados
           • Histórico de movimentação
           • Situação atual do acervo
        
        💡 DICA: Use o menu superior para navegar entre as telas.
        """
        
        messagebox.showinfo("Guia Rápido", guia)
    
    def mostrar_sobre(self):
        """Exibe informações sobre o sistema"""
        messagebox.showinfo(
            "Sobre - Biblioteca ISCAT",
            "Biblioteca ISCAT - Sistema de Gestão Completo\n\n"
            "Versão 3.0 - Final\n"
            "Módulos implementados:\n"
            "✓ Cadastro de Livros\n"
            "✓ Controle de Usuários\n"
            "✓ Sistema de Empréstimos\n"
            "✓ Consultas e Estoque\n"
            "✓ Relatórios Avançados\n\n"
            "Desenvolvido com Python e Tkinter\n"
            "Para fins educacionais e acadêmicos\n\n"
            "🎓 Sistema pronto para apresentação e estudo!"
        )


class TelaLivros:
    """Classe para a tela de cadastro de livros"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
        self.atualizar_lista_livros()

    def validar_isbn_input(self, texto_novo):
        """
        Valida a entrada do ISBN:
        - Permite apagar (texto vazio)
        - Apenas números
        - Máximo 5 caracteres
        """
        if texto_novo == "":
            return True
        if not texto_novo.isdigit():
            return False
        if len(texto_novo) > 13:
            return False
        return True
    
    def criar_widgets(self):
        """Cria a interface da tela de livros"""
        titulo = ttk.Label(
            self.frame,
            text="📚 Cadastro de Livros",
            font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        frame_form = ttk.LabelFrame(self.frame, text="Dados do Livro", padding="15")
        frame_form.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        campos = [
            ("Título:", 0),
            ("Autor:", 1),
            ("ISBN:", 2),
            ("Gênero:", 3),
            ("Quantidade:", 4)
        ]

        # Registro do validador de ISBN
        vcmd_isbn = (self.frame.register(self.validar_isbn_input), '%P')
        
        self.entries = {}
        for i, (texto, linha) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=linha, column=0, sticky=tk.W, pady=5)
            
            # Aplicar validação apenas no campo ISBN
            if "ISBN" in texto:
                entry = ttk.Entry(frame_form, width=40, validate='key', validatecommand=vcmd_isbn)
            else:
                entry = ttk.Entry(frame_form, width=40)
                
            entry.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            self.entries[texto.replace(":", "").lower()] = entry
        
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_livro).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Editar", command=self.editar_livro).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_livro).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos).grid(row=0, column=3, padx=5)
        ttk.Button(frame_botoes, text="Verificar", command=self.verificar_livro).grid(row=0, column=4, padx=5)
        
        frame_lista = ttk.LabelFrame(self.frame, text="Livros Cadastrados", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("título", "autor", "isbn", "gênero", "quantidade")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15)
        
        self.treeview.heading("título", text="Título")
        self.treeview.heading("autor", text="Autor")
        self.treeview.heading("isbn", text="ISBN")
        self.treeview.heading("gênero", text="Gênero")
        self.treeview.heading("quantidade", text="Quantidade")
        
        self.treeview.column("título", width=200)
        self.treeview.column("autor", width=150)
        self.treeview.column("isbn", width=120)
        self.treeview.column("gênero", width=100)
        self.treeview.column("quantidade", width=80)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.treeview.bind("<<TreeviewSelect>>", self.selecionar_livro)
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="📊 Ver Relatórios", 
                  command=self.app.abrir_tela_relatorios).grid(row=0, column=1, padx=5)
    
    def adicionar_livro(self):
        """Adiciona um novo livro"""
        dados = self.obter_dados_formulario()
        
        if not dados['título'] or not dados['isbn']:
            messagebox.showwarning("Atenção", "Título e ISBN são obrigatórios!")
            return
        
        try:
            quantidade = int(dados['quantidade'])
            if quantidade < 0:
                messagebox.showwarning("Atenção", "Quantidade não pode ser negativa!")
                return
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade deve ser um número!")
            return
        
        isbn = dados['isbn']
        if isbn in self.app.livros:
            resposta = messagebox.askyesno(
                "Livro Existente",
                f"Já existe livro com ISBN {isbn}.\nDeseja adicionar {quantidade} unidades ao estoque?"
            )
            if resposta:
                self.app.livros[isbn]['quantidade'] += quantidade
                self.app.salvar_dados(self.app.livros, self.app.arquivo_livros)
                self.atualizar_lista_livros()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", f"Quantidade atualizada: {self.app.livros[isbn]['quantidade']}")
            return
        
        self.app.livros[isbn] = {
            'título': dados['título'],
            'autor': dados['autor'],
            'gênero': dados['gênero'],
            'quantidade': quantidade
        }
        
        self.app.salvar_dados(self.app.livros, self.app.arquivo_livros)
        self.atualizar_lista_livros()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Livro adicionado!")
    
    def editar_livro(self):
        """Edita um livro existente"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro!")
            return
        
        item = self.treeview.item(selecionado[0])
        # Converter para string para garantir compatibilidade
        isbn_atual = str(item['values'][2])
        dados = self.obter_dados_formulario()
        novo_isbn = dados['isbn']
        
        if not dados['título']:
            messagebox.showwarning("Atenção", "Título é obrigatório!")
            return
        
        try:
            quantidade = int(dados['quantidade'])
            if quantidade < 0:
                messagebox.showwarning("Atenção", "Quantidade não pode ser negativa!")
                return
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade deve ser um número!")
            return
        
        if novo_isbn != isbn_atual and novo_isbn in self.app.livros:
            messagebox.showwarning("Atenção", f"Já existe livro com ISBN {novo_isbn}!")
            return
        
        if novo_isbn != isbn_atual:
            livro_antigo = self.app.livros.pop(isbn_atual)
            livro_antigo.update({
                'título': dados['título'],
                'autor': dados['autor'],
                'gênero': dados['gênero'],
                'quantidade': quantidade
            })
            self.app.livros[novo_isbn] = livro_antigo
        else:
            self.app.livros[isbn_atual] = {
                'título': dados['título'],
                'autor': dados['autor'],
                'gênero': dados['gênero'],
                'quantidade': quantidade
            }
        
        self.app.salvar_dados(self.app.livros, self.app.arquivo_livros)
        self.atualizar_lista_livros()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Livro editado!")
    
    def excluir_livro(self):
        """Exclui um livro"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um livro!")
            return
        
        item = self.treeview.item(selecionado[0])
        titulo = item['values'][0]
        # Converter explicitamente para string para evitar erro de chave (int vs str)
        isbn = str(item['values'][2])
        
        livro_emprestado = any(
            emp.get('isbn_livro') == isbn and emp.get('status') == 'ativo'
            for emp in self.app.emprestimos.values()
        )
        
        if livro_emprestado:
            messagebox.showwarning("Atenção", f"O livro '{titulo}' está emprestado!")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar",
            f"Excluir o livro '{titulo}' (ISBN: {isbn})?"
        )
        
        if resposta:
            if isbn in self.app.livros:
                del self.app.livros[isbn]
                self.app.salvar_dados(self.app.livros, self.app.arquivo_livros)
                self.atualizar_lista_livros()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Livro excluído!")
            else:
                messagebox.showerror("Erro", "Erro ao localizar o livro no sistema.")
    
    def verificar_livro(self):
        """Verifica se livro existe"""
        isbn = self.entries['isbn'].get().strip()
        
        if not isbn:
            messagebox.showwarning("Atenção", "Digite um ISBN!")
            return
        
        if isbn in self.app.livros:
            livro = self.app.livros[isbn]
            emprestado = any(
                emp.get('isbn_livro') == isbn and emp.get('status') == 'ativo'
                for emp in self.app.emprestimos.values()
            )
            
            status = "Disponível" if not emprestado else "Emprestado"
            messagebox.showinfo(
                "Livro Encontrado",
                f"✅ Livro encontrado!\n\n"
                f"Título: {livro.get('título', '')}\n"
                f"Autor: {livro.get('autor', '')}\n"
                f"Status: {status}"
            )
        else:
            messagebox.showinfo(
                "Livro Não Encontrado",
                f"❌ Não existe livro com ISBN {isbn}"
            )
    
    def selecionar_livro(self, event):
        """Preenche formulário com livro selecionado"""
        selecionado = self.treeview.selection()
        if not selecionado:
            return
        
        item = self.treeview.item(selecionado[0])
        valores = item['values']
        
        self.entries['título'].delete(0, tk.END)
        self.entries['título'].insert(0, valores[0])
        
        self.entries['autor'].delete(0, tk.END)
        self.entries['autor'].insert(0, valores[1])
        
        self.entries['isbn'].delete(0, tk.END)
        self.entries['isbn'].insert(0, valores[2])
        
        self.entries['gênero'].delete(0, tk.END)
        self.entries['gênero'].insert(0, valores[3])
        
        self.entries['quantidade'].delete(0, tk.END)
        self.entries['quantidade'].insert(0, valores[4])
    
    def limpar_campos(self):
        """Limpa os campos do formulário"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def obter_dados_formulario(self):
        """Obtém dados do formulário"""
        return {
            'título': self.entries['título'].get().strip(),
            'autor': self.entries['autor'].get().strip(),
            'isbn': self.entries['isbn'].get().strip(),
            'gênero': self.entries['gênero'].get().strip(),
            'quantidade': self.entries['quantidade'].get().strip() or "0"
        }
    
    def atualizar_lista_livros(self):
        """Atualiza a lista de livros"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        livros_ordenados = sorted(
            self.app.livros.items(),
            key=lambda x: x[1].get('título', '').lower()
        )
        
        for isbn, livro in livros_ordenados:
            self.treeview.insert("", tk.END, values=(
                livro.get('título', ''),
                livro.get('autor', ''),
                isbn,
                livro.get('gênero', ''),
                livro.get('quantidade', 0)
            ))


class TelaUsuarios:
    """Classe para a tela de cadastro de usuários"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
        self.atualizar_lista_usuarios()
    
    def criar_widgets(self):
        """Cria a interface da tela de usuários"""
        titulo = ttk.Label(
            self.frame,
            text="👥 Controle de Usuários",
            font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        frame_form = ttk.LabelFrame(self.frame, text="Dados do Usuário", padding="15")
        frame_form.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        campos = [("Nome:", 0), ("ID:", 1)]
        self.entries = {}
        
        for i, (texto, linha) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=linha, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame_form, width=40)
            entry.grid(row=linha, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            self.entries[texto.replace(":", "").lower()] = entry
        
        ttk.Label(frame_form, text="Tipo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.combo_tipo = ttk.Combobox(frame_form, 
                                      values=["Aluno", "Professor", "Funcionário", "Visitante"], 
                                      width=37)
        self.combo_tipo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.combo_tipo.set("Aluno")
        
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_usuario).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Editar", command=self.editar_usuario).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_usuario).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos).grid(row=0, column=3, padx=5)
        ttk.Button(frame_botoes, text="Ver Histórico", command=self.ver_historico).grid(row=0, column=4, padx=5)
        
        frame_lista = ttk.LabelFrame(self.frame, text="Usuários Cadastrados", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("id", "nome", "tipo", "emprestimos_ativos")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15)
        
        self.treeview.heading("id", text="ID")
        self.treeview.heading("nome", text="Nome")
        self.treeview.heading("tipo", text="Tipo")
        self.treeview.heading("emprestimos_ativos", text="Empréstimos Ativos")
        
        self.treeview.column("id", width=100)
        self.treeview.column("nome", width=250)
        self.treeview.column("tipo", width=120)
        self.treeview.column("emprestimos_ativos", width=120)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.treeview.bind("<<TreeviewSelect>>", self.selecionar_usuario)
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="📊 Ver Relatórios", 
                  command=self.app.abrir_tela_relatorios).grid(row=0, column=1, padx=5)
    
    def adicionar_usuario(self):
        """Adiciona novo usuário"""
        nome = self.entries['nome'].get().strip()
        id_usuario = self.entries['id'].get().strip()
        tipo = self.combo_tipo.get()
        
        if not nome or not id_usuario:
            messagebox.showwarning("Atenção", "Nome e ID são obrigatórios!")
            return
        
        if id_usuario in self.app.usuarios:
            messagebox.showwarning("Atenção", f"Já existe usuário com ID {id_usuario}!")
            return
        
        self.app.usuarios[id_usuario] = {
            'nome': nome,
            'tipo': tipo,
            'data_cadastro': datetime.now().strftime("%Y-%m-%d"),
            'historico': []
        }
        
        self.app.salvar_dados(self.app.usuarios, self.app.arquivo_usuarios)
        self.atualizar_lista_usuarios()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado!")
    
    def editar_usuario(self):
        """Edita usuário existente"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário!")
            return
        
        item = self.treeview.item(selecionado[0])
        # Converter ID para string para evitar problemas de compatibilidade
        id_atual = str(item['values'][0])
        
        nome = self.entries['nome'].get().strip()
        novo_id = self.entries['id'].get().strip()
        tipo = self.combo_tipo.get()
        
        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório!")
            return
        
        if novo_id != id_atual and novo_id in self.app.usuarios:
            messagebox.showwarning("Atenção", f"Já existe usuário com ID {novo_id}!")
            return
        
        if novo_id != id_atual:
            usuario_data = self.app.usuarios.pop(id_atual)
            usuario_data.update({'nome': nome, 'tipo': tipo})
            self.app.usuarios[novo_id] = usuario_data
            
            for emp in self.app.emprestimos.values():
                if str(emp.get('id_usuario')) == id_atual:
                    emp['id_usuario'] = novo_id
            self.app.salvar_dados(self.app.emprestimos, self.app.arquivo_emprestimos)
        else:
            self.app.usuarios[id_atual].update({'nome': nome, 'tipo': tipo})
        
        self.app.salvar_dados(self.app.usuarios, self.app.arquivo_usuarios)
        self.atualizar_lista_usuarios()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Usuário editado!")
    
    def excluir_usuario(self):
        """Exclui usuário"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário!")
            return
        
        item = self.treeview.item(selecionado[0])
        # Converter explicitamente para string para evitar erro de chave (int vs str)
        id_usuario = str(item['values'][0])
        nome = item['values'][1]
        
        emprestimos_ativos = any(
            str(emp.get('id_usuario')) == id_usuario and emp.get('status') == 'ativo'
            for emp in self.app.emprestimos.values()
        )
        
        if emprestimos_ativos:
            messagebox.showwarning("Atenção", f"Usuário '{nome}' tem empréstimos ativos!")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar",
            f"Excluir usuário '{nome}' (ID: {id_usuario})?"
        )
        
        if resposta:
            if id_usuario in self.app.usuarios:
                del self.app.usuarios[id_usuario]
                self.app.salvar_dados(self.app.usuarios, self.app.arquivo_usuarios)
                self.atualizar_lista_usuarios()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Usuário excluído!")
            else:
                messagebox.showerror("Erro", "Erro ao localizar o usuário no sistema.")
    
    def ver_historico(self):
        """Exibe histórico do usuário"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário!")
            return
        
        item = self.treeview.item(selecionado[0])
        id_usuario = str(item['values'][0])
        nome = item['values'][1]
        
        emprestimos_usuario = [
            emp for emp in self.app.emprestimos.values()
            if str(emp.get('id_usuario')) == id_usuario
        ]
        
        if not emprestimos_usuario:
            messagebox.showinfo("Histórico", f"Usuário '{nome}' não tem histórico.")
            return
        
        historico = f"📋 HISTÓRICO - {nome}\n\n"
        for emp in emprestimos_usuario:
            livro = self.app.livros.get(emp.get('isbn_livro', ''), {})
            status = "✅ Devolvido" if emp.get('status') == 'devolvido' else "🔄 Emprestado"
            
            historico += f"Livro: {livro.get('título', '')}\n"
            historico += f"Data: {emp.get('data_emprestimo', '')}\n"
            historico += f"Status: {status}\n"
            historico += "-" * 40 + "\n"
        
        messagebox.showinfo(f"Histórico - {nome}", historico)
    
    def selecionar_usuario(self, event):
        """Preenche formulário com usuário selecionado"""
        selecionado = self.treeview.selection()
        if not selecionado:
            return
        
        item = self.treeview.item(selecionado[0])
        valores = item['values']
        
        self.entries['nome'].delete(0, tk.END)
        self.entries['nome'].insert(0, valores[1])
        
        self.entries['id'].delete(0, tk.END)
        self.entries['id'].insert(0, valores[0])
        
        self.combo_tipo.set(valores[2])
    
    def limpar_campos(self):
        """Limpa os campos do formulário"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.combo_tipo.set("Aluno")
    
    def atualizar_lista_usuarios(self):
        """Atualiza lista de usuários"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        emprestimos_ativos = {}
        for emp in self.app.emprestimos.values():
            if emp.get('status') == 'ativo':
                usuario_id = str(emp.get('id_usuario', ''))
                if usuario_id:
                    emprestimos_ativos[usuario_id] = emprestimos_ativos.get(usuario_id, 0) + 1
        
        usuarios_ordenados = sorted(
            self.app.usuarios.items(),
            key=lambda x: x[1].get('nome', '').lower()
        )
        
        for usuario_id, usuario in usuarios_ordenados:
            qtd_ativos = emprestimos_ativos.get(str(usuario_id), 0)
            self.treeview.insert("", tk.END, values=(
                usuario_id,
                usuario.get('nome', ''),
                usuario.get('tipo', ''),
                qtd_ativos
            ))


class TelaNovoEmprestimo:
    """Classe para tela de novo empréstimo"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
        self.atualizar_comboboxes()
    
    def criar_widgets(self):
        """Cria a interface da tela de novo empréstimo"""
        titulo = ttk.Label(
            self.frame,
            text="🔄 Novo Empréstimo",
            font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        frame_form = ttk.LabelFrame(self.frame, text="Dados do Empréstimo", padding="15")
        frame_form.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Usuário
        ttk.Label(frame_form, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
        frame_usuario = ttk.Frame(frame_form)
        frame_usuario.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        self.combo_usuario = ttk.Combobox(frame_usuario, width=30)
        self.combo_usuario.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(frame_usuario, text="Carregar", 
                  command=self.carregar_dados_usuario).grid(row=0, column=1, padx=(10, 0))
        
        self.frame_dados_usuario = ttk.Frame(frame_form)
        self.frame_dados_usuario.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_nome = ttk.Label(self.frame_dados_usuario, text="Nome: ")
        self.label_nome.grid(row=0, column=0, sticky=tk.W)
        self.label_tipo = ttk.Label(self.frame_dados_usuario, text="Tipo: ")
        self.label_tipo.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Livro
        ttk.Label(frame_form, text="Livro (ISBN):").grid(row=2, column=0, sticky=tk.W, pady=5)
        frame_livro = ttk.Frame(frame_form)
        frame_livro.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        self.combo_livro = ttk.Combobox(frame_livro, width=30)
        self.combo_livro.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(frame_livro, text="Carregar", 
                  command=self.carregar_dados_livro).grid(row=0, column=1, padx=(10, 0))
        
        self.frame_dados_livro = ttk.Frame(frame_form)
        self.frame_dados_livro.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_titulo = ttk.Label(self.frame_dados_livro, text="Título: ")
        self.label_titulo.grid(row=0, column=0, sticky=tk.W)
        self.label_autor = ttk.Label(self.frame_dados_livro, text="Autor: ")
        self.label_autor.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        self.label_quantidade = ttk.Label(self.frame_dados_livro, text="Disponíveis: ")
        self.label_quantidade.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Prazo
        ttk.Label(frame_form, text="Prazo (dias):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_prazo = ttk.Entry(frame_form, width=10)
        self.entry_prazo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.entry_prazo.insert(0, "7")
        
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(frame_botoes, text="Realizar Empréstimo", 
                  command=self.realizar_emprestimo, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Limpar", 
                  command=self.limpar_campos).grid(row=0, column=1, padx=5)
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="📋 Gerenciar Empréstimos", 
                  command=self.app.abrir_gerenciar_emprestimos).grid(row=0, column=1, padx=5)
    
    def atualizar_comboboxes(self):
        """Atualiza as comboboxes"""
        # Usuários
        nomes_usuarios = [
            f"{user_id} - {self.app.usuarios[user_id].get('nome', '')}"
            for user_id in self.app.usuarios.keys()
        ]
        self.combo_usuario['values'] = nomes_usuarios
        
        # Livros disponíveis
        livros_info = []
        for isbn, livro in self.app.livros.items():
            if livro.get('quantidade', 0) > 0:
                livros_info.append(f"{isbn} - {livro.get('título', '')}")
        
        self.combo_livro['values'] = livros_info
    
    def carregar_dados_usuario(self):
        """Carrega dados do usuário selecionado"""
        selecao = self.combo_usuario.get()
        if not selecao:
            return
        
        try:
            user_id = selecao.split(" - ")[0]
        except IndexError:
            return
        
        if user_id in self.app.usuarios:
            usuario = self.app.usuarios[user_id]
            self.label_nome.config(text=f"Nome: {usuario.get('nome', '')}")
            self.label_tipo.config(text=f"Tipo: {usuario.get('tipo', '')}")
    
    def carregar_dados_livro(self):
        """Carrega dados do livro selecionado"""
        selecao = self.combo_livro.get()
        if not selecao:
            return
        
        try:
            isbn = selecao.split(" - ")[0]
        except IndexError:
            return
        
        if isbn in self.app.livros:
            livro = self.app.livros[isbn]
            self.label_titulo.config(text=f"Título: {livro.get('título', '')}")
            self.label_autor.config(text=f"Autor: {livro.get('autor', '')}")
            self.label_quantidade.config(text=f"Disponíveis: {livro.get('quantidade', 0)}")
    
    def realizar_emprestimo(self):
        """Realiza o empréstimo"""
        selecao_usuario = self.combo_usuario.get()
        if not selecao_usuario:
            messagebox.showwarning("Atenção", "Selecione um usuário!")
            return
        
        try:
            user_id = selecao_usuario.split(" - ")[0]
        except IndexError:
            messagebox.showwarning("Atenção", "Selecione um usuário válido!")
            return
        
        selecao_livro = self.combo_livro.get()
        if not selecao_livro:
            messagebox.showwarning("Atenção", "Selecione um livro!")
            return
        
        try:
            isbn = selecao_livro.split(" - ")[0]
        except IndexError:
            messagebox.showwarning("Atenção", "Selecione um livro válido!")
            return
        
        try:
            prazo_dias = int(self.entry_prazo.get())
            if prazo_dias <= 0:
                messagebox.showwarning("Atenção", "Prazo deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showwarning("Atenção", "Prazo deve ser um número!")
            return
        
        if user_id not in self.app.usuarios:
            messagebox.showwarning("Atenção", "Usuário não encontrado!")
            return
        
        if isbn not in self.app.livros:
            messagebox.showwarning("Atenção", "Livro não encontrado!")
            return
        
        livro = self.app.livros[isbn]
        if livro.get('quantidade', 0) <= 0:
            messagebox.showwarning("Atenção", "Livro não disponível!")
            return
        
        emprestimos_ativos = sum(
            1 for emp in self.app.emprestimos.values()
            if emp.get('id_usuario') == user_id and emp.get('status') == 'ativo'
        )
        
        if emprestimos_ativos >= 3:
            messagebox.showwarning("Atenção", 
                f"Usuário já tem {emprestimos_ativos} empréstimos ativos!")
            return
        
        emprestimo_id = self.app.gerar_id_unico("EMP")
        data_emprestimo = datetime.now().strftime("%Y-%m-%d")
        data_devolucao = (datetime.now() + timedelta(days=prazo_dias)).strftime("%Y-%m-%d")
        
        self.app.emprestimos[emprestimo_id] = {
            'id_usuario': user_id,
            'isbn_livro': isbn,
            'data_emprestimo': data_emprestimo,
            'data_devolucao_prevista': data_devolucao,
            'status': 'ativo',
            'multa': 0.00
        }
        
        self.app.livros[isbn]['quantidade'] -= 1
        
        if 'historico' not in self.app.usuarios[user_id]:
            self.app.usuarios[user_id]['historico'] = []
        self.app.usuarios[user_id]['historico'].append(emprestimo_id)
        
        if not self.app.salvar_todos_dados():
            messagebox.showerror("Erro", "Não foi possível salvar!")
            return
        
        self.limpar_campos()
        self.atualizar_comboboxes()
        
        messagebox.showinfo("Sucesso", 
            f"Empréstimo realizado!\n\n"
            f"Código: {emprestimo_id}\n"
            f"Data Devolução: {data_devolucao}")
    
    def limpar_campos(self):
        """Limpa os campos"""
        self.combo_usuario.set('')
        self.combo_livro.set('')
        self.entry_prazo.delete(0, tk.END)
        self.entry_prazo.insert(0, "7")
        
        self.label_nome.config(text="Nome: ")
        self.label_tipo.config(text="Tipo: ")
        self.label_titulo.config(text="Título: ")
        self.label_autor.config(text="Autor: ")
        self.label_quantidade.config(text="Disponíveis: ")


class TelaGerenciarEmprestimos:
    """Classe para tela de gerenciar empréstimos"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
        self.atualizar_lista_emprestimos()
    
    def criar_widgets(self):
        """Cria a interface da tela"""
        titulo = ttk.Label(
            self.frame,
            text="📋 Gerenciar Empréstimos",
            font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        frame_filtros = ttk.LabelFrame(self.frame, text="Filtros", padding="10")
        frame_filtros.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_filtros, text="Status:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.combo_filtro = ttk.Combobox(frame_filtros, 
                                        values=["Todos", "Ativos", "Devolvidos"], 
                                        width=15, state="readonly")
        self.combo_filtro.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.combo_filtro.set("Ativos")
        
        ttk.Button(frame_filtros, text="Aplicar Filtro", 
                  command=self.atualizar_lista_emprestimos).grid(row=0, column=2, padx=10)
        ttk.Button(frame_filtros, text="Limpar Filtro", 
                  command=self.limpar_filtro).grid(row=0, column=3, padx=10)
        
        frame_lista = ttk.LabelFrame(self.frame, text="Empréstimos", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("id", "usuario", "livro", "data_emp", "data_dev", "status", "multa")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15)
        
        self.treeview.heading("id", text="ID Empréstimo")
        self.treeview.heading("usuario", text="Usuário")
        self.treeview.heading("livro", text="Livro")
        self.treeview.heading("data_emp", text="Data Empréstimo")
        self.treeview.heading("data_dev", text="Data Devolução")
        self.treeview.heading("status", text="Status")
        self.treeview.heading("multa", text="Multa (Kz)")
        
        self.treeview.column("id", width=100)
        self.treeview.column("usuario", width=150)
        self.treeview.column("livro", width=200)
        self.treeview.column("data_emp", width=100)
        self.treeview.column("data_dev", width=100)
        self.treeview.column("status", width=80)
        self.treeview.column("multa", width=80)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        frame_acoes = ttk.Frame(self.frame)
        frame_acoes.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(frame_acoes, text="Registrar Devolução", 
                  command=self.registrar_devolucao, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(frame_acoes, text="Calcular Multa", 
                  command=self.calcular_multa, width=20).grid(row=0, column=1, padx=5)
        ttk.Button(frame_acoes, text="Ver Detalhes", 
                  command=self.ver_detalhes, width=20).grid(row=0, column=2, padx=5)
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=4, column=0, columnspan=4, pady=(20, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="🔄 Novo Empréstimo", 
                  command=self.app.abrir_novo_emprestimo).grid(row=0, column=1, padx=5)
    
    def atualizar_lista_emprestimos(self):
        """Atualiza lista de empréstimos"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        filtro = self.combo_filtro.get()
        
        for emp_id, emprestimo in self.app.emprestimos.items():
            if filtro == "Ativos" and emprestimo.get('status') != 'ativo':
                continue
            elif filtro == "Devolvidos" and emprestimo.get('status') != 'devolvido':
                continue
            
            usuario = self.app.usuarios.get(emprestimo.get('id_usuario', ''), {})
            livro = self.app.livros.get(emprestimo.get('isbn_livro', ''), {})
            
            status = "🔄 Ativo" if emprestimo.get('status') == 'ativo' else "✅ Devolvido"
            multa = f"{emprestimo.get('multa', 0.00):.2f}"
            
            self.treeview.insert("", tk.END, values=(
                emp_id,
                usuario.get('nome', 'Desconhecido'),
                livro.get('título', 'Desconhecido'),
                emprestimo.get('data_emprestimo', ''),
                emprestimo.get('data_devolucao_prevista', ''),
                status,
                multa
            ))
    
    def limpar_filtro(self):
        """Limpa filtro"""
        self.combo_filtro.set("Todos")
        self.atualizar_lista_emprestimos()
    
    def registrar_devolucao(self):
        """Registra devolução"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um empréstimo!")
            return
        
        item = self.treeview.item(selecionado[0])
        emp_id = item['values'][0]
        
        if emp_id not in self.app.emprestimos:
            messagebox.showerror("Erro", "Empréstimo não encontrado!")
            return
        
        emprestimo = self.app.emprestimos[emp_id]
        
        if emprestimo.get('status') == 'devolvido':
            messagebox.showwarning("Atenção", "Este empréstimo já foi devolvido!")
            return
        
        multa = self.app.calcular_multa(emprestimo.get('data_devolucao_prevista', ''))
        
        emprestimo['status'] = 'devolvido'
        emprestimo['data_devolucao_real'] = datetime.now().strftime("%Y-%m-%d")
        emprestimo['multa'] = multa
        
        isbn = emprestimo.get('isbn_livro', '')
        if isbn in self.app.livros:
            self.app.livros[isbn]['quantidade'] += 1
        
        if not self.app.salvar_todos_dados():
            messagebox.showerror("Erro", "Não foi possível salvar!")
            return
        
        self.atualizar_lista_emprestimos()
        
        if multa > 0:
            messagebox.showinfo("Sucesso", 
                f"Devolução registrada!\nMulta: {multa:.2f} Kz")
        else:
            messagebox.showinfo("Sucesso", "Devolução registrada!")
    
    def calcular_multa(self):
        """Calcula multa"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um empréstimo!")
            return
        
        item = self.treeview.item(selecionado[0])
        emp_id = item['values'][0]
        
        if emp_id not in self.app.emprestimos:
            messagebox.showerror("Erro", "Empréstimo não encontrado!")
            return
        
        emprestimo = self.app.emprestimos[emp_id]
        
        if emprestimo.get('status') == 'devolvido':
            multa = emprestimo.get('multa', 0.00)
            messagebox.showinfo("Multa", f"Multa paga: {multa:.2f} Kz")
        else:
            multa = self.app.calcular_multa(emprestimo.get('data_devolucao_prevista', ''))
            if multa > 0:
                messagebox.showwarning("Multa Pendente", 
                    f"Multa a pagar: {multa:.2f} Kz\n500 Kz por dia de atraso")
            else:
                messagebox.showinfo("Sem Multa", "Não há multa pendente.")
    
    def ver_detalhes(self):
        """Exibe detalhes do empréstimo"""
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um empréstimo!")
            return
        
        item = self.treeview.item(selecionado[0])
        emp_id = item['values'][0]
        
        if emp_id not in self.app.emprestimos:
            messagebox.showerror("Erro", "Empréstimo não encontrado!")
            return
        
        emprestimo = self.app.emprestimos[emp_id]
        usuario = self.app.usuarios.get(emprestimo.get('id_usuario', ''), {})
        livro = self.app.livros.get(emprestimo.get('isbn_livro', ''), {})
        
        detalhes = f"📋 DETALHES DO EMPRÉSTIMO\n\n"
        detalhes += f"ID: {emp_id}\n"
        detalhes += f"Usuário: {usuario.get('nome', 'Desconhecido')}\n"
        detalhes += f"Tipo: {usuario.get('tipo', 'Desconhecido')}\n"
        detalhes += f"Livro: {livro.get('título', 'Desconhecido')}\n"
        detalhes += f"ISBN: {emprestimo.get('isbn_livro', '')}\n"
        detalhes += f"Data Empréstimo: {emprestimo.get('data_emprestimo', '')}\n"
        detalhes += f"Data Devolução Prevista: {emprestimo.get('data_devolucao_prevista', '')}\n"
        detalhes += f"Status: {'🔄 Ativo' if emprestimo.get('status') == 'ativo' else '✅ Devolvido'}\n"
        
        if emprestimo.get('status') == 'devolvido':
            detalhes += f"Data Devolução Real: {emprestimo.get('data_devolucao_real', 'N/A')}\n"
            detalhes += f"Multa Paga: {emprestimo.get('multa', 0.00):.2f} Kz\n"
        else:
            multa_pendente = self.app.calcular_multa(emprestimo.get('data_devolucao_prevista', ''))
            if multa_pendente > 0:
                detalhes += f"Multa Pendente: {multa_pendente:.2f} Kz\n"
        
        messagebox.showinfo(f"Detalhes - {emp_id}", detalhes)


class TelaConsultaEstoque:
    """Classe para a tela de consulta e estoque de livros"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.criar_widgets()
        self.atualizar_lista_livros()
    
    def criar_widgets(self):
        """Cria a interface da tela de consulta"""
        titulo = ttk.Label(
            self.frame,
            text="🔍 Consulta de Livros / Estoque",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        frame_filtros = ttk.LabelFrame(self.frame, text="Filtros de Consulta", padding="15")
        frame_filtros.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(frame_filtros, text="Disponibilidade:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filtro_disponibilidade = ttk.Combobox(frame_filtros, 
                                                  values=["Todos", "Disponíveis", "Indisponíveis"], 
                                                  width=15, state="readonly")
        self.filtro_disponibilidade.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.filtro_disponibilidade.set("Todos")
        
        ttk.Label(frame_filtros, text="Gênero:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        generos = sorted(set(livro.get('gênero', '') for livro in self.app.livros.values() if livro.get('gênero')))
        generos.insert(0, "Todos")
        
        self.filtro_genero = ttk.Combobox(frame_filtros, values=generos, width=15, state="readonly")
        self.filtro_genero.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        self.filtro_genero.set("Todos")
        
        ttk.Button(frame_filtros, text="Aplicar Filtros", 
                  command=self.atualizar_lista_livros).grid(row=0, column=4, padx=10)
        ttk.Button(frame_filtros, text="Limpar Filtros", 
                  command=self.limpar_filtros).grid(row=0, column=5, padx=10)
        ttk.Button(frame_filtros, text="Exportar Lista", 
                  command=self.exportar_lista).grid(row=0, column=6, padx=10)
        
        frame_lista = ttk.LabelFrame(self.frame, text="📚 Catálogo de Livros", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("título", "autor", "isbn", "gênero", "quantidade", "disponivel", "status")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=20)
        
        self.treeview.heading("título", text="Título")
        self.treeview.heading("autor", text="Autor")
        self.treeview.heading("isbn", text="ISBN")
        self.treeview.heading("gênero", text="Gênero")
        self.treeview.heading("quantidade", text="Quantidade")
        self.treeview.heading("disponivel", text="Disponível")
        self.treeview.heading("status", text="Status")
        
        self.treeview.column("título", width=250)
        self.treeview.column("autor", width=150)
        self.treeview.column("isbn", width=120)
        self.treeview.column("gênero", width=100)
        self.treeview.column("quantidade", width=80)
        self.treeview.column("disponivel", width=80)
        self.treeview.column("status", width=100)
        
        vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=self.treeview.yview)
        hsb = ttk.Scrollbar(frame_lista, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        
        frame_stats = ttk.Frame(self.frame)
        frame_stats.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.label_total = ttk.Label(frame_stats, text="Total: 0 livros")
        self.label_total.grid(row=0, column=0, padx=(0, 20))
        
        self.label_disponiveis = ttk.Label(frame_stats, text="Disponíveis: 0")
        self.label_disponiveis.grid(row=0, column=1, padx=(0, 20))
        
        self.label_emprestados = ttk.Label(frame_stats, text="Emprestados: 0")
        self.label_emprestados.grid(row=0, column=2, padx=(0, 20))
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="🔎 Buscar Livro", 
                  command=self.app.abrir_busca_livros, width=20).grid(row=0, column=1, padx=5)
        ttk.Button(frame_navegacao, text="📊 Ver Relatórios", 
                  command=self.app.abrir_tela_relatorios, width=20).grid(row=0, column=2, padx=5)
    
    def atualizar_lista_livros(self):
        """Atualiza a lista de livros com filtros aplicados"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        filtro_disp = self.filtro_disponibilidade.get()
        filtro_gen = self.filtro_genero.get()
        
        total = 0
        disponiveis = 0
        emprestados = 0
        
        for isbn, livro in self.app.livros.items():
            if filtro_gen != "Todos" and livro.get('gênero', '') != filtro_gen:
                continue
            
            qtd_total = livro.get('quantidade', 0)
            qtd_emprestada = sum(
                1 for emp in self.app.emprestimos.values()
                if emp.get('isbn_livro') == isbn and emp.get('status') == 'ativo'
            )
            qtd_disponivel = qtd_total - qtd_emprestada
            
            if filtro_disp == "Disponíveis" and qtd_disponivel <= 0:
                continue
            elif filtro_disp == "Indisponíveis" and qtd_disponivel > 0:
                continue
            
            total += 1
            if qtd_disponivel > 0:
                disponiveis += 1
            if qtd_emprestada > 0:
                emprestados += 1
            
            if qtd_disponivel <= 0:
                status = "❌ Indisponível"
            elif qtd_disponivel == qtd_total:
                status = "✅ Disponível"
            else:
                status = f"⚠️ {qtd_disponivel}/{qtd_total} disp."
            
            self.treeview.insert("", tk.END, values=(
                livro.get('título', ''),
                livro.get('autor', ''),
                isbn,
                livro.get('gênero', ''),
                qtd_total,
                qtd_disponivel,
                status
            ))
        
        self.label_total.config(text=f"Total: {total} livros")
        self.label_disponiveis.config(text=f"Disponíveis: {disponiveis}")
        self.label_emprestados.config(text=f"Emprestados: {emprestados}")
    
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.filtro_disponibilidade.set("Todos")
        self.filtro_genero.set("Todos")
        self.atualizar_lista_livros()
    
    def exportar_lista(self):
        """Exporta a lista de livros para arquivo de texto"""
        try:
            with open("catalogo_livros.txt", "w", encoding='utf-8') as f:
                f.write("CATÁLOGO DE LIVROS - BIBLIOTECA ISCAT\n")
                f.write("=" * 60 + "\n\n")
                
                for item in self.treeview.get_children():
                    valores = self.treeview.item(item)['values']
                    f.write(f"Título: {valores[0]}\n")
                    f.write(f"Autor: {valores[1]}\n")
                    f.write(f"ISBN: {valores[2]}\n")
                    f.write(f"Gênero: {valores[3]}\n")
                    f.write(f"Quantidade Total: {valores[4]}\n")
                    f.write(f"Disponível: {valores[5]}\n")
                    f.write(f"Status: {valores[6]}\n")
                    f.write("-" * 60 + "\n")
                
                f.write(f"\nTotal de livros listados: {len(self.treeview.get_children())}\n")
            
            messagebox.showinfo("Exportação", "Catálogo exportado para 'catalogo_livros.txt'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")


class TelaEstoque:
    """Classe para tela de visualização de estoque"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.criar_widgets()
        self.atualizar_estoque()
    
    def criar_widgets(self):
        """Cria a interface da tela de estoque"""
        titulo = ttk.Label(
            self.frame,
            text="📦 Situação do Estoque",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        frame_principal = ttk.Frame(self.frame)
        frame_principal.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        frame_stats = ttk.LabelFrame(frame_principal, text="📊 Estatísticas do Estoque", padding="15")
        frame_stats.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        total_livros = sum(livro.get('quantidade', 0) for livro in self.app.livros.values())
        livros_unicos = len(self.app.livros)
        
        disponiveis_total = 0
        emprestados_total = 0
        
        for isbn, livro in self.app.livros.items():
            qtd_total = livro.get('quantidade', 0)
            qtd_emprestada = sum(
                1 for emp in self.app.emprestimos.values()
                if emp.get('isbn_livro') == isbn and emp.get('status') == 'ativo'
            )
            disponiveis_total += (qtd_total - qtd_emprestada)
            emprestados_total += qtd_emprestada
        
        stats = [
            ("📚 Total de Livros", f"{total_livros} unidades"),
            ("📖 Títulos Diferentes", f"{livros_unicos} títulos"),
            ("✅ Livros Disponíveis", f"{disponiveis_total} unidades"),
            ("🔄 Livros Emprestados", f"{emprestados_total} unidades"),
            ("📈 Taxa de Uso", f"{(emprestados_total/total_livros*100 if total_livros > 0 else 0):.1f}%"),
            ("⚠️ Baixo Estoque", self.contar_baixo_estoque())
        ]
        
        for i, (label, valor) in enumerate(stats):
            ttk.Label(frame_stats, text=label, font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky=tk.W, pady=5)
            ttk.Label(frame_stats, text=valor, font=("Arial", 10)).grid(
                row=i, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        frame_alerta = ttk.LabelFrame(frame_principal, text="⚠️ Atenção - Baixo Estoque", padding="15")
        frame_alerta.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.lista_baixo_estoque = tk.Text(frame_alerta, width=40, height=10, font=("Arial", 9))
        self.lista_baixo_estoque.grid(row=0, column=0, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_alerta, command=self.lista_baixo_estoque.yview)
        self.lista_baixo_estoque.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame_generos = ttk.LabelFrame(self.frame, text="📈 Distribuição por Gênero", padding="15")
        frame_generos.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 10))
        
        colunas = ("genero", "quantidade", "percentual")
        self.tree_generos = ttk.Treeview(frame_generos, columns=colunas, show="headings", height=8)
        
        self.tree_generos.heading("genero", text="Gênero")
        self.tree_generos.heading("quantidade", text="Quantidade")
        self.tree_generos.heading("percentual", text="Percentual")
        
        self.tree_generos.column("genero", width=150)
        self.tree_generos.column("quantidade", width=100)
        self.tree_generos.column("percentual", width=100)
        
        self.tree_generos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_g = ttk.Scrollbar(frame_generos, orient="vertical", command=self.tree_generos.yview)
        self.tree_generos.configure(yscrollcommand=scrollbar_g.set)
        scrollbar_g.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame_generos.columnconfigure(0, weight=1)
        frame_generos.rowconfigure(0, weight=1)
        
        frame_botoes = ttk.Frame(self.frame)
        frame_botoes.grid(row=3, column=0, pady=(10, 0))
        
        ttk.Button(frame_botoes, text="🔄 Atualizar", 
                  command=self.atualizar_estoque).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="📋 Imprimir Relatório", 
                  command=self.imprimir_relatorio).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial).grid(row=0, column=2, padx=5)
    
    def contar_baixo_estoque(self):
        """Conta livros com baixo estoque (menos de 3 unidades)"""
        baixo_estoque = 0
        for livro in self.app.livros.values():
            if livro.get('quantidade', 0) < 3:
                baixo_estoque += 1
        return f"{baixo_estoque} títulos"
    
    def atualizar_estoque(self):
        """Atualiza todas as informações do estoque"""
        self.lista_baixo_estoque.delete(1.0, tk.END)
        
        for item in self.tree_generos.get_children():
            self.tree_generos.delete(item)
        
        generos = {}
        total_livros = sum(livro.get('quantidade', 0) for livro in self.app.livros.values())
        
        for livro in self.app.livros.values():
            genero = livro.get('gênero', 'Sem Gênero')
            if genero not in generos:
                generos[genero] = 0
            generos[genero] += livro.get('quantidade', 0)
        
        for genero, quantidade in sorted(generos.items(), key=lambda x: x[1], reverse=True):
            percentual = (quantidade / total_livros * 100) if total_livros > 0 else 0
            self.tree_generos.insert("", tk.END, values=(
                genero,
                quantidade,
                f"{percentual:.1f}%"
            ))
        
        livros_baixo_estoque = []
        for isbn, livro in self.app.livros.items():
            if livro.get('quantidade', 0) < 3:
                livros_baixo_estoque.append(
                    f"• {livro.get('título', '')} - {livro.get('quantidade', 0)} unidades"
                )
        
        if livros_baixo_estoque:
            self.lista_baixo_estoque.insert(1.0, "📢 ATENÇÃO: Repor estoque dos seguintes livros:\n\n")
            for livro in livros_baixo_estoque:
                self.lista_baixo_estoque.insert(tk.END, livro + "\n")
        else:
            self.lista_baixo_estoque.insert(1.0, "✅ Todos os livros têm estoque adequado!\n")
    
    def imprimir_relatorio(self):
        """Imprime relatório do estoque"""
        relatorio = "RELATÓRIO DE ESTOQUE - BIBLIOTECA ISCAT\n"
        relatorio += "=" * 50 + "\n\n"
        
        total_livros = sum(livro.get('quantidade', 0) for livro in self.app.livros.values())
        relatorio += f"Total de livros em estoque: {total_livros}\n\n"
        
        relatorio += "Distribuição por Gênero:\n"
        for item in self.tree_generos.get_children():
            valores = self.tree_generos.item(item)['values']
            relatorio += f"  {valores[0]}: {valores[1]} ({valores[2]})\n"
        
        messagebox.showinfo("Relatório de Estoque", relatorio)


class TelaBuscaLivros:
    """Classe para tela de busca de livros"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria a interface da tela de busca"""
        titulo = ttk.Label(
            self.frame,
            text="🔎 Busca Avançada de Livros",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        frame_busca = ttk.LabelFrame(self.frame, text="Critérios de Busca", padding="15")
        frame_busca.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(frame_busca, text="Termo de busca:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_busca = ttk.Entry(frame_busca, width=40)
        self.entry_busca.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        ttk.Label(frame_busca, text="Buscar por:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.tipo_busca = ttk.Combobox(frame_busca, 
                                      values=["Título", "Autor", "ISBN", "Todos os Campos"], 
                                      width=15, state="readonly")
        self.tipo_busca.grid(row=0, column=3, sticky=tk.W)
        self.tipo_busca.set("Todos os Campos")
        
        ttk.Button(frame_busca, text="🔍 Buscar", 
                  command=self.realizar_busca, width=15).grid(row=0, column=4, padx=(20, 0))
        
        frame_resultados = ttk.LabelFrame(self.frame, text="📚 Resultados da Busca", padding="10")
        frame_resultados.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("título", "autor", "isbn", "gênero", "quantidade", "disponivel", "status")
        self.treeview = ttk.Treeview(frame_resultados, columns=colunas, show="headings", height=15)
        
        self.treeview.heading("título", text="Título")
        self.treeview.heading("autor", text="Autor")
        self.treeview.heading("isbn", text="ISBN")
        self.treeview.heading("gênero", text="Gênero")
        self.treeview.heading("quantidade", text="Quantidade")
        self.treeview.heading("disponivel", text="Disponível")
        self.treeview.heading("status", text="Status")
        
        self.treeview.column("título", width=250)
        self.treeview.column("autor", width=150)
        self.treeview.column("isbn", width=120)
        self.treeview.column("gênero", width=100)
        self.treeview.column("quantidade", width=80)
        self.treeview.column("disponivel", width=80)
        self.treeview.column("status", width=100)
        
        vsb = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.treeview.yview)
        hsb = ttk.Scrollbar(frame_resultados, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.label_resultados = ttk.Label(self.frame, text="Digite um termo para buscar...")
        self.label_resultados.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="📋 Ver Estoque Completo", 
                  command=self.app.abrir_estoque, width=20).grid(row=0, column=1, padx=5)
    
    def realizar_busca(self):
        """Realiza a busca de livros"""
        termo = self.entry_busca.get().strip()
        tipo = self.tipo_busca.get()
        
        if not termo:
            messagebox.showwarning("Atenção", "Digite um termo para buscar!")
            return
        
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        resultados = []
        termo_lower = termo.lower()
        
        for isbn, livro in self.app.livros.items():
            titulo = livro.get('título', '').lower()
            autor = livro.get('autor', '').lower()
            
            if tipo == "Título" and termo_lower in titulo:
                resultados.append((isbn, livro))
            elif tipo == "Autor" and termo_lower in autor:
                resultados.append((isbn, livro))
            elif tipo == "ISBN" and termo_lower in isbn.lower():
                resultados.append((isbn, livro))
            elif tipo == "Todos os Campos" and (termo_lower in titulo or termo_lower in autor or termo_lower in isbn.lower()):
                resultados.append((isbn, livro))
        
        if resultados:
            for isbn, livro in resultados:
                qtd_total = livro.get('quantidade', 0)
                qtd_emprestada = sum(
                    1 for emp in self.app.emprestimos.values()
                    if emp.get('isbn_livro') == isbn and emp.get('status') == 'ativo'
                )
                qtd_disponivel = qtd_total - qtd_emprestada
                
                status = "✅ Disponível" if qtd_disponivel > 0 else "❌ Indisponível"
                
                self.treeview.insert("", tk.END, values=(
                    livro.get('título', ''),
                    livro.get('autor', ''),
                    isbn,
                    livro.get('gênero', ''),
                    qtd_total,
                    qtd_disponivel,
                    status
                ))
            
            self.label_resultados.config(
                text=f"✅ Encontrados {len(resultados)} livro(s) para '{termo}'"
            )
        else:
            self.label_resultados.config(
                text=f"❌ Nenhum livro encontrado para '{termo}'"
            )


class TelaHistoricoMovimentacao:
    """Classe para tela de histórico de movimentação"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        self.criar_widgets()
        self.carregar_movimentacao()
    
    def criar_widgets(self):
        """Cria a interface da tela de histórico"""
        titulo = ttk.Label(
            self.frame,
            text="📝 Histórico de Movimentação",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        frame_controles = ttk.LabelFrame(self.frame, text="Período", padding="15")
        frame_controles.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(frame_controles, text="Mostrar últimos:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.periodo = ttk.Combobox(frame_controles, 
                                   values=["7 dias", "15 dias", "30 dias", "60 dias", "Todos"], 
                                   width=10, state="readonly")
        self.periodo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.periodo.set("30 dias")
        
        ttk.Button(frame_controles, text="🔄 Atualizar", 
                  command=self.carregar_movimentacao).grid(row=0, column=2, padx=10)
        ttk.Button(frame_controles, text="📋 Exportar Histórico", 
                  command=self.exportar_historico).grid(row=0, column=3, padx=10)
        
        frame_lista = ttk.LabelFrame(self.frame, text="📊 Movimentações", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        colunas = ("data", "tipo", "usuario", "livro", "status")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=20)
        
        self.treeview.heading("data", text="Data")
        self.treeview.heading("tipo", text="Tipo")
        self.treeview.heading("usuario", text="Usuário")
        self.treeview.heading("livro", text="Livro")
        self.treeview.heading("status", text="Status")
        
        self.treeview.column("data", width=100)
        self.treeview.column("tipo", width=100)
        self.treeview.column("usuario", width=150)
        self.treeview.column("livro", width=250)
        self.treeview.column("status", width=80)
        
        vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=self.treeview.yview)
        hsb = ttk.Scrollbar(frame_lista, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        frame_stats = ttk.Frame(self.frame)
        frame_stats.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.label_total = ttk.Label(frame_stats, text="Total: 0 movimentações")
        self.label_total.grid(row=0, column=0, padx=(0, 20))
        
        self.label_emprestimos = ttk.Label(frame_stats, text="Empréstimos: 0")
        self.label_emprestimos.grid(row=0, column=1, padx=(0, 20))
        
        self.label_devolucoes = ttk.Label(frame_stats, text="Devoluções: 0")
        self.label_devolucoes.grid(row=0, column=2, padx=(0, 20))
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=4, column=0, columnspan=4, pady=(20, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="📊 Ver Outros Relatórios", 
                  command=self.app.abrir_tela_relatorios, width=20).grid(row=0, column=1, padx=5)
    
    def carregar_movimentacao(self):
        """Carrega a movimentação conforme período selecionado"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        periodo = self.periodo.get()
        if periodo == "7 dias":
            limite_dias = 7
        elif periodo == "15 dias":
            limite_dias = 15
        elif periodo == "60 dias":
            limite_dias = 60
        elif periodo == "Todos":
            limite_dias = 3650
        else:
            limite_dias = 30
        
        movimentacao = self.app.obter_movimentacao(limite_dias)
        
        total = len(movimentacao)
        emprestimos = sum(1 for m in movimentacao if m['tipo'] == 'EMPRÉSTIMO')
        devolucoes = sum(1 for m in movimentacao if m['tipo'] == 'DEVOLUÇÃO')
        
        for mov in movimentacao:
            self.treeview.insert("", tk.END, values=(
                mov['data'],
                mov['tipo'],
                mov['usuario'],
                mov['livro'],
                mov['status']
            ))
        
        self.label_total.config(text=f"Total: {total} movimentações")
        self.label_emprestimos.config(text=f"Empréstimos: {emprestimos}")
        self.label_devolucoes.config(text=f"Devoluções: {devolucoes}")
    
    def exportar_historico(self):
        """Exporta o histórico para arquivo de texto"""
        try:
            with open("historico_movimentacao.txt", "w", encoding='utf-8') as f:
                f.write("HISTÓRICO DE MOVIMENTAÇÃO - BIBLIOTECA ISCAT\n")
                f.write("=" * 70 + "\n\n")
                
                for item in self.treeview.get_children():
                    valores = self.treeview.item(item)['values']
                    f.write(f"Data: {valores[0]}\n")
                    f.write(f"Tipo: {valores[1]}\n")
                    f.write(f"Usuário: {valores[2]}\n")
                    f.write(f"Livro: {valores[3]}\n")
                    f.write(f"Status: {valores[4]}\n")
                    f.write("-" * 70 + "\n")
                
                f.write(f"\nTotal de movimentações: {len(self.treeview.get_children())}\n")
                f.write(f"Período: {self.periodo.get()}\n")
            
            messagebox.showinfo("Exportação", "Histórico exportado para 'historico_movimentacao.txt'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")


class TelaRelatorios:
    """Classe para tela central de relatórios"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria a interface da tela de relatórios"""
        titulo = ttk.Label(
            self.frame,
            text="📊 Centro de Relatórios",
            font=("Arial", 18, "bold"),
            foreground="#2c3e50"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        descricao = ttk.Label(
            self.frame,
            text="Selecione um relatório para visualizar informações detalhadas do sistema",
            font=("Arial", 10),
            foreground="#7f8c8d"
        )
        descricao.grid(row=1, column=0, columnspan=2, pady=(0, 40))
        
        frame_cards = ttk.Frame(self.frame)
        frame_cards.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        relatorios = [
            ("📚", "Livros Mais Emprestados", 
             "Top 10 livros com mais empréstimos", 
             self.app.relatorio_livros_mais_emprestados),
            
            ("📈", "Situação do Acervo", 
             "Estatísticas completas do acervo", 
             self.app.relatorio_situacao_acervo),
            
            ("📋", "Relatório Completo", 
             "Visão geral de todos os dados", 
             self.app.relatorio_completo),
            
            ("🔄", "Histórico de Movimentação", 
             "Todas as movimentações recentes", 
             self.app.abrir_historico_movimentacao),
            
            ("👥", "Usuários Ativos", 
             "Usuários com empréstimos ativos", 
             self.app.relatorio_usuarios_ativos),
            
            ("📖", "Livros Emprestados", 
             "Lista de livros atualmente emprestados", 
             self.app.relatorio_livros_emprestados)
        ]
        
        for i, (icone, titulo_card, descricao_card, comando) in enumerate(relatorios):
            row = i // 2
            col = (i % 2) * 2
            
            card = ttk.LabelFrame(frame_cards, padding="15", relief="solid")
            card.grid(row=row, column=col, columnspan=2, padx=15, pady=15, sticky=(tk.W, tk.E))
            
            ttk.Label(card, text=icone, font=("Arial", 24)).grid(row=0, column=0, rowspan=2, padx=(0, 15))
            
            ttk.Label(card, text=titulo_card, font=("Arial", 12, "bold")).grid(
                row=0, column=1, sticky=tk.W)
            
            ttk.Label(card, text=descricao_card, font=("Arial", 9), 
                     foreground="#7f8c8d", wraplength=200).grid(
                row=1, column=1, sticky=tk.W, pady=(5, 10))
            
            ttk.Button(card, text="Abrir Relatório", command=comando, width=15).grid(
                row=2, column=0, columnspan=2, pady=(5, 0))
        
        frame_export = ttk.LabelFrame(self.frame, text="📤 Exportação de Dados", padding="20")
        frame_export.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(frame_export, text="Exporte todos os dados do sistema para arquivos de texto:", 
                 font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(frame_export, text="📁 Exportar Todos os Dados", 
                  command=self.app.exportar_dados, width=25).grid(row=1, column=0, padx=5)
        ttk.Button(frame_export, text="🖨️ Imprimir Relatórios", 
                  command=self.imprimir_todos_relatorios, width=25).grid(row=1, column=1, padx=5)
        
        frame_navegacao = ttk.Frame(self.frame)
        frame_navegacao.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(frame_navegacao, text="🏠 Voltar ao Início", 
                  command=self.app.criar_tela_inicial, width=25).grid(row=0, column=0, padx=5)
        ttk.Button(frame_navegacao, text="❓ Ajuda", 
                  command=self.app.mostrar_guia_rapido, width=25).grid(row=0, column=1, padx=5)
    
    def imprimir_todos_relatorios(self):
        """Imprime todos os relatórios"""
        self.app.relatorio_completo()
        self.app.relatorio_situacao_acervo()
        self.app.relatorio_livros_mais_emprestados()
        
        messagebox.showinfo("Relatórios", "Todos os relatórios principais foram exibidos!")


def main():
    """Função principal para iniciar a aplicação"""
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA BIBLIOTECA ISCAT - VERSÃO FINAL COMPLETA")
    print("=" * 60)
    print("Módulos implementados:")
    print("✓ Cadastro de Livros")
    print("✓ Controle de Usuários")
    print("✓ Sistema de Empréstimos")
    print("✓ Consultas e Estoque")
    print("✓ Relatórios Avançados")
    print("=" * 60)
    print("Sistema pronto para uso! 🎓")
    main()
