from .Banca import Banca
from .Diploma import Diploma
from .Orientacao import Orientacao
from .Producao import Producao
from .Projeto import Projeto
from .Tecnica import Tecnica
from .Patente import Patente
from util.Global import *

from datetime import datetime

class Pesquisador:
    
    def __init__(self, xml):
        self.id = self.g_id(xml)
        self.nome = self.g_nome(xml)
        
        self.citacoes = self.g_citacoes(xml)
        self.build_citations()
        # self.colaboracoes = self.build_colabs()
        
        self.cidade = self.g_cidade(xml)
        self.estado = self.g_estado(xml)
        self.pais = self.g_pais(xml)
        self.orcid = self.g_orcid(xml)
        self.resumo = self.g_resumo(xml)
        self.date = self.g_date(xml)
        self.diplomas = self.g_diplomas(xml)
        self.projetos = self.g_projetos(xml)
        self.producoes = self.g_producoes(xml)
        self.bancas = self.g_bancas(xml)
        self.orientacoes = self.g_orientacoes(xml)
        self.tecnicas = self.g_tecnicas(xml)
        self.patentes = self.g_patentes(xml)
        
        # self.find_qualis()
    
    def __str__(self):
        s =  'ID_LATTES: ' + self.id + '\n'
        s += 'NOME: ' + self.nome + '\n'
        s += 'C/S/P: ' + self.cidade + '/' + self.estado + '/' + self.pais + '\n'
        s += 'ORCID: ' + self.orcid + '\n' 
        s += 'ÚLTIMA ATUALIZAÇÃO: ' + self.date.strftime('%d/%m/%Y %H:%M:%S') + '\n'
        s += 'ORIENTAÇÕES: ' + str(len(self.orientacoes)) + ' (' + self.g_freq_orientacoes() + ')\n'
        s += 'BANCAS: ' + str(len(self.bancas)) + ' (' + self.g_freq_bancas() + ')\n'
        s += 'PROJETOS: ' + str(len(self.projetos)) + ' (' + self.g_freq_projetos() + ')\n'
        s += 'PRODUÇÕES: ' + str(len(self.producoes)) + ' (' + self.g_freq_producoes() + ')'
        return s        
    
    def g_freq_producoes(self):
        pe = re = re_e = co = li = ca = lo = 0
        for i in self.producoes:
            if i.tipo == LocalTipo.PERIODICO:
                pe += 1
            elif i.tipo == LocalTipo.RESUMO:
                re += 1
            elif i.tipo == LocalTipo.RESUMO_EXPANDIDO:
                re_e += 1
            elif i.tipo == LocalTipo.CONFERENCIA:
                co += 1
            elif i.tipo == LocalTipo.LIVRO:
                li += 1
            elif i.tipo == LocalTipo.CAPITULO_LIVRO:
                ca += 1
            elif i.tipo == LocalTipo.LIVRO_ORGANIZADO:
                lo += 1
        return 'pe=' + str(pe) + ' / re=' + str(re) + ' / re_e=' + str(re_e) + ' / co=' + str(co) + ' / li=' + str(li) + ' / ca=' + str(ca) + ' / lo=' + str(lo)

    def g_freq_projetos(self):
        en = pe = ex = o = 0
        for p in self.projetos:
            if p.tipo == ProjetoTipo.ENSINO:
                en += 1
            elif p.tipo == ProjetoTipo.PESQUISA:
                pe += 1
            elif p.tipo == ProjetoTipo.EXTENSAO:
                ex += 1
            elif p.tipo == ProjetoTipo.OUTRA:
                o += 1
        return 'en=' + str(en) + ' / p=' + str(pe) + ' / ex=' + str(ex) + ' / o=' + str(o)

    def g_freq_bancas(self):
        g = m = d = qm = qd = 0
        for b in self.bancas:
            if b.tipo == BancaTipo.GRADUACAO:
                g += 1
            elif b.tipo == BancaTipo.MESTRADO:
                m += 1
            elif b.tipo == BancaTipo.DOUTORADO:
                d += 1
            elif b.tipo == BancaTipo.QUALIFICACAO_MESTRADO:
                qm += 1
            elif b.tipo == BancaTipo.QUALIFICACAO_DOUTORADO:
                qd += 1
        return 'g=' + str(g) + ' / m=' + str(m) + ' / d=' + str(d) + ' / qm=' + str(qm) + ' / qd=' + str(qd)
     
    def g_freq_orientacoes(self):
        g = m = d = ic = mo = o = 0
        for ori in self.orientacoes:
            if ori.tipo == OrientacaoTipo.GRADUACAO:
                g += 1
            elif ori.tipo == OrientacaoTipo.MESTRADO:
                m += 1
            elif ori.tipo == OrientacaoTipo.DOUTORADO:
                d += 1
            elif ori.tipo == OrientacaoTipo.INICIACAO_CIENTIFICA:
                ic += 1
            elif ori.tipo == OrientacaoTipo.MONOGRAFIA:
                mo += 1
            elif ori.tipo == OrientacaoTipo.OUTRA:
                o += 1
        return 'g=' + str(g) + ' / m=' + str(m) + ' / d=' + str(d) + ' / ic=' + str(ic) + ' / mo=' + str(mo) + ' / o=' + str(o)
            
    def g_id(self, xml) -> str:
        return xml.attrib['NUMERO-IDENTIFICADOR']
    
    def g_nome(self, xml) -> str:
        return xml.find('DADOS-GERAIS').attrib['NOME-COMPLETO']
    
    def g_citacoes(self, xml) -> list:
        return xml.find('DADOS-GERAIS').attrib['NOME-EM-CITACOES-BIBLIOGRAFICAS'].split(';')
    
    def build_citations(self):
        res = []    

        for c in self.citacoes:
            s = c.split(',')

            if len(s) > 1:
                new_name = s[1] + ' ' + s[0]
                new_name = " ".join(new_name.split()).strip()
                res.append(new_name) # add by changing text order
                
                new_name = new_name.upper()
                res.append(new_name) # add by captilizing the text
                
                res.append(" ".join(c.split()).strip().upper()) # add by captilizing original citation
        
        self.citacoes.extend(res)
        self.citacoes = list(set(self.citacoes))
        
        try:
            self.citacoes.remove(self.nome)
        except:
            pass
        finally:
            self.citacoes.insert(0, self.nome) # necessário inserir somente aqui (full name pode surgir artificialmente)

    
    # implementar ao final
    def build_colabs() -> dict:
        pass
        
    
    def g_cidade(self, xml) -> str:
        return xml.find('DADOS-GERAIS').attrib['CIDADE-NASCIMENTO']
    
    def g_estado(self, xml) -> str:
        return xml.find('DADOS-GERAIS').attrib['UF-NASCIMENTO']
    
    def g_pais(self, xml) -> str:
        return xml.find('DADOS-GERAIS').attrib['PAIS-DE-NASCIMENTO']
    
    def g_orcid(self, xml) -> str:
        return xml.find('DADOS-GERAIS').attrib['ORCID-ID'] if 'ORCID-ID' in xml.find('DADOS-GERAIS') else ''
    
    def g_resumo(self, xml) -> str:
        return xml.find('DADOS-GERAIS').find('RESUMO-CV').attrib['TEXTO-RESUMO-CV-RH']
    
    def g_date(self, xml) -> datetime:
        d = xml.attrib['DATA-ATUALIZACAO']
        t = xml.attrib['HORA-ATUALIZACAO']
        return datetime.strptime(d[:2] + '/' + d[2:4] + '/' + d[4:] + ' ' + t[:2] + ':' 
                                 + t[2:4] + ':' + t[4:], '%d/%m/%Y %H:%M:%S')
    
    def g_diplomas(self, xml) -> list:
        ds = xml.find('DADOS-GERAIS').find('FORMACAO-ACADEMICA-TITULACAO')
        res = []
        for d in ds.findall('GRADUACAO'):
            res.append(Diploma(d.attrib['NOME-CURSO'], DiplomaTipo.GRADUACAO, d.attrib['STATUS-DO-CURSO'], 
                             d.attrib['TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO'], d.attrib['NOME-DO-ORIENTADOR'], 
                             d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))
            
        for d in ds.findall('MESTRADO'):
            res.append(Diploma(d.attrib['NOME-CURSO'], DiplomaTipo.MESTRADO, d.attrib['STATUS-DO-CURSO'], 
                               d.attrib['TITULO-DA-DISSERTACAO-TESE'], d.attrib['NOME-COMPLETO-DO-ORIENTADOR'], 
                               d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))
        
        for d in ds.findall('DOUTORADO'):
            res.append(Diploma(d.attrib['NOME-CURSO'], DiplomaTipo.DOUTORADO, d.attrib['STATUS-DO-CURSO'], 
                               d.attrib['TITULO-DA-DISSERTACAO-TESE'], d.attrib['NOME-COMPLETO-DO-ORIENTADOR'], 
                               d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))
        
        for d in ds.findall('POS-DOUTORADO'):
            res.append(Diploma(None, DiplomaTipo.POS_DOUTORADO, d.attrib['STATUS-DO-CURSO'], 
                               None, None, 
                               d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))
        
        for d in ds.findall('ESPECIALIZACAO'):
            res.append(Diploma(d.attrib['NOME-CURSO'], DiplomaTipo.ESPECIALIZACAO, d.attrib['STATUS-DO-CURSO'], 
                               d.attrib['TITULO-DA-MONOGRAFIA'], d.attrib['NOME-DO-ORIENTADOR'], 
                               d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))
            
        for d in ds.findall('CURSO-TECNICO-PROFISSIONALIZANTE'):
            res.append(Diploma(d.attrib['NOME-CURSO'] if len(d.attrib['NOME-CURSO']) > 0 else 'Curso técnico / profissionalizante', 
                               DiplomaTipo.TECNICO, d.attrib['STATUS-DO-CURSO'], 
                               None, None, 
                               d.attrib['NOME-INSTITUICAO'], d.attrib['ANO-DE-INICIO'], d.attrib['ANO-DE-CONCLUSAO']))       
        
        return res
    
    def g_projetos(self, xml) -> list:
        ds = xml.find('DADOS-GERAIS').find('ATUACOES-PROFISSIONAIS').findall('ATUACAO-PROFISSIONAL')
        
        res = []
        for d1 in ds:
            d2 = d1.find('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')
            if d2:
                for d3 in d2.findall('PARTICIPACAO-EM-PROJETO'):
                    for p in d3.findall('PROJETO-DE-PESQUISA'):
                        tipo = ProjetoTipo.ENSINO if 'ENSINO' in p.attrib['NATUREZA'] else ProjetoTipo.PESQUISA if 'PESQUISA' in p.attrib['NATUREZA'] else ProjetoTipo.EXTENSAO if 'EXTENSAO' in p.attrib['NATUREZA'] else ProjetoTipo.OUTRA
                        res.append(Projeto(tipo, p.attrib['NOME-DO-PROJETO'], p.attrib['SITUACAO'], p.attrib['ANO-INICIO'], p.attrib['ANO-FIM']))
        return res
    
    def g_bancas(self, xml) -> list:
        ds = xml.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')
        res = []
        
        if ds != None:
            for d in ds.findall('PARTICIPACAO-EM-BANCA-DE-GRADUACAO'):
                aux1 = d.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO')
                aux2 = d.find('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO')
                res.append(Banca(BancaTipo.GRADUACAO, aux1.attrib['TITULO'], aux2.attrib['NOME-DO-CANDIDATO'],
                           aux2.attrib['NOME-INSTITUICAO'], aux2.attrib['NOME-CURSO'], aux1.attrib['ANO']))

            for d in ds.findall('PARTICIPACAO-EM-BANCA-DE-MESTRADO'):
                aux1 = d.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO')
                aux2 = d.find('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO')
                res.append(Banca(BancaTipo.MESTRADO, aux1.attrib['TITULO'], aux2.attrib['NOME-DO-CANDIDATO'],
                           aux2.attrib['NOME-INSTITUICAO'], aux2.attrib['NOME-CURSO'], aux1.attrib['ANO']))

            for d in ds.findall('PARTICIPACAO-EM-BANCA-DE-DOUTORADO'):
                aux1 = d.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO')
                aux2 = d.find('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO')
                res.append(Banca(BancaTipo.DOUTORADO, aux1.attrib['TITULO'], aux2.attrib['NOME-DO-CANDIDATO'],
                           aux2.attrib['NOME-INSTITUICAO'], aux2.attrib['NOME-CURSO'], aux1.attrib['ANO']))

            for d in ds.findall('PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO'):
                aux1 = d.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO')
                aux2 = d.find('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO')

                res.append(Banca(BancaTipo.QUALIFICACAO_MESTRADO if 'mestrado' in aux1.attrib['NATUREZA'] else BancaTipo.QUALIFICACAO_DOUTORADO, 
                           aux1.attrib['TITULO'], aux2.attrib['NOME-DO-CANDIDATO'], 
                           aux2.attrib['NOME-INSTITUICAO'], aux2.attrib['NOME-CURSO'], aux1.attrib['ANO']))
        return res
    
    def g_orientacoes(self, xml) -> list:
        
        #Trabalhar orientações concluídas
        
        ds = xml.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS')
        res = []
        
        if ds != None:
            for d in ds.findall('OUTRAS-ORIENTACOES-CONCLUIDAS'):
                tag = d.find('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
                tag2 = d.find('DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
                res.append(Orientacao(tag.attrib['TITULO'], tag2.attrib['NOME-DO-ORIENTADO'], tag2.attrib['NOME-DA-INSTITUICAO'], tag2.attrib['NOME-DO-CURSO'], OrientacaoTipo.GRADUACAO if 'GRADUACAO' in tag.attrib['NATUREZA'] else OrientacaoTipo.INICIACAO_CIENTIFICA if 'INICIACAO_CIENTIFICA' in tag.attrib['NATUREZA'] else OrientacaoTipo.MONOGRAFIA if 'MONOGRAFIA' in tag.attrib['NATUREZA'] else OrientacaoTipo.OUTRA, 'CONCLUIDO', tag.attrib['ANO'], PapelTipo.ORIENTADOR))

            for d in ds.findall('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO'):
                tag = d.find('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
                tag2 = d.find('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
                res.append(Orientacao(tag.attrib['TITULO'], tag2.attrib['NOME-DO-ORIENTADO'], tag2.attrib['NOME-DA-INSTITUICAO'], tag2.attrib['NOME-DO-CURSO'], OrientacaoTipo.MESTRADO, 'CONCLUIDO', tag.attrib['ANO'], PapelTipo.ORIENTADOR if 'ORIENTADOR_PRINCIPAL' in tag2.attrib['TIPO-DE-ORIENTACAO'] else PapelTipo.COORIENTADOR))

            for d in ds.findall('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO'):
                tag = d.find('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
                tag2 = d.find('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
                res.append(Orientacao(tag.attrib['TITULO'], tag2.attrib['NOME-DO-ORIENTADO'], tag2.attrib['NOME-DA-INSTITUICAO'], tag2.attrib['NOME-DO-CURSO'], OrientacaoTipo.DOUTORADO, 'CONCLUIDO', tag.attrib['ANO'], PapelTipo.ORIENTADOR if 'ORIENTADOR_PRINCIPAL' in tag2.attrib['TIPO-DE-ORIENTACAO'] else PapelTipo.COORIENTADOR))
            
        
        # Trabalhar orientações em andamento
        ds = xml.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO')
        
        if ds != None:
            for d in ds.findall('ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA'):
                tag = d.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')
                tag2 = d.find('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.INICIACAO_CIENTIFICA, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR))

            for d in ds.findall('ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO'):
                tag = d.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO')
                tag2 = d.find('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO')
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.GRADUACAO, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR))

            for d in ds.findall('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
                tag = d.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')
                tag2 = d.find('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')            
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.MESTRADO, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR if 'ORIENTADOR_PRINCIPAL' in tag2.attrib['TIPO-DE-ORIENTACAO'] else PapelTipo.COORIENTADOR))

            for d in ds.findall('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
                tag = d.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')
                tag2 = d.find('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')            
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.DOUTORADO, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR if 'ORIENTADOR_PRINCIPAL' in tag2.attrib['TIPO-DE-ORIENTACAO'] else PapelTipo.COORIENTADOR))

            for d in ds.findall('OUTRAS-ORIENTACOES-EM-ANDAMENTO'):
                tag = d.find('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO') 
                tag2 = d.find('DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.OUTRA, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR))


            for d in ds.findall('ORIENTACAO-EM-ANDAMENTO-DE-APERFEICOAMENTO-ESPECIALIZACAO'):
                tag = d.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-APERFEICOAMENTO-ESPECIALIZACAO')
                tag2 = d.find('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-APERFEICOAMENTO-ESPECIALIZACAO')
                res.append(Orientacao(tag.attrib['TITULO-DO-TRABALHO'], tag2.attrib['NOME-DO-ORIENTANDO'], tag2.attrib['NOME-INSTITUICAO'], tag2.attrib['NOME-CURSO'], OrientacaoTipo.MONOGRAFIA, 'EM_ANDAMENTO', tag.attrib['ANO'], PapelTipo.ORIENTADOR))
        
        return res
    
    
    def g_producoes(self, xml) -> list:
        
        # Periódicos
        
        ds = xml.find('PRODUCAO-BIBLIOGRAFICA')
        res = []
        
        dt = ds.find('ARTIGOS-PUBLICADOS')
        if dt != None:
            for d in dt.findall('ARTIGO-PUBLICADO'):
                tag1 = d.find('DADOS-BASICOS-DO-ARTIGO')
                tag2 = d.find('DETALHAMENTO-DO-ARTIGO')
                autores = []
                for a in d.findall('AUTORES'):
                    autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])

                res.append(Producao(tag1.attrib['TITULO-DO-ARTIGO'], autores, tag2.attrib['TITULO-DO-PERIODICO-OU-REVISTA'], 
                                    None, LocalTipo.PERIODICO, tag1.attrib['ANO-DO-ARTIGO'], tag2.attrib['ISSN']))

        
        # Conferências, resumos e resumos expandidos
        
        dt = ds.find('TRABALHOS-EM-EVENTOS')
        if dt != None:
            for d in dt.findall('TRABALHO-EM-EVENTOS'):
                tag1 = d.find('DADOS-BASICOS-DO-TRABALHO')
                tag2 = d.find('DETALHAMENTO-DO-TRABALHO')
                autores = []
                for a in d.findall('AUTORES'):
                    autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])

                res.append(Producao(tag1.attrib['TITULO-DO-TRABALHO'], autores, tag2.attrib['NOME-DO-EVENTO'], None,
                                    LocalTipo.CONFERENCIA if 'COMPLETO' in tag1.attrib['NATUREZA'] else LocalTipo.RESUMO if 'RESUMO' == tag1.attrib['NATUREZA'] else LocalTipo.RESUMO_EXPANDIDO if 'RESUMO_EXPANDIDO' == tag1.attrib['NATUREZA'] else "",                                 
                                    tag1.attrib['ANO-DO-TRABALHO']))  

        
        # Capítulo de livros
        
        ds = xml.find('PRODUCAO-BIBLIOGRAFICA').find('LIVROS-E-CAPITULOS')
        
        if ds != None:
            dt = ds.find('CAPITULOS-DE-LIVROS-PUBLICADOS')
            if dt != None:
                for d in dt.findall('CAPITULO-DE-LIVRO-PUBLICADO'):
                    tag1 = d.find('DADOS-BASICOS-DO-CAPITULO')
                    tag2 = d.find('DETALHAMENTO-DO-CAPITULO')
                    autores = []
                    for a in d.findall('AUTORES'):
                        autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])

                    res.append(Producao(tag1.attrib['TITULO-DO-CAPITULO-DO-LIVRO'], autores, tag2.attrib['TITULO-DO-LIVRO'], 
                                        None, LocalTipo.CAPITULO_LIVRO,
                                        tag1.attrib['ANO']))  

        # Livro publicado ou organização de livro
        
            dt = ds.find('LIVROS-PUBLICADOS-OU-ORGANIZADOS')
            if dt != None:
                for d in dt.findall('LIVRO-PUBLICADO-OU-ORGANIZADO'):
                    tag1 = d.find('DADOS-BASICOS-DO-LIVRO')
                    tag2 = d.find('DETALHAMENTO-DO-LIVRO')
                    autores = []
                    for a in d.findall('AUTORES'):
                        autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])

                    res.append(Producao(tag1.attrib['TITULO-DO-LIVRO'], autores, tag2.attrib['NOME-DA-EDITORA'], 
                                        None, LocalTipo.LIVRO if 'LIVRO_PUBLICADO' == tag1.attrib['TIPO'] else LocalTipo.LIVRO_ORGANIZADO if 'LIVRO_ORGANIZADO_OU_EDICAO' == tag1.attrib['TIPO'] else "", tag1.attrib['ANO']))  
        
        return res   
    
    def find_pos(self, tag, res):
        for i, val in enumerate(res):
            if tag == val[0].tipo:
                return i, True
        return None, False

    
    def g_tecnicas(self, xml) -> list:
        
        pt = xml.find('PRODUCAO-TECNICA')
        res = []
        
        if pt != None:
            for t in list(pt):
                if 'DEMAIS-TIPO' not in t.tag:
                    if len(res) > 0:
                        pos, flag = self.find_pos(t.tag, res)
                        v = list(t[0].attrib.values())
                        if flag:
                            res[pos].append(Tecnica(t.tag, (v[1], v[2])))
                        else:
                            res.append([Tecnica(t.tag, (v[1], v[2]))])
                    else:                    
                        v = list(t[0].attrib.values())
                        res.append([Tecnica(t.tag, (v[1], v[2]))])
                else:
                    for t2 in list(t):
                        if len(res) > 0:
                            pos, flag = self.find_pos(t2.tag, res)
                            v = list(t2[0].attrib.values())
                            if flag:
                                res[pos].append(Tecnica(t2.tag, (v[1], v[2])))
                            else:
                                res.append([Tecnica(t2.tag, (v[1], v[2]))])
                        else:                    
                            v = list(t2[0].attrib.values())
                            res.append([Tecnica(t2.tag, (v[1], v[2]))])
        
        return res
    
    
    
    def g_patentes(self, xml):
        pt = xml.find('PRODUCAO-TECNICA')
        res = []
        
        if pt != None:
            patentes = pt.findall('PATENTE')
            for p in patentes:
                tag1 = p.find('DADOS-BASICOS-DA-PATENTE')
                tag2 = p.find('DETALHAMENTO-DA-PATENTE').find('REGISTRO-OU-PATENTE')
                autores = []
                for a in p.findall('AUTORES'):
                    autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])
                
                res.append(Patente(tag1.attrib['TITULO'], tag2.attrib['DATA-PEDIDO-DE-DEPOSITO'], tag2.attrib['DATA-DE-CONCESSAO'], tag1.attrib['ANO-DESENVOLVIMENTO'], autores, PatenteTipo.ATIVO))
                
            softwares = pt.findall('SOFTWARE')
            for s in softwares:
                tag2 = s.find('DETALHAMENTO-DO-SOFTWARE').find('REGISTRO-OU-PATENTE')
                if tag2 != None:
                    tag1 = s.find('DADOS-BASICOS-DO-SOFTWARE')
                
                    autores = []
                    for a in s.findall('AUTORES'):
                        autores.append(a.attrib['NOME-COMPLETO-DO-AUTOR'])
                        
                    res.append(Patente(tag1.attrib['TITULO-DO-SOFTWARE'], tag2.attrib['DATA-PEDIDO-DE-DEPOSITO'], tag2.attrib['DATA-DE-CONCESSAO'], tag1.attrib['ANO'], autores, PatenteTipo.SOFTWARE))
        
        
        return res