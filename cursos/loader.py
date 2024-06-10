from cursos.models import Curso, Area_Cientifica, Linguagem_Programacao, Disciplina, Projeto, Docente
import json
from django.db.models import Count

Curso.objects.all().delete()
Area_Cientifica.objects.all().delete()
Disciplina.objects.all().delete()
Projeto.objects.all().delete()
Linguagem_Programacao.objects.all().delete()
Docente.objects.all().delete()

def importar_curso1(ficheiro_json):
    with open('cursos/json/lei.json') as f:
        dados = json.load(f)

    curso_dados = dados['curso']
    curso = Curso.objects.create(
        nome=curso_dados['nome'],
        apresentacao=curso_dados['apresentacao'],
        objetivos=curso_dados['objetivos'],
        competencias=curso_dados['competencias']
    )

    areas_cientificas_dados = dados['areas_cientificas']
    for area_dados in areas_cientificas_dados:
        Area_Cientifica.objects.create(
            nome=area_dados['nome']
        )

    disciplinas_dados = dados['disciplinas']
    for disciplina_dados in disciplinas_dados:
        area_cientifica = Area_Cientifica.objects.get(nome=disciplina_dados['area_cientifica'])
        disciplinas = Disciplina.objects.filter(nome=disciplina_dados['nome'])
        if disciplinas.exists():
            # Se houver disciplinas com o mesmo nome, adiciona todas elas ao docente
            for disciplina in disciplinas:
                disciplina.projetos.clear()  # Limpa os projetos existentes (opcional)
                projeto_dados = disciplina_dados['projetos'][0]  # Considera apenas o primeiro projeto por disciplina
                projeto = Projeto.objects.create(
                    nome=projeto_dados['nome'],
                    descricao=projeto_dados['descricao'],
                    conceitos=projeto_dados['conceitos'],
                    tecnologias=projeto_dados['tecnologias'],
                    foto=projeto_dados['foto'],
                    video=projeto_dados.get('video'),
                    gitLink=projeto_dados.get('gitLink'),
                    disciplina=disciplina
                )
                linguagens_dados = projeto_dados['linguagens']
                for linguagem_dados in linguagens_dados:
                    linguagem, _ = Linguagem_Programacao.objects.get_or_create(
                        nome=linguagem_dados['nome']
                    )
                    projeto.linguagens.add(linguagem)
        else:
            # Se não houver disciplinas com o mesmo nome, cria uma nova
            disciplina = Disciplina.objects.create(
                nome=disciplina_dados['nome'],
                ano=disciplina_dados['ano'],
                semestre=disciplina_dados['semestre'],
                ects=disciplina_dados['ects'],
                code=disciplina_dados['code'],
                area_cientifica=area_cientifica
            )

            projetos_dados = disciplina_dados['projetos']
            for projeto_dados in projetos_dados:
                projeto = Projeto.objects.create(
                    nome=projeto_dados['nome'],
                    descricao=projeto_dados['descricao'],
                    conceitos=projeto_dados['conceitos'],
                    tecnologias=projeto_dados['tecnologias'],
                    foto=projeto_dados['foto'],
                    video=projeto_dados.get('video'),
                    gitLink=projeto_dados.get('gitLink'),
                    disciplina=disciplina
                )
                linguagens_dados = projeto_dados['linguagens']
                for linguagem_dados in linguagens_dados:
                    linguagem, _ = Linguagem_Programacao.objects.get_or_create(
                        nome=linguagem_dados['nome']
                    )
                    projeto.linguagens.add(linguagem)

    docentes_dados = dados['docentes']
    for docente_dado in docentes_dados:
        docente = Docente.objects.create(
            nome=docente_dado['nome']
        )
        disciplinas_dados = docente_dado['disciplinas']
        for disciplina_nome in disciplinas_dados:
            disciplinas = Disciplina.objects.filter(nome=disciplina_nome)
            for disciplina in disciplinas:
                docente.disciplina.add(disciplina)




importar_curso1('cursos/json/lei.json')

def listar_disciplinas_por_area(area_nome):
    print(f"Disciplinas da área científica {area_nome}:")
    area = Area_Cientifica.objects.get(nome=area_nome)
    disciplinas = Disciplina.objects.filter(area_cientifica=area)
    for disciplina in disciplinas:
        print(disciplina)


def listar_projetos_por_linguagem(linguagem_nome):
    print(f"Projetos que utilizam a linguagem {linguagem_nome}:")
    linguagem = Linguagem_Programacao.objects.get(nome=linguagem_nome)
    projetos = Projeto.objects.filter(linguagens=linguagem)
    for projeto in projetos:
        print(projeto)

def contar_docentes_por_nome(nome_docente):
    num_docentes = Docente.objects.filter(nome__icontains=nome_docente).count()
    print(f"Número de docentes com o nome {nome_docente}: {num_docentes}")


def listar_projetos_por_disciplina(disciplina_nome):
    print(f"Projetos relacionados à disciplina {disciplina_nome}:")
    disciplina = Disciplina.objects.get(nome=disciplina_nome)
    projetos = Projeto.objects.filter(disciplina=disciplina)
    for projeto in projetos:
        print(projeto)


def listar_docentes_por_disciplina(disciplina_nome):
    print(f"Docentes que ministram a disciplina {disciplina_nome}:")
    disciplina = Disciplina.objects.get(nome=disciplina_nome)
    docentes = Docente.objects.filter(disciplina=disciplina)
    for docente in docentes:
        print(docente)

def listar_linguagens_por_projeto(projeto_nome):
    print(f"Linguagens de programação utilizadas no {projeto_nome}:")
    try:
        projeto = Projeto.objects.get(nome=projeto_nome)
        linguagens = projeto.linguagens.all()
        for linguagem in linguagens:
            print(linguagem)
    except Projeto.DoesNotExist:
        print(f"{projeto_nome} não foi encontrado.")


def listar_area_por_disciplina(disciplina_nome):
    try:
        disciplina = Disciplina.objects.get(nome=disciplina_nome)
        area = disciplina.area_cientifica
        print(f"A disciplina {disciplina_nome} pertence à área científica {area}.")
    except Disciplina.DoesNotExist:
        print(f"A disciplina {disciplina_nome} não foi encontrada.")


def contar_projetos_por_disciplina(disciplina_nome):
    try:
        disciplina = Disciplina.objects.get(nome=disciplina_nome)
        num_projetos = Projeto.objects.filter(disciplina=disciplina).count()
        print(f"Número de projetos relacionados à disciplina {disciplina_nome}: {num_projetos}")
    except Disciplina.DoesNotExist:
        print(f"A disciplina {disciplina_nome} não foi encontrada.")
