
use grupospesquisa;

print("Inserindo grupos de pesquisa/usuários");

db.researchGroups.insertMany([
    {
        'name': 'Grupo Exemplo',
        'isSignedIn': true,
        'users': [
            {
                'nick': 'mazuh',
                'password': '$2b$14$poaO46ZWpL1NfVdJyS5mNeeMklsiEOxMFvm4aWx0ca1aRNVTBUR4u',
                'fullName': 'Usuário de testes para PPGP',
                'role': 'Usuário teste',
                'email': 'assessoriatecnica@ufrn.edu.br'
            }
        ],
        'descriptionSmall' : 'Descrição pequena',
        'descriptionBig' : 'Descrição grande Descrição grande Descrição grande Descrição grande Descrição grande Descrição grande',
    },
    {
        'name': 'Grupo Exemplo',
        'isSignedIn': true,
        'users': [],
        'descriptionSmall' : 'Descrição pequena',
        'descriptionBig' : 'Descrição grande Descrição grande Descrição grande Descrição grande Descrição grande Descrição grande',
    }
])

EX_ID = db.researchGroups.findOne({'name': 'Grupo Exemplo'})._id;

print("Inserindo atendimento...");

db.attendances.insertMany([
    {
        'ownerProgram': EX_ID,
        'location': {
            'building': 'Nepsa 2',
            'floor': 'Térreo',
            'room': 'A10',
            'opening': 'Segunda à Sexta-Feira (08:00 às 11:30 e 13:30 às 17:00)'
        },
        'email': 'email_exemplo@gmail.com',
        'phones': [
            {
                'type': 'Fixo',
                'number': '+55 84 3342-2288 (Ramal 189)'
            }
        ]
    }
]);

print("Inserindo linhas de pesquisa...");

db.researchLines.insertMany([
    {
        'ownerProgram': EX_ID,
        'name': 'Grupo Exemplo',
        'description': 'Rem accusamus consectetur explicabo aspernatur laboriosam sequi molestiae. Perferendis temporibus saepe quaerat. Enim omnis qui et aut fugiat non. Saepe cupiditate vitae quo qui. Ab laboriosam dolore sequi omnis necessitatibus.'
    }
]);

print("Inserindo informações sobre as integrações...");

db.integrationsInfos.insertMany([
    {
        'ownerProgram': EX_ID,
        'institutionsWithCovenant': [
            {
                'name': 'Instituto Nacional de Colonização e Reforma Agrária SR-19',
                'initials': 'INCRARN',
                'logoFile': 'logo-incrarn.jpg'
            },
            {
                'name': 'Universidade Federal do Rio Grande do Norte',
                'initials': 'UFRN',
                'logoFile': 'logo-ufrn.jpg'
            },
            {
                'name': 'Instituto Federal de Educação, Ciência e Tecnologia de Sergipe',
                'initials': 'IFS',
                'logoFile': 'logo-ifs.jpg'
            },
            {
                'name': 'Instituto Federal da Paraíba',
                'initials': 'IFPB',
                'logoFile': 'logo-ifpb.jpg'
            },
            {
                'name': 'Assembleia Legislativa do Estado Rio Grande do Norte',
                'initials': 'ALRN',
                'logoFile': 'logo-alrn.jpg'
            }
        ],
        'participationsInEvents': [
            {
                'title': 'Laboratoire de Recherche en Management (LAREQUOI)',
                'description': 'A professora Dinah dos Santos Tinoco participou de intercâmbio no LAREQUOI da Université de Versailles St. Quentin em Yvelines, França, no período de abril a junho de 2013. No período, além de ter participado de reuniões com professores do Laboratório, foi membro da comissão de avaliação de três bancas de defesa de Doutorado, tendo previamente elaborado Relatórios Técnicos de avaliação das teses.',
                'year': 2013,
                'international': 'Yvelines, França'
            },
            {
                'title': 'Center for Latin American Studies da Faculty of Economics and Public Administration da University of Economics',
                'description': 'O professor Hironobu Sano participou, em abril de 2013, de missão para o Center for Latin American Studies da Faculty of Economics and Public Administration da University of Economics, a principal instituição de ensino superior da República Tcheca.',
                'year': 2013,
                'international': 'Praga, República Tcheca'
            },
            {
                'title': 'Grupo de Investigación en Gobierno, Administración y Políticas Públicas (GIGAPP)',
                'description': 'O professor Thiago Dias participou como congressista do GIGAPP, realizado de 27 de setembro a 02 de outubro de 2014 em Madrid, Espanha, organizado pelo Instituto Nacional de Administración Pública, onde apresentou o artigo Gestão Social e Desenvolvimento Territorial: uma olhar a partir processo de governança dos colegiados territoriais brasileiro no Grupo de Trabalho Planejamento, Gestão Pública e Participação Social.',
                'year': 2014,
                'international': 'Madrid, Espanha'
            }
        ]
    }
]);

print("Inserindo coordenação...");

db.boardsOfStaffs.insertMany([
    {
        'ownerProgram': EX_ID,
        'coordination': [
            {
                'name': 'Thiago Ferreira Dias',
                'rank': 'Coordenador',
                'course': 'Direito',
                'abstract': 'Possui Doutorado em Administração pela Universidade Federal do Rio Grande do Norte (2011), Mestrado em Administração e Desenvolvimento Rural pela Universidade Federal Rural de Pernambuco (2007) e graduação em Administração pela Universidade Federal de Pernambuco (2005). De 2010 a 2013 foi professor da Universidade Federal Rural do Semi-Árido (UFERSA). De 2012 a 2013 foi coordenador da Incubadora de Iniciativas Sociais e Solidárias do Oeste Potiguar (INCUBAOESTE). Desde janeiro de 2014 é professor adjunto da Universidade Federal do Rio Grande do Norte.',
                'photo': 'http://servicosweb.cnpq.br/wspessoa/servletrecuperafoto?tipo=1&id=K4731730Y4'
            },
            {
                'name': 'Antônio Alves Filho',
                'rank': 'Vice-Coordenador',
                'course': 'Direito',
                'abstract': 'Possui graduação em Psicologia pela Universidade Federal do Rio Grande do Norte (1993) e mestrado em Administração (1999) e doutorado em Psicologia (2012) também pela UFRN. De 2009 a 2013 foi professor adjunto da Universidade Federal de Alagoas (UFAL), no curso de Psicologia. A partir de dezembro de 2013, passou a ser professor adjunto do Departamento de Ciências Administrativas da Universidade Federal do Rio Grande do Norte. Na Psicologia atua na área da Psicologia do Trabalho e das Organizações, com ênfase em Fatores Humanos no Trabalho. Na Administração atua na área de Gestão de Pessoas. Desde 2014 é docente permanente do Programa de Pós-Graduação em Gestão Pública, UFRN.',
                'photo': 'http://servicosweb.cnpq.br/wspessoa/servletrecuperafoto?tipo=1&id=K4701984E0'
            }
        ],
        'students': [
            {
                'name': 'Penélope Medeiros Filgueira Burlamaqui',
                'course': 'Direito',
                'function': {
                    'rank': 'Discente',
                    'description': 'Chefia a secretaria, responsável por organizar e movimentar a burocracia do setor.'
                },
                'photo': ''
            },
            {
                'name': 'Marcell Guilherme Costa da Silva',
                'course': 'Direito',
                'function': {
                    'rank': 'Discente',
                    'description': 'Desenvolve o sistema web, automatiza atividades da secretaria e provê um mínimo suporte técnico aos computadores.'
                },
                'photo': ''
            },
            {
                'name': 'Davila Regina Silva Rodrigues',
                'course': 'Serviço Social',
                'function': {
                    'rank': 'Discente',
                    'description': 'Provê um suporte maior à administração do setor, juntamente com a secretária.'
                },
                'photo': ''
            }
        ],
    'researchers': [
        {
            'name': 'Luccas Mateus de Medeiros Gomes',
            'course': 'Direito',
            'function': {
                'rank': 'Discente',
                'description': 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo'
            },
            'photo': ''
        },
        {
            'name': 'Luca Lisboa Krause',
            'course': 'Direito',
            'function': {
                'rank': 'Discente',
                'description': 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo'
            },
            'photo': ''
        },
        {
            'name': 'Luis Lucas Martins Peixoto',
            'course': 'Direito',
            'function': {
                'rank': 'Discente',
                'description': 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo'
            },
            'photo': ''
        }
    ]
}
]);

print("Inserindo trabalhos de conclusão...");

db.finalReports.insertMany([
    {
        'ownerProgram': EX_ID,
        'scheduledReports': [
            {
                'time': new Date(2017, 06, 25, 14, 00, 00, 00),
                'title': 'Direcionamento Estratégico Da Assembleia Legislativa Do Rio Grande Do Norte',
                'author': 'Carlos Eduardo Artioli Russo',
                'location': 'Sala D4 do Setor V'
            }
        ]
    }
]);


print("Inserindo documentos oficiais...");

db.officialDocuments.insertMany([
    {
        'ownerProgram': EX_ID,
        'title': 'Regimento Interno',
        'category': 'regimento',
        'cod': '12-2015',
        'file': 'regimento_0122015consepe.pdf',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Estrutura Curricular',
        'category': 'regimento',
        'cod': '01-2014',
        'file': 'resolucao_ESTRUTURA-CURRICULAR.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Matrícula',
        'category': 'regimento',
        'cod': '02-2014',
        'file': 'resolucao_MATRICULA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Exame de Proficiência',
        'category': 'outros',
        'cod': '03-2014',
        'file': 'resolucao_EXAME-DE-PROFICIENCIA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Procedimentos de Defesa',
        'category': 'ata',
        'cod': '04-2014',
        'file': 'resolucao_PROCEDIMENTOS-DE-DEFESA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Exame de Qualificação',
        'category': 'regimento',
        'cod': '05-2014',
        'file': 'resolucao_EXAME-DE-QUALIFICACAO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Credenciamento Docente',
        'category': 'ata',
        'cod': '06-2014',
        'file': 'resolucao_CREDENCIAMENTO-DOCENTE.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Resolução de Calendário',
        'category': 'outros',
        'cod': '07-2014',
        'file': 'resolucao_RESOLUCAO-CALENDARIO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Áreas de Concentração e Linhas de Pesquisa',
        'category': 'ata',
        'cod': '08-2014',
        'file': 'resolucao_LINHAS-PESQUISA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Projeto de Intervenção',
        'category': 'outros',
        'cod': '09-2014',
        'file': 'resolucao_PROJETO-INTERVENCAO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': EX_ID,
        'title': 'Aluno Especial',
        'category': 'ata',
        'cod': '10-2014',
        'file': 'resolucao_ALUNO-ESPECIAL.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    }
]);

print("Inserindo eventos...");

db.calendar.insertMany([
    {
        'ownerProgram': EX_ID,
        'events': [
          {
            'title': 'Matrícula para o período 2017.2',
            'initialDate': new Date(2017, 07, 17, 00, 00, 00, 00),
            'finalDate': new Date(2017, 07, 21, 00, 00, 00, 00),
            'hour' : "",
            'link': ""
          },
          {
            'title': 'Início do período letivo 2017.2.',
            'initialDate': new Date(2017, 07, 17, 00, 00, 00, 00),
            'finalDate': "",
            'hour' : "",
            'link': 'https://duckduckgo.com'
          },
          {
            'title': 'Hackathon UFRN',
            'initialDate': new Date(2017, 07, 17, 00, 00, 00, 00),
            'finalDate': new Date(2017, 07, 20, 00, 00, 00, 00),
            'hour' : "",
            'link': 'duckduckgo.com'
          },
          {
            'title': 'Palestra sobre Direito Processual Civil',
            'initialDate': new Date(2017, 07, 17, 00, 00, 00, 00),
            'finalDate': new Date(2017, 07, 17, 00, 00, 00, 00),
            'hour' : '13:00 a 18:00',
            'link': ""
          }
        ]
    }
]);

print("Inserindo publicações...");

db.publications.insertMany([
    {
        'ownerProgram': EX_ID,
        'books': [
          {
            'authors': 'João Guimarães Rosa',
            'title': 'Grande Sertão Veredas',
            'edition': '12.ed',
            'location' : 'São Paulo',
            'publisher': 'Editora 34',
            'year' : '2002'
          },
          {
            'authors': 'Leonardo Martins e Dmitri Dimoulis',
            'title': 'Teoria dos direitos fundamentais',
            'edition': '5.ed',
            'location' : 'Porto Alegre',
            'publisher': 'Editora Saraiva',
            'year' : '2014'
          }
        ],
        'articles': [
          {
            'authors':'Roberto Campos',
            'title': 'Em defesa dos bodes',
            'publisher' : 'Veja',
            'location' : 'São Paulo',
            'edition' : '1731.ed',
            'number': 'n. 2',
            'pages': '23-30',
            'date': '12 jan. 2000'

          },
          {
            'authors':'Fabiana Mottta',
            'title': 'Incapazes no novo código civil',
            'publisher' : 'InVerbis',
            'location' : 'Natal',
            'edition' : '12.ed',
            'number': 'n. 1',
            'pages': '50-62',
            'date': '13 jul. 2016'

          }
        ]
    }
]);

db.news.insertMany([
    {
        'ownerProgram': EX_ID,
        'news' : [
          {
            'title': 'Lorem ipsum',
            'id': '1',
            'headline' : 'quod consequatur ex culpa labore tenetur voluptatem qui consequatur aut ut voluptas sapiente similique recusandae nemo quis qui et cumque',
            'body' : 'Atque veniam fuga magnam culpa necessitatibus. Consequatur dolorem magnam aut quod repellat temporibus vel natus. Possimus et est possimus aut ad est atque qui. Corrupti recusandae veritatis quia sed totam aspernatur qui. Esse aliquam magni ullam culpa possimus consequuntur. Dolores sint optio velit harum maiores ut. Rerum corrupti perspiciatis ipsa velit nisi saepe. Ex nostrum qui culpa. Voluptatibus molestiae ab mollitia reprehenderit. consectetur ex.'
          }
        ]
    },
]);

db.avaliationForm.insertMany([
    {
        'ownerProgram': EX_ID,
        'formYear' : [],
        'formFourYears' : [],
    },
]);
