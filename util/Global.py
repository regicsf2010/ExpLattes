from enum import Enum

# Enums
class Qualis(Enum):
    CONFERENCIA = 1
    PERIODICO = 2
    
class DiplomaTipo(Enum):
    GRADUACAO = 1
    MESTRADO = 2
    DOUTORADO = 3
    POS_DOUTORADO = 4
    ESPECIALIZACAO = 5
    TECNICO = 6
    
class ProjetoTipo(Enum):
    ENSINO = 1
    PESQUISA = 2
    EXTENSAO = 3
    OUTRA = 4
    
class LocalTipo(Enum):
    CONFERENCIA = 1
    PERIODICO = 2
    RESUMO = 3    
    RESUMO_EXPANDIDO = 4
    LIVRO = 5
    CAPITULO_LIVRO = 6
    LIVRO_ORGANIZADO = 7
        
class BancaTipo(Enum):
    GRADUACAO = 1
    MESTRADO = 2
    DOUTORADO = 3    
    QUALIFICACAO_MESTRADO = 4
    QUALIFICACAO_DOUTORADO = 5
    
class OrientacaoTipo(Enum):
    GRADUACAO = 1
    MESTRADO = 2
    DOUTORADO = 3    
    INICIACAO_CIENTIFICA = 4
    MONOGRAFIA = 5
    OUTRA = 6
    
class PapelTipo(Enum):
    ORIENTADOR = 1
    COORIENTADOR = 2
    
class PatenteTipo(Enum):
    ATIVO = 1
    SOFTWARE = 2    