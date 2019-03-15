var app = document.getElementById('app');


class DadosBase extends React.Component {
    render() {
        return(
            <div>
                <h4>Passo 1 de 3 <small className="text-muted">Informações do grupo de pesquisa</small></h4>
                <p>Por favor, preencha abaixo os dados relacionados à base de pesquisa avaliada</p>

                <div className="row">
                    <div className="col-md-8">
                        <div className="form-group">
                            <label htmlFor="nomeBase">Nome da base <span className="red-text">*</span></label>
                            <input type="text" className="form-control" id="nomeBase" placeholder="Nome da base de pesquisa" defaultValue={this.props.currentState.group_name} onChange={this.props.changeName} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="nomeBase">Coordenador(a) <span className="red-text">*</span></label>
                            <input type="text" className="form-control" id="nomeBase" placeholder="Coordenador(a) da base de pesquisa" defaultValue={this.props.currentState.coordinator} onChange={this.props.changeCoordinator} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="anoAtividades">Ano de referência <span className="red-text">*</span> <i>(ano em que as atividades cadastradas ocorreram)</i></label>
                            <input type="number" className="form-control" id="nomeBase" defaultValue={this.props.currentState.year} onChange={this.props.changeYear} />
                        </div>
                        <div className="row">
                            <div className="col-md-6">
                                <div className="form-group">
                                    <label htmlFor="alunosGraduacao">Número de alunos de graduação vinculados ao projeto de pesquisa (alunos bolsistas ou não desde que devidamente comprovados)<span className="red-text">*</span></label>
                                    <br></br>
                                    <br></br>
                                    <br></br>
                                    <input type="number" className="form-control" id="alunosGraduacao" defaultValue={this.props.currentState.numGrad} onChange={this.props.changeGrad} />
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div className="form-group">
                                    <label htmlFor="alunosPosGraduacao">Número de alunos de pós-graduação vinculados ao projeto de pesquisa (não podem ser contabilizados os projetos de dissertações e teses dos alunos, pois estes são projetos dos alunos). <span className="red-text">*</span></label>
                                    <input type="number" className="form-control" id="alunosPosGraduacao" defaultValue={this.props.currentState.numPosGrad} onChange={this.props.changePosGrad}/>
                                </div>
                            </div>
                        </div>
                        <div className="form-group">
                            <label htmlFor="atividadesFuturas">Atividades futuras <span className="red-text">*</span> <i>(atividades que a base planeja desenvolver futuramente)</i></label>
                            <textarea className="form-control" onChange={this.props.changeGoals} defaultValue={this.props.currentState.goals}></textarea>
                        </div>
                        <button className="btn btn-primary" onClick={this.props.nextStep} >Próximo passo</button>
                    </div>
                </div><br/><br/><br/>
            </div>
        );
    }
}

class Autocomplete extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activeSuggestion: 0,
            filteredSuggestions: [],
            showSuggestions: false,
            userInput: ""
        }
        this.onChange = this.onChange.bind(this);
        this.onClick = this.onClick.bind(this);
        this.sendProfessor = this.sendProfessor.bind(this);
    } 

    onChange(e) {
        const suggestions = this.props.suggestions;
        const userInput = e.currentTarget.value;

        // Filter our suggestions that don't contain the user's input
        const filteredSuggestions = suggestions.filter(
        suggestion =>
            suggestion.toLowerCase().indexOf(userInput.toLowerCase()) > -1
        );

        // Update the user input and filtered suggestions, reset the active
        // suggestion and make sure the suggestions are shown
        this.setState({
            activeSuggestion: 0,
            filteredSuggestions,
            showSuggestions: true,
            userInput: e.currentTarget.value
        });
    };

    sendProfessor(event) {
        if(this.props.suggestions.filter(el => el === this.state.userInput).length > 0){
            this.props.addProfessor(this.state.userInput, true, this.props.phd);
            this.setState({
                activeSuggestion: 0,
                filteredSuggestions: [],
                showSuggestions: false,
                userInput: "" 
            });
        }
    }

    onClick(e) {
        this.setState({
            activeSuggestion: 0,
            filteredSuggestions: [],
            showSuggestions: false,
            userInput: e.currentTarget.innerText
        });
    }

    render() {
        const {
            onChange,
            onClick,
            onKeyDown,
            state: {
              activeSuggestion,
              filteredSuggestions,
              showSuggestions,
              userInput
            }
          } = this;
          let suggestionsListComponent;

          if (showSuggestions && userInput) {
            if (filteredSuggestions.length) {
              suggestionsListComponent = (
                <ul class="suggestions">
                  {filteredSuggestions.map((suggestion, index) => {
                    let className;
      
                    return (
                      <li
                        className={className}
                        key={suggestion}
                        onClick={onClick}
                      >
                        {suggestion}
                      </li>
                    );
                  })}
                </ul>
              );
            } else {
              suggestionsListComponent = (
                <div class="no-suggestions">
                  <em>Nenhum professor com esse nome foi encontrado</em>
                </div>
              );
            }
          }
      
          return (
            <div>
            <React.Fragment>
              <input
                type="text"
                className="form-control"
                placeholder="Procure o professor na lista"
                onChange={onChange}
                onKeyDown={onKeyDown}
                value={userInput}
              />
              {suggestionsListComponent}
            </React.Fragment>
            <button className="btn-primary btn-block" onClick={this.sendProfessor} >Adicionar professor</button>
            </div>
          );
        }
}

class CadastroProfessores extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            curr_professor: {
                name: '',
                ccsa: false,
                master_phd: false 
            },
        }

        this.changeProfessorName = this.changeProfessorName.bind(this);
        this.changeProfessorMasterPHD = this.changeProfessorMasterPHD.bind(this);
        this.sendProfessor = this.sendProfessor.bind(this);
    }

    changeProfessorName(event) {
        this.setState({curr_professor : {
               name : event.nativeEvent.target.value,
               ccsa: this.state.curr_professor.ccsa,
               master_phd: this.state.curr_professor.master_phd
            }
        });
    }

    changeProfessorMasterPHD(event) {
        this.setState({curr_professor : {
               name : this.state.curr_professor.name,
               ccsa: this.state.curr_professor.ccsa,
               master_phd: !(this.state.curr_professor.master_phd),
            }
        });
    }
    sendProfessor(event) {
        this.props.addProfessor(this.state.curr_professor.name, false, this.state.curr_professor.master_phd);
        document.getElementById('nomeDoProfessor').value = '';
        document.getElementById('professorQualificacao').checked = false;
        this.setState({curr_professor: {
                name: '',
                ccsa: false,
                master_phd: false,
            }
        });
    }

    render() {
        return(
            <div>
                <h4>Passo 2 de 3 <small className="text-muted">Professores relacionados</small></h4>
                <p>Por favor, cadastre os professores relacionados à base de pesquisas para avaliação</p>

                <div className="row">
                    <div className="col-md-10">
                        <div className="row">
                            <div className="col-md-10">
                                <Autocomplete addProfessor={this.props.addProfessor} suggestions={this.props.professorsList} phd={this.state.curr_professor.master_phd} />
                                <br/>
                                <input type="text" id="nomeDoProfessor" className="form-control" onChange={this.changeProfessorName} placeholder="Nome do professor"/>
                                <button className="btn-primary btn-block" onClick={this.sendProfessor} >Adicionar professor</button>
                                <br/>
                                <div className="form-check">
                                <p>O professor possui titúlo de mestre ou doutor?</p>
                                <input type="checkbox" name="master_phd" value="1" id="professorQualificacao" onChange={this.changeProfessorMasterPHD}/>
                                <label className="form-check-label" htmlFor="professorQualificacao">Sim</label>
                                </div>
                            </div>
                        </div><br/>
                        <TabelaProfessores professors={this.props.professors} removeProfessor={this.props.removeProfessor}/>
                        <br/>
                        <button onClick={this.props.previousStep} className="btn">Passo anterior</button> <button onClick={this.props.nextStep} className="btn btn-primary">Próximo passo</button>
                    </div>
                </div>
            </div>
        );
    }
}

class TabelaProfessores extends React.Component {

    render() {
        return(
            <div>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Nome do professor</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name} { 
                                            prof.master_phd === true ? <span className="btn btn-success">Possui PHD</span> 
                                            : <span className="btn btn-danger">Não possui PHD</span>  } 
                                            {
                                            prof.ccsa === true ? <span className="btn btn-success">Filiado ao CCSA</span> 
                                            : <span className="btn btn-danger">Não filiado ao CCSA</span>  } 
                                            <button onClick={() => this.props.removeProfessor(prof.id)}>remover</button></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
            </div>
        );
    }
}

class Avaliacao extends React.Component {

    componentDidMount() {
        () => this.props.getInformation();
    }

    render() {
        return(
            <div>
                <h4>Passo 3 de 3 <small className="text-muted">Critérios de avaliação</small></h4>
                <p>Por favor, preencha corretamente as tabelas abaixo relativas aos 7 critérios de avaliação da base de pesquisa. Os critérios referem-se aos professores, apenas. Note que para cada atividade relatada aparecerá abaixo da tabela um campo para descrição detalhada da atividade</p>
                <button className="btn" onClick={this.props.previousStep} >Passo anterior</button><br/><br/>
                <CriterioUm professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioDois professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioTres professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioQuatro professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioCinco professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioSeis professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion}/><hr/>
                <CriterioSete professors={this.props.professors} changeProfessorFieldNumber={this.props.changeProfessorFieldNumber} changeInsertion={this.props.changeInsertion} /><br/><br/>
                <button onClick={() => this.props.submit("partial")} className="btn">Salvar</button> <button onClick={() => this.props.submit("final")} className="btn btn-primary">Envio final</button>
            </div>
        );
    }
}

class CriterioUm extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 1.</b> Produção científica dos professores do Grupo de Pesquisa no ano referente em eventos locais, regionais, nacionais e internacionais (número de participações em eventos com trabalhos completos em anais de congressos) Fonte: Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th rowSpan={2}>Professores</th>
                            <th colSpan={4}>Eventos</th>
                        </tr>
                        <tr>
                            <td><center>Local</center></td>
                            <td><center>Regional</center></td>
                            <td><center>Nacional</center></td>
                            <td><center>Internacional</center></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[0][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 1, 'Local')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[0][1].insertions.length}  type="number" onChange={this.handleChange.bind(null, prof.id, 1, 'Regional')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[0][2].insertions.length}  type="number" onChange={this.handleChange.bind(null, prof.id, 1, 'Nacional')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[0][3].insertions.length}  type="number" onChange={this.handleChange.bind(null, prof.id, 1, 'Internacional')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[0].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 0, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }

            </div>
        );
    }
}

class CriterioDois extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 2.</b> Produção científica definitiva dos professores do Grupo de Pesquisa no ano referente (número de publicações em artigos, livros, capítulos de livros). Fonte: Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th rowSpan={2}>Professores</th>
                            <th colSpan={4}>Produção</th>
                        </tr>
                        <tr>
                            <td><center>Artigos</center></td>
                            <td><center>Cap. Livro</center></td>
                            <td><center>Livro</center></td>
                            <td><center>Org. Livros</center></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[1][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 2, 'Artigos')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[1][1].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 2, 'Cap. Livro')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[1][2].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 2, 'Livro')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[1][3].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 2, 'Org. Livros')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[1].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 1, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }
            </div>
        );
    }
}

class CriterioTres extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 3.</b> Número de projetos de pesquisa financiados por agências externas à UFRN no ano referente. Fonte: Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Professores</th>
                            <th>Número</th>
                        </tr>
                    </thead>
                    <tbody>
                    {
                        this.props.professors.map(function(prof) {
                            return(
                                <tr key={prof.id}>
                                    <td>{prof.name}</td>
                                    <td><input className="tableNumber" value={prof.criterions[2][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 3, 'Projetos')} /></td>
                                </tr>
                            );
                        }, this)
                    }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[2].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 2, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }
            </div>
        );
    }
}

class CriterioQuatro extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 4.</b> Número de projetos de pesquisa desenvolvidos internamente pelos participantes do Grupo de Pesquisa, com ou sem financiamento, no ano referente, cadastrados no SIGAA. (serão contabilizados o número de projetos por coordenador). Fonte:Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Professores</th>
                            <th>Número</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[3][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 4, 'Projetos')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[3].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 3, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }
            </div>
        );
    }
}

class CriterioCinco extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 5.</b> Número de professores com bolsas produtividade que participam do Grupo de Pesquisa no ano referente. Fonte: Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Professores</th>
                            <th>Número</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[4][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 5, 'Bolsas')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[4].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 4, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }
            </div>
        );
    }
}

class CriterioSeis extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 6.</b> Participação do Grupo de Pesquisa no Seminário de Pesquisa do CCSA no ano referente, (número de atividades). Fonte: Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th rowSpan={2}>Professores</th>
                            <th colSpan={7}>Participação no seminário</th>
                        </tr>
                        <tr>
                            <td><center>Ofic.</center></td>
                            <td><center>Conf.</center></td>
                            <td><center>Minicursos</center></td>
                            <td><center>Mesas redondas</center></td>
                            <td><center>Coord. GT</center></td>
                            <td><center>Org. Evento</center></td>
                            <td><center>Exposição</center></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[5][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Ofic.')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][1].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Conf.')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][2].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Minicursos')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][3].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Mesas redondas')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][4].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Coord. GT')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][5].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Org. Evento')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[5][6].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 6, 'Exposição')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[5].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 5, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }
            </div>
        );
    }
}

class CriterioSete extends React.Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleInsChange = this.handleInsChange.bind(this);
    }

    handleChange(id, criterion, type, e) {
        this.props.changeProfessorFieldNumber(id, criterion, type, e.target.value);
    }

    handleInsChange(id, CriIdx, typeIdx, insIdx, e) {
        this.props.changeInsertion(id, CriIdx, typeIdx, insIdx, e.target.value);
    }

    render() {
        return(
            <div>
                <div className="card">
                    <div className="card-body">
                        <b>Critério 7.</b> Organização de eventos pelos professores do Grupo de Pesquisa (número de eventos - seminários, encontros, colóquios, oficinas, etc) e participação em eventos como debatedor, organizador de mesa redonda e avaliador de trabalhos. Fonte:Lattes
                    </div>
                </div><br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th rowSpan={2}>Professores</th>
                            <th colSpan={4}>Organização de eventos</th>
                            <th colSpan={3}>Participação em eventos</th>
                        </tr>
                        <tr>
                            <td><center>Seminários</center></td>
                            <td><center>Encontros</center></td>
                            <td><center>Colóquios</center></td>
                            <td><center>Oficinas</center></td>
                            <td><center>Debates</center></td>
                            <td><center>Org. Mesas</center></td>
                            <td><center>Aval. Trabalhos</center></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.props.professors.map(function(prof) {
                                return(
                                    <tr key={prof.id}>
                                        <td>{prof.name}</td>
                                        <td><input className="tableNumber" value={prof.criterions[6][0].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Seminários')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][1].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Encontros')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][2].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Colóquios')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][3].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Oficinas')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][4].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Debates')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][5].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Org. Mesas')} /></td>
                                        <td><input className="tableNumber" value={prof.criterions[6][6].insertions.length} type="number" onChange={this.handleChange.bind(null, prof.id, 7, 'Aval. Trabalhos')} /></td>
                                    </tr>
                                );
                            }, this)
                        }
                    </tbody>
                </table>
                {
                    this.props.professors.map(function(prof) {
                        return(<div className="card" key={prof.id}>
                            <div className="card-header">{ prof.name }</div>
                            <div className="card-body">
                            {
                                prof.criterions[6].map(function(type, typeIdx){
                                    return(
                                        <div key={typeIdx}>
                                            {
                                                type.insertions.map(function(ins, insIdx) {
                                                    return(
                                                        <div key={insIdx}>
                                                            {type.type}<br/>
                                                            <textarea value={ins} onChange={this.handleInsChange.bind(null, prof.id, 6, typeIdx, insIdx)} className="form-control" rows="3"></textarea>
                                                        </div>
                                                    );
                                                }, this)
                                            }
                                        </div>
                                    )
                                }, this)
                            }
                            </div>
                        </div>);
                    }, this)
                }

            </div>
        );
    }
}

class Success extends React.Component {
    render() {
        return(
            <div>
                <h4>Avaliação submetida com sucesso!</h4>
            </div>
        );
    }
}

class Fail extends React.Component {
    render() {
        return(
            <div>
                <h4>Erro ao submeter avaliação!</h4>
            </div>
        );
    }
}

class Application extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            curr_step: 1,
            group_name: '',
            coordinator: '',
            state : 'inProgress',
            groupAccount: document.getElementById("groupName").textContent.replace(' ', '+'),
            year: 0,
            numGrad: 0,
            numPosGrad: 0,
            goals: '',
            id_counter: 0,
            professors: [],
            professorsList: []
        };

        this.changeName = this.changeName.bind(this);
        this.changeCoordinator = this.changeCoordinator.bind(this);
        this.changeYear = this.changeYear.bind(this);
        this.changeGrad = this.changeGrad.bind(this);
        this.changePosGrad = this.changePosGrad.bind(this);
        this.changeGoals = this.changeGoals.bind(this);
        this.nextStep = this.nextStep.bind(this);
        this.previousStep = this.previousStep.bind(this);
        this.addProfessor = this.addProfessor.bind(this);
        this.removeProfessor = this.removeProfessor.bind(this);
        this.changeProfessorFieldNumber = this.changeProfessorFieldNumber.bind(this);
        this.changeInsertion = this.changeInsertion.bind(this);
        this.submit = this.submit.bind(this);
        this.getInformation = this.getInformation.bind(this);
    }

    componentWillMount() {
        if (!(window.location.href.includes("new=new"))) {
            this.getInformation();
        }
        this.getProfessors();
    }

    changeName(event) {
        this.setState({ group_name: event.nativeEvent.target.value });
    }

    changeCoordinator(event) {
        this.setState({ coordinator: event.nativeEvent.target.value });
    }

    changeYear(event) {
        this.setState({ year: event.nativeEvent.target.value });
    }

    changeGrad(event) {
        this.setState({ numGrad: event.nativeEvent.target.value });
    }

    changePosGrad(event) {
        this.setState({ numPosGrad: event.nativeEvent.target.value });
    }

    changeGoals(event) {
        this.setState({ goals: event.nativeEvent.target.value });
    }

    nextStep() {
        this.setState(function (prevState, props) { return {curr_step: prevState.curr_step + 1} });
    }

    previousStep() {
        this.setState(function (prevState, props) { return {curr_step: prevState.curr_step - 1} });
    }

    addProfessor(name, ccsa, master_phd) {
        this.setState(function(prevState, props) {
            var newProfs = prevState.professors;
            newProfs.push({
                name: name,
                id: prevState.id_counter,
                ccsa: ccsa,
                master_phd: master_phd,
                // {type: '', description: ''}
                criterions: [
                    [ // Criterio 1
                        {type: 'Local', insertions: []},
                        {type: 'Regional', insertions: []},
                        {type: 'Nacional', insertions: []},
                        {type: 'Internacional', insertions: []}
                    ],
                    [ // Criterio 2
                        {type: 'Artigos', insertions: []},
                        {type: 'Cap. Livro', insertions: []},
                        {type: 'Livro', insertions: []},
                        {type: 'Org. Livros', insertions: []},

                    ],
                    [ // Critério 3
                        {type: 'Projetos', insertions: []},
                    ],
                    [ // Criterio 4
                        {type: 'Projetos', insertions: []},
                    ],
                    [ // Criteio 5
                        {type: 'Bolsas', insertions: []},
                    ],
                    [ // Criterio 6
                        {type: 'Ofic.', insertions: []},
                        {type: 'Conf.', insertions: []},
                        {type: 'Minicursos', insertions: []},
                        {type: 'Mesas redondas', insertions: []},
                        {type: 'Coord. GT', insertions: []},
                        {type: 'Org. Evento', insertions: []},
                        {type: 'Exposição', insertions: []},
                    ],
                    [ // Criterio 7
                        {type: 'Seminários', insertions: []},
                        {type: 'Encontros', insertions: []},
                        {type: 'Colóquios', insertions: []},
                        {type: 'Oficinas', insertions: []},
                        {type: 'Debates', insertions: []},
                        {type: 'Org. Mesas', insertions: []},
                        {type: 'Aval. Trabalhos', insertions: []},
                    ]
                ]
            });
            return {
                professors: newProfs,
                id_counter: prevState.id_counter + 1,
            }
        })
    }

    removeProfessor(id) {
        this.setState(function(prevState, props) {
            var newProfs = prevState.professors.filter(function(prof) {
                if (prof.id !== id) return prof;
            });
            return {professors: newProfs};
        });
    }

    getCriterionInsertions(profId, criterionIdx, type) {
        for (var i = 0; i < this.state.professors.length; i++) {
            if (this.state.professors[i].id == profId) {
                var types = this.state.professors.filter(prof => prof.id === profId)[0].criterions[criterionIdx];
                for (var j = 0; j < types.length; j++) {
                    if (types[j].type == type) return types[j].insertions;
                }
            }
        }
    }

    clearAllCriterionInsertions(profId, criterionIdx, type) {
        for (var i = 0; i < this.state.professors.length; i++) {
            if (this.state.professors[i].id == profId) {
                this.setState(function(prevState, props) {
                    var newProfs = prevState.professors;
                    var newProfCriteria = newProfs.criterions[criterionIdx].filter(function(ins) {
                        return(ins.type != type);
                    });
                });
            }
        }
    }

    addCriterionInsertions(profId, criterionIdx, type, qnt) {
        this.setState(function(prevState, props) {
            for (var i=0; i < prevState.professors.length; i++) {
                if (prevState.professors[i].id == profId) {
                    var prof = prevState.professors[i];
                    var insType = {};
                    var typeIdx = 0;
                    for (var j = 0; j < prof.criterions[criterionIdx].length; j++) {
                        if (prof.criterions[criterionIdx][j].type == type) {
                            insType = prof.criterions[criterionIdx][j];
                            typeIdx = j;
                            break;
                        }
                    }

                    var insertions = insType.insertions;

                    for (var j = 0; j < qnt; j++) {
                        insertions.push('');
                    }

                    insType.insertions = insertions;
                    prof.criterions[criterionIdx][typeIdx] = insType;
                    var newProfs = prevState.professors;
                    newProfs[i] = prof;

                    return {professors: newProfs};
                }
            }
        });
    }

    removeCriterionInsertions(profId, criterionIdx, type, qnt) {
        this.setState(function(prevState, props) {
            for (var i=0; i < prevState.professors.length; i++) {
                if (prevState.professors[i].id == profId) {
                    var prof = prevState.professors[i];
                    var insType = {};
                    var typeIdx = 0;
                    for (var j = 0; j < prof.criterions[criterionIdx].length; j++) {
                        if (prof.criterions[criterionIdx][j].type == type) {
                            insType = prof.criterions[criterionIdx][j];
                            typeIdx = j;
                            break;
                        }
                    }

                    var insertions = insType.insertions;

                    for (var j = 0; j < qnt; j++) {
                        insertions.pop();
                    }

                    insType.insertions = insertions;
                    prof.criterions[criterionIdx][typeIdx] = insType;
                    var newProfs = prevState.professors;
                    newProfs[i] = prof;

                    return {professors: newProfs};
                }
            }
        });
    }

    changeProfessorFieldNumber(profId, criterion, type, value) {
        var criterion_idx = criterion - 1;

        for (var i = 0; i < this.state.professors.length; i++) {
            if (this.state.professors[i].id == profId) {
                // Professor found
                var currentInsertions = this.getCriterionInsertions(profId, criterion_idx, type);
                if (value <= 0) {
                    this.removeCriterionInsertions(profId, criterion_idx, type, currentInsertions.length);
                } else if(currentInsertions.length < value) {
                    this.addCriterionInsertions(profId, criterion_idx, type, value - currentInsertions.length);
                } else if(currentInsertions.length > value) {
                    this.removeCriterionInsertions(profId, criterion_idx, type, currentInsertions.length - value);
                }
            }
        }
    }

    changeInsertion(profId, critIdx, typeIdx, insIdx, value) {
        this.setState(function(prevState, props) {
            for (var i=0; i < prevState.professors.length; i++) {
                if (prevState.professors[i].id == profId) {
                    var prof = prevState.professors[i];
                    prof.criterions[critIdx][typeIdx].insertions[insIdx] = value;

                    var newProfs = prevState.professors;
                    newProfs[i] = prof;

                    return {professors: newProfs};
                }
            }
        });
    }

    setStep(stp) {
        this.setState({curr_step:stp});
    }

    submit(state) {
        var parsedUrl = new URL(window.location.href);
        const result = Object.assign({}, this.state, 
                        {"state": state},
                        {'index': parsedUrl.searchParams.get('index')}, 
                        {'form_type': parsedUrl.searchParams.get('form_type')});
        const data = JSON.stringify(result);
        const config = {
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: data
        };
        var self = this;
        fetch("http://localhost:3002/admin/formulario_avaliacao_final/", config)
            .then(function(res) {
                return res.json();
            })
            .then(function(json){
                const finalJson = JSON.parse(json);
                if (finalJson.success) {
                    self.setState({curr_step: 4});
                } else {
                    self.setState({curr_step: 5});
                }
            })
            .catch(function(e) {
                console.error(e);
            });
    }

    getInformation() {
        var parsedUrl = new URL(window.location.href);
        const result = {'groupAccount': this.state.groupAccount, 
                        'index': parsedUrl.searchParams.get('index'), 
                        'id': parsedUrl.searchParams.get('id'),
                        'form_type': parsedUrl.searchParams.get('form_type')};
        const data = JSON.stringify(result);
        const config = {
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: data
        };
        var self = this;
        fetch("http://localhost:3002/admin/informacoes_formulario/", config)
            .then(function(res) {
                return res.json();
            })
            .then(function(json){
                const finalJson = JSON.parse(json);
                self.setState(finalJson);
            })
            .catch(function(e) {
                console.error(e);
            });
    }

    getProfessors() {
        const config = {
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            method: 'GET',
        };
        var self = this;
        fetch(`http://localhost:3002/admin/lista_professores/`, config)
            .then(function(res) {
                return res.json();
            })
            .then(function(json){
                const finalJson = JSON.parse(json);
                self.setState({ professorsList : finalJson.map(prof => prof.nome) });
            })
            .catch(function(e) {
                console.error(e);
            });
    }

    render() {
        switch(this.state.curr_step) {
            case 1:
                return <DadosBase currentState={this.state}
                                  changeName={this.changeName}
                                  changeCoordinator={this.changeCoordinator}
                                  changeYear={this.changeYear}
                                  changeGrad={this.changeGrad}
                                  changePosGrad={this.changePosGrad}
                                  changeGoals={this.changeGoals}
                                  nextStep={this.nextStep} />
            case 2:
                return <CadastroProfessores nextStep={this.nextStep}
                                            previousStep={this.previousStep}
                                            addProfessor={this.addProfessor}
                                            removeProfessor={this.removeProfessor}
                                            professors={this.state.professors} 
                                            professorsList={this.state.professorsList} />
            case 3:
                return <Avaliacao previousStep={this.previousStep}
                                  professors={this.state.professors}
                                  changeProfessorFieldNumber={this.changeProfessorFieldNumber}
                                  changeInsertion={this.changeInsertion}
                                  submit={this.submit}
                                  getInformation={this.getInformation}/>
            case 4:
                return <Success/>
            case 5:
                return <Fail/>
        }
    }
}

ReactDOM.render(<Application/>, app);
