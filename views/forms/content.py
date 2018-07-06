"""
Forms about content editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,\
                    TextAreaField, DateTimeField, SubmitField,\
                    SelectField, DateField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, URL

class ParticipationsInEventsForm(FlaskForm):
    """
    Form for the list of participations in events.
    """
    title = StringField('Instituição visitada:', validators=[
        DataRequired('Digite uma chamada para o intercâmbio.')
    ])

    description = TextAreaField('Resumo do envolvimento:', validators=[
        DataRequired('Insira um breve resumo sobre a participação.')
    ])

    year = IntegerField('Ano:', validators=[
        DataRequired('Informe qual o ano do evento.')
    ])

    location = StringField('Cidade e país:', validators=[
        DataRequired('Falta localizar a cidade e país.')
    ])

    index = IntegerField()

    create = SubmitField('Adicionar')

class NewsForm(FlaskForm):
    """
    Form for adding and editing news 
    """

    title = StringField('Titúlo da notícia:', validators=[
        DataRequired('Digite um titúlo para a notícia')
    ])
    
    headLine = StringField('Resumo básico/Manchete:', validators=[
        DataRequired('Digite a manchete')
    ])

    body = TextAreaField('Notícia:', validators=[
        DataRequired('Insira a notícia.')
    ])

    index = IntegerField()

    create = SubmitField('Editar');

class StaffForm(FlaskForm):
    """
    Form for list of staff.
    """
    name = StringField('Nome do servidor:', validators=[
        DataRequired('Digite o nome do servidor.')
    ])

    rank = StringField('Posição do servidor:', validators=[
        DataRequired('Digite a posição do servidor.')
    ])

    abstract = TextAreaField('Resumo da formação caso da coordenação, e descrição do trabalho caso secretário:', validators=[
        DataRequired('Insira um breve resumo sobre a formação acadêmica do servidor.')
    ])

    function = SelectField('Tipo de servidor', choices=[('coordination','Coordenação'), ('secretariat','Secretáriado')], validators = [
        DataRequired('Insira o tipo de servidor')
    ])

    photo = URLField('Foto do servidor')

    index = IntegerField()

    create = SubmitField('Adicionar')

class InstitutionsWithCovenantsForm(FlaskForm):
    """
    Form for the list of institutions with covenants.
    """
    name = StringField('Instituição com convênio:', validators=[
        DataRequired('Digite o nome da instituição.')
    ])

    initials = StringField('Sigla da Instituição:', validators=[
        DataRequired('Digite a sigla da instituição.')
    ])
    
    description = TextAreaField('Descrição do relacionamento entre o Grupo de Pesquisa e a Instituição')

    logo = FileField(validators=[
        DataRequired('Por favor insira um logo em formato .jpeg ou .png')
    ])

    create = SubmitField('Adicionar')

class EditInstitutionsWithCovenantsForm(FlaskForm):
    """
    Form for editing list of institutions with covenants.
    """

    name = StringField('Instituição com convênio:', validators=[
        DataRequired('Digite o nome da instituição.')
    ])

    initials = StringField('Sigla da Instituição:', validators=[
        DataRequired('Digite a sigla da instituição.')
    ])

    logo = FileField()

    description = TextAreaField('Descrição do relacionamento entre o Grupo de Pesquisa e a Instituição')

    index = IntegerField()

    create = SubmitField('Editar')

class MagazinesForm(FlaskForm):
    """
    Form for the list of magazines.
    """
    name = StringField('Nome da revista:', validators=[
        DataRequired('Digite o nome da revista.')
    ])

    issn = StringField('ISSN do periódico:', validators=[
        DataRequired('Digite o ISSN do periódico.')
    ])
    
    description = TextAreaField('Descrição da revista', validators=[
        DataRequired('Por favor descreva a revista.')
    ])

    cover = FileField(validators=[
        DataRequired('Por favor insira uma foto para a revista')
    ])

    create = SubmitField('Adicionar')

class EditMagazinesForm(FlaskForm):
    """
    Form for the list of magazines.
    """
    name = StringField('Nome da revista:', validators=[
        DataRequired('Digite o nome da revista.')
    ])

    issn = StringField('ISSN do periódico:', validators=[
        DataRequired('Digite o ISSN do periódico.')
    ])
    
    description = TextAreaField('Descrição da revista', validators=[
        DataRequired('Por favor descreva a revista.')
    ])

    cover = FileField()

    index = IntegerField()

    create = SubmitField('Adicionar')

class ScheduledReportForm(FlaskForm):

    """
    Scheduled report form.
    """
    time = DateTimeField('Data e hora:', format='%d/%m/%Y %H:%M')

    title = StringField('Título do trabalho:', validators=[
        DataRequired('Digite o título do trabalho.')
    ])

    author = StringField('Autoria:', validators=[
        DataRequired('Digite o nome do(s) autor(es).')
    ])

    location = StringField('Localização:', validators=[
        DataRequired('Digite a localização.')
    ])

    index = IntegerField()

    create = SubmitField('Agendar')

class CalendarForm(FlaskForm):

    """
    Calendar event form
    """

    title = StringField('Título do evento:', validators=[
        DataRequired('Digite o título do evento.')
    ])

    initial_date = DateField('Data inicial:', format='%d/%m/%Y', validators=[
        DataRequired('Escolha a data de começo do evento.')
    ])


    final_date = StringField('Data final(Se existir):')

    hour = StringField('Hora de começo e termino do evento(Se existir)')

    link = URLField('Link para mais informações(Se existir)')

    index = IntegerField()

    create = SubmitField('Adicionar')

class AttendanceForm(FlaskForm):
    """
    Form for adding attendance information to database
    """
    building = StringField('Prédio onde a unidade se localiza:', validators=[
        DataRequired('Digite o nome do prédio.')
    ])

    floor = StringField('Digite o andar onde a unidade se localiza:', validators=[
        DataRequired('Digite o andar.')
    ])

    room = StringField('Sala onde a unidade se localiza:', validators=[
        DataRequired('Digite o nome da sala.')
    ])

    email = EmailField('Email da unidade:', validators=[
        DataRequired('Digite o email.')
    ])

    opening = StringField('Horário de funcionamento:', validators=[
        DataRequired('Digite o horário de funcionamento.')
    ])

    type1 = StringField('Tipo do telefone:', validators=[
        DataRequired('Digite o tipo do telefone.')
    ])

    phone1 = StringField('Telefone:', validators=[
        DataRequired('Digite o telefone para contato.')
    ])

    type2 = StringField('Tipo do telefone:')

    phone2 = StringField('Telefone:')

    type3 = StringField('Tipo do telefone:')

    phone3 = StringField('Telefone:')

    attendance_id = StringField(validators=[
        DataRequired()
    ])

    create = SubmitField('Editar')

class DocumentForm(FlaskForm):
    """
    Form for upload of document
    """
    title = StringField('Titulo do documento:', validators=[
        DataRequired('Digite o título do documento.')
    ])

    cod = StringField('Código:', validators=[
        DataRequired('Informe qual o código do documento.')
    ])

    category = SelectField('Categoria',  choices=[
        ('regimento','Regimento'),('ata','ATA'),('outros','Outros')], validators=[
            DataRequired('Especifique o tipo de documento.')
    ])

    document = FileField(validators=[
        DataRequired('Por favor carregue um documento valido')
    ])

    create = SubmitField('Adicionar')

class EditDocumentForm(FlaskForm):
    """
    Form for edit and delete document
    """
    title = StringField('Titulo do documento:', validators=[
        DataRequired('Digite o título do documento.')
    ])

    cod = StringField('Código:', validators=[
        DataRequired('Informe qual o código do documento.')
    ])

    category = SelectField('Categoria',  choices=[
        ('regimento','Regimento'),('ata','ATA'),('outros','Outros')], validators=[
            DataRequired('Especifique o tipo de documento.')
    ])

    document = FileField()

    document_id = StringField(validators=[
        DataRequired()
    ])

    create = SubmitField('Adicionar')

class BookForm(FlaskForm):
    """
    Form for books
    """
    title = StringField('Titulo do livro:', validators=[
        DataRequired('Digite o título do livro.')
    ])

    subtitle = StringField('Subtitulo do livro(se houver):')

    authors = StringField('Nome do autor(es):', validators=[
        DataRequired('Digite o nome dos autor(es)')
    ])

    edition = IntegerField('Número da edição:', validators=[
        DataRequired('Digite o número da edição')
    ])

    location = StringField('Local de impressão:')

    publisher = StringField('Editora:')

    year = IntegerField('Ano da publicação:')

    index = IntegerField()

    create = SubmitField('Adicionar')

class ChapterForm(FlaskForm):
    """
    Form for chapters in books
    """
    book_title = StringField('Titulo do livro:', validators=[
        DataRequired('Digite o título do livro.')
    ])
    
    book_authors = StringField('Nome do autor(es) do livro:', validators=[
        DataRequired('Digite o nome dos autor(es)')
    ])

    chapter_title = StringField('Titulo do capitulo:', validators=[
        DataRequired('Digite o título do capitulo.')
    ])

    chapter_authors = StringField('Nome do autor(es) do capitulo:', validators=[
        DataRequired('Digite o nome dos autor(es)')
    ])

    edition = IntegerField('Número da edição:', validators=[
        DataRequired('Digite o número da edição')
    ])

    location = StringField('Local de impressão:')

    publisher = StringField('Editora:')

    year = IntegerField('Ano da publicação:')

    pages = StringField('Número das páginas:', validators=[
        DataRequired('Digite o número das páginas')
    ])

    index = IntegerField()

    create = SubmitField('Adicionar')


class ArticleForm(FlaskForm):
    """
    Form for articles
    """
    title = StringField('Titulo do artigo:', validators=[
        DataRequired('Digite o título do artigo.')
    ])

    subtitle = StringField('Subtitulo do artigo(se houver):')

    authors = StringField('Nome do autor(es):', validators=[
        DataRequired('Digite o nome dos autor(es)')
    ])

    edition = IntegerField('Número da edição:', validators=[
        DataRequired('Digite o número da edição')
    ])

    pages = StringField('Número das páginas:', validators=[
        DataRequired('Digite o número das páginas')
    ])

    number = IntegerField('Número:')

    location = StringField('Local de impressão:')

    publisher = StringField('Editora:')

    date = StringField('Data:')

    index = IntegerField()

    create = SubmitField('Adicionar')

class ProjectForm(FlaskForm):
    """
    Form for projects
    """
    title = StringField('Titulo do projeto:', validators=[
        DataRequired('Digite o título do projeto')
    ])

    subtitle = StringField('Subtitulo do projeto:')

    description = TextAreaField('Descrição do projeto:')

    situation = SelectField('Situação', choices=[
        ('Renovado', 'Renovado'), ('Em execução', 'Em execução'), ('Encerrado com pendências', 'Encerrado com pendências'), ('Finalizado', 'Finalizado'), ('Necessita correção', 'Necessita correção')], validators=[
            DataRequired('Escolha a situação do projeto')
    ])

    year = IntegerField('Ano do projeto', validators=[
        DataRequired('Digite o ano do projeto')
    ])

    email = EmailField('Email para contato', validators=[
        DataRequired('Por favor digite um email válido para contato')
    ])

    dt_init = StringField('Data de início do projeto', validators=[
        DataRequired('Digite a data de início do projeto')
    ])

    dt_end = StringField('Data esperada pra o final do projeto', validators=[
        DataRequired('Digite a data esperada para finalização do projeto')
    ])

    project_id = StringField()

    create = SubmitField('Adicionar')

class MemberOfProjectForm(FlaskForm):
    """
    Form for members inside project
    """
    name = StringField('Nome do membro:', validators=[
        DataRequired('Digite o nome do membro do projeto')
    ])

    project_role = SelectField('Categoria', choices=[
        ('Colaborador(a)', 'Colaborador(a)'), ('Coordenador(a)', 'Coordenador(a)')
    ])

    general_role = SelectField('Tipo', choices=[
        ('Discente', 'Discente'), ('Externo', 'Externo'), ('Coordenador(a)', 'Coordenador(a)')
    ])

    project_id = StringField(validators=[
        DataRequired('Houve um erro')
    ])

    index = IntegerField()

    create = SubmitField('Adicionar')
