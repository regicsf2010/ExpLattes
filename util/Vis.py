from util.Global import *

from wordcloud import WordCloud, STOPWORDS
from PIL import Image

import util.Functions as fun
import matplotlib.pyplot as plt
import numpy as np
import nltk

def plot_bancas(data, w = 19, h = 8):
    r = fun.get_freq_based_on_year(data)
    
    title = str(sum(r.values())) + ' bancas em ' + (str(int(max(r)) - int(min(r)) + 1) if sum(r.values()) != 0 else '0') + ' anos'
    
    fig, ax = plt.subplots(figsize = (w, h))
    
    keys = sorted(r)
    values = list(map(r.get, keys))

    rects = ax.bar(keys, values, color = '#2bbcd6', alpha = 1)

    ax.set_title(title, fontsize = 'x-large')
    ax.set_xlabel('Ano', fontsize = 'xx-large')
    ax.set_ylabel('Frequência', fontsize = 'xx-large')
    
    ax.tick_params(axis = 'both', which = 'major', labelrotation = 90, labelsize = 'xx-large')
    ax.grid(axis = 'x', color = 'lightblue', linestyle = '--')
    
    ax.set_ylim(0, max(values) + 1.5 if bool(values) else 10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, labelleft = False)
    
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * h, '%d' % int(h), ha = 'center', va = 'bottom', fontsize = 'x-large')
        
    plt.tight_layout()
    
    
    
def plot_producoes(data, w = 19, h = 8):
    r = fun.get_freq_based_on_year(data)
    
    title = str(sum(r.values())) + ' publicações em ' + str(int(max(r)) - int(min(r)) + 1) + ' anos'
    
    fig, ax = plt.subplots(figsize = (w, h))
    
    keys = sorted(r)
    values = list(map(r.get, keys))

    rects = ax.bar(keys, values, color = '#2bbcd6', alpha = 1)

    ax.set_title(title + '\n', fontsize = 'x-large')
    ax.set_xlabel('Ano', fontsize = 'xx-large')
    ax.set_ylabel('Frequência', fontsize = 'xx-large')
    ax.tick_params(axis = 'both', which = 'major', labelrotation = 90, labelsize = 'xx-large')
    ax.grid(axis = 'x', color = 'lightblue', linestyle = '--')
    ax.set_ylim(0, max(values) + 1.5 if bool(values) else 10)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, labelleft = False)
    
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * h, '%d' % int(h), ha = 'center', va = 'bottom', fontsize = 'x-large')

    plt.tight_layout()
        
    
def plot_projetos(data, w = 19, h = 8):
    r = fun.get_freq_based_on_year(data)
    
    title = str(sum(r.values())) + ' projetos em ' + str(int(max(r)) - int(min(r)) + 1) + ' anos'
    
    fig, ax = plt.subplots(figsize = (w, h))
    
    keys = sorted(r)
    values = list(map(r.get, keys))

    rects = ax.bar(keys, values, color = '#2bbcd6', alpha = 1)

    ax.set_title(title, fontsize = 'x-large')
    ax.set_xlabel('Ano', fontsize = 'xx-large')
    ax.set_ylabel('Frequência', fontsize = 'xx-large')
    ax.tick_params(axis = 'both', which = 'major', labelrotation = 90, labelsize = 'xx-large')
    ax.grid(axis = 'x', color = 'lightblue', linestyle = '--')
    ax.set_ylim(0, max(values) + 1.5 if bool(values) else 10)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, labelleft = False)
    
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * h, '%d' % int(h), ha = 'center', va = 'bottom', fontsize = 'x-large')

    # ax.axis('off')                                                                     
    plt.tight_layout()        

def plot_orientacoes(data, w = 19, h = 8):
    r = fun.get_freq_based_on_year(data)
    
    title = str(sum(r.values())) + ' orientações em ' + str(int(max(r)) - int(min(r)) + 1) + ' anos'
    
    fig, ax = plt.subplots(figsize = (w, h))
    
    keys = sorted(r)
    values = list(map(r.get, keys))

    rects = ax.bar(keys, values, color = '#2bbcd6', alpha = 1)

    ax.set_title(title, fontsize = 'x-large')
    ax.set_xlabel('Ano', fontsize = 'xx-large')
    ax.set_ylabel('Frequência', fontsize = 'xx-large')
    ax.tick_params(axis = 'both', which = 'major', labelrotation = 90, labelsize = 'xx-large')
    ax.grid(axis = 'x', color = 'lightblue', linestyle = '--')
    ax.set_ylim(0, max(values) + 1.5 if bool(values) else 10)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left = False, labelleft = False)
    
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * h, '%d' % int(h), ha = 'center', va = 'bottom', fontsize = 'x-large')

    # ax.axis('off')                                                                     
    # ax.axis('off')
    plt.tight_layout()
        
def plot_radar_orientacoes(data, w = 15, h = 12):
    r = [ fun.get_freq_based_on_year(data, OrientacaoTipo.GRADUACAO), 
           fun.get_freq_based_on_year(data, OrientacaoTipo.MESTRADO),
           fun.get_freq_based_on_year(data, OrientacaoTipo.DOUTORADO),
           fun.get_freq_based_on_year(data, OrientacaoTipo.INICIACAO_CIENTIFICA),
           fun.get_freq_based_on_year(data, OrientacaoTipo.MONOGRAFIA),
           fun.get_freq_based_on_year(data, OrientacaoTipo.OUTRA)]
    
    title = 'Orientação'
    labels = ['Graduação', 'Mestrado', 'Doutorado', 'IC', 'Monografia', 'Outra']
    
    fig, ax = plt.subplots(figsize = (w, h), subplot_kw = dict(polar = True))
    
    vals = np.array([])

    for v in r:
        vals = np.append(vals, sum(v.values()))

    if vals.sum() != 0:
        vals = vals / vals.sum() * 100

    angles = np.linspace(start = 0, stop = 2 * np.pi, num = len(vals) + 1).tolist()
    vals = np.append(vals, vals[:1])
    angles[-1] = angles[0]

    ax.plot(angles, vals, color = 'blue', label = 'Total (%)')
    ax.fill(angles, vals, facecolor = 'blue', alpha = 0.1)

    ax.legend(fontsize = 'large')
    ax.set_title(title, size = 'xx-large', y = 1.08)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels = labels, fontsize = 'x-large')
    ax.set_ylim(0, 100)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle == 0:
            label.set_horizontalalignment('left')
        elif angle == np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('center')

    ax.set_rlabel_position(45)
    ax.set_facecolor('#FAFAFA')

    plt.tight_layout()     
        
def plot_radar_bancas(data, w = 15, h = 12):
    r = [fun.get_freq_based_on_year(data, BancaTipo.GRADUACAO),
           fun.get_freq_based_on_year(data, BancaTipo.MESTRADO),
           fun.get_freq_based_on_year(data, BancaTipo.DOUTORADO),
           fun.get_freq_based_on_year(data, BancaTipo.QUALIFICACAO_MESTRADO),
           fun.get_freq_based_on_year(data, BancaTipo.QUALIFICACAO_DOUTORADO)]
    
    title = 'Banca'
    labels = ['Graduação', 'Mestrado', 'Doutorado', 'Qualis Mestrado', 'Qualis Doutorado']
    
    fig, ax = plt.subplots(figsize = (w, h), subplot_kw = dict(polar = True))
    
    vals = np.array([])

    for v in r:
        vals = np.append(vals, sum(v.values()))

    if vals.sum() != 0:
        vals = vals / vals.sum() * 100

    angles = np.linspace(start = 0, stop = 2 * np.pi, num = len(vals) + 1).tolist()
    vals = np.append(vals, vals[:1])
    angles[-1] = angles[0]

    ax.plot(angles, vals, color = 'blue', label = 'Total (%)')
    ax.fill(angles, vals, facecolor = 'blue', alpha = 0.1)

    ax.legend(fontsize = 'large')
    ax.set_title(title, size = 'xx-large', y = 1.08)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels = labels, fontsize = 'x-large')
    ax.set_ylim(0, 100)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle == 0:
            label.set_horizontalalignment('left')
        elif angle == np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('center')

    ax.set_rlabel_position(45)
    ax.set_facecolor('#FAFAFA')

    plt.tight_layout()  
        
def plot_radar_projetos(data, w = 15, h = 12):
    r = [fun.get_freq_based_on_year(data, ProjetoTipo.ENSINO),
           fun.get_freq_based_on_year(data, ProjetoTipo.PESQUISA),
           fun.get_freq_based_on_year(data, ProjetoTipo.EXTENSAO),
           fun.get_freq_based_on_year(data, ProjetoTipo.OUTRA)]
    
    title = 'Projeto'
    labels = ['Ensino', 'Pesquisa', 'Extensão', 'Outra']
    
    fig, ax = plt.subplots(figsize = (w, h), subplot_kw = dict(polar = True))
    
    vals = np.array([])

    for v in r:
        vals = np.append(vals, sum(v.values()))

    if vals.sum() != 0:
        vals = vals / vals.sum() * 100

    angles = np.linspace(start = 0, stop = 2 * np.pi, num = len(vals) + 1).tolist()
    vals = np.append(vals, vals[:1])
    angles[-1] = angles[0]

    ax.plot(angles, vals, color = 'blue', label = 'Total (%)')
    ax.fill(angles, vals, facecolor = 'blue', alpha = 0.1)

    ax.legend(fontsize = 'large')
    ax.set_title(title, size = 'xx-large', y = 1.08)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels = labels, fontsize = 'x-large')
    ax.set_ylim(0, 100)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle == 0:
            label.set_horizontalalignment('left')
        elif angle == np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('center')

    ax.set_rlabel_position(45)
    ax.set_facecolor('#FAFAFA')

    plt.tight_layout()
        
def plot_radar_producoes(data, w = 15, h = 12):
    r = [fun.get_freq_based_on_year(data, LocalTipo.CONFERENCIA),
           fun.get_freq_based_on_year(data, LocalTipo.PERIODICO),
           fun.get_freq_based_on_year(data, LocalTipo.RESUMO),
           fun.get_freq_based_on_year(data, LocalTipo.RESUMO_EXPANDIDO),
           fun.get_freq_based_on_year(data, LocalTipo.LIVRO),
           fun.get_freq_based_on_year(data, LocalTipo.CAPITULO_LIVRO),
           fun.get_freq_based_on_year(data, LocalTipo.LIVRO_ORGANIZADO)]
    
    title = 'Produção'
    labels = ['Conferência', 'Periódico', 'Resumo', 'Res. Exp.', 'Livro', 'Cap. Livro', 'Livro org.']
    
    fig, ax = plt.subplots(figsize = (w, h), subplot_kw = dict(polar = True))
    
    vals = np.array([])

    for v in r:
        vals = np.append(vals, sum(v.values()))

    if vals.sum() != 0:
        vals = vals / vals.sum() * 100

    angles = np.linspace(start = 0, stop = 2 * np.pi, num = len(vals) + 1).tolist()
    vals = np.append(vals, vals[:1])
    angles[-1] = angles[0]

    ax.plot(angles, vals, color = 'blue', label = 'Total (%)')
    ax.fill(angles, vals, facecolor = 'blue', alpha = 0.1)

    ax.legend(fontsize = 'large')
    ax.set_title(title, size = 'xx-large', y = 1.08)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels = labels, fontsize = 'x-large')
    ax.set_ylim(0, 100)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle == 0:
            label.set_horizontalalignment('left')
        elif angle == np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('center')

    ax.set_rlabel_position(45)
    ax.set_facecolor('#FAFAFA')

    plt.tight_layout()        

def plot_qualis(data, w = 19, h = 8):
    r = [fun.get_freq_based_on_year(data, LocalTipo.CONFERENCIA),
         fun.get_freq_based_on_year(data, LocalTipo.PERIODICO)]
    
    titles = [str(sum(r[0].values())) + ' papers de conferência',
              str(sum(r[1].values())) + ' papers de periódico']
    
    rr = [fun.get_freq_based_on_qualis(fun.get_data_range(data = data, _type = [LocalTipo.CONFERENCIA])), 
          fun.get_freq_based_on_qualis(fun.get_data_range(data = data, _type = [LocalTipo.PERIODICO]))]
    
    
    l, c = 1, 2
    fig, ax = plt.subplots(l, c, figsize = (w, h))
    
    for i in range(len(rr)):
        keys = sorted(rr[i])
        values = list(map(rr[i].get, keys))
        
        d = {'A1':0, 'A2':0, 'A3':0, 'A4':0,'B1':0, 'B2':0, 'B3':0, 'B4':0, 'C':0, 'NI': 0}
        for j, q in enumerate(keys):
            d[q] = values[j]
        
        rects = ax[i].bar(d.keys(), d.values(), color = '#2bbcd6', alpha = 1)

        ax[i].set_title(titles[i], fontsize = 'xx-large')
        ax[i].set_xlabel('Qualis', fontsize = 'xx-large')
        ax[i].set_ylabel('Frequência', fontsize = 'xx-large')
        ax[i].tick_params(axis = 'both', which = 'major', labelsize = 'xx-large')
        ax[i].grid(axis = 'x', color = 'lightblue', linestyle = '--')
        ax[i].set_ylim(0, max(values) + 1.5 if bool(values) else 10)
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['left'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].tick_params(left = False, labelleft = False)
        for rect in rects:
            h = rect.get_height()
            ax[i].text(rect.get_x() + rect.get_width() / 2., 1.01 * h, '%d' % int(h), ha = 'center', va = 'bottom', fontsize = 'x-large')
        
    plt.tight_layout()
    
def plot_wordcloud(data, path, n_words = 200, bg_color = 'purple', with_bg = False):
    # nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(nltk.corpus.stopwords.words('portuguese'))
    stopwords.extend(['applied', 'approach',
                      'based', 'baseado', 'Brazil', 'sobre',
                      'used', 'using', 'utilizando',          
                      'Pará', 'Proposal'
                      'study'
                      ])
    
    words = ' '.join(s.titulo for s in data)
    
    mask = np.array(Image.open(path + '/bc.png'))
    
    wordcloud = WordCloud(width = 1600, height = 800,
                          max_words = n_words,
                          random_state = 1, background_color = bg_color,
                          colormap = 'Set2', collocations = False,
                          stopwords = stopwords,
                          mask = mask if with_bg else None).generate(words)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation = 'bilinear')
    ax.set_axis_off()