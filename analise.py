import unicodedata
import string
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import unidecode
import operator


artigos = [ "a", "o", "as", "os", "um", "uns", "uma", "umas" ]

preposicoes = ['a', 'ante', 'ate', 'apos','com', 'contra', 'de', 'desde',
               'em', 'entre', 'para', 'per', 'por', 'perante', 'sem', 'sob', 
               'sobre', 'tras']

combinacoes = [ "ao", "aos", "a", "as", "do", "dos", "da", "das", "dum", "duns", "duma", "dumas", "no", "nos", "na", "nas", "num", "nuns", "numa", "numas", "pelo", "pelos", "pela", "pelas" ]
             
pronomes_pessoais = [ "eu", "tu", "ele", "ela", "nos", "vos", "eles", "elas"]

pronomes_pessoais_atonos = ["mim", "te", "se", "lhe", "o", "a", "nos", "vos", "lhes", "os", "as", "se"]

pronomes_pessoais_tonicos = [ "mim", "ti", "ele", "ela", "si", "nos", "vos", "eles", "elas", "si"]

pronomes_possessivos = [ "meu", "minha", "meus", "minhas", "teu", "tua", "teus", "tuas", "seu", "sua", "seus", "suas", "nosso", "nossa", "nossos", "nossas", "vosso", "vossa", "vossos", "vossas", "seu", "sua", "seus", "suas"]

pronomes_demonstrativos = [ "este", "esta", "isto", "esse", "essa", "isso", "aquele", "aquela", "aquilo"]

pronomes_relativos = [ "qual", "cujo", "cuja", "cujos" "cujas", "que", "quanto" "quanta", "quantos", "quantas", "onde"]

pronomes_interrogativos = [ "quem", "que", "qual", "quais",  "quanto", "quantos", "quantas"]

pronomes_indefinidos = ["alguém", "ninguém", "tudo", "nada", "algo", "outrem", "nenhum", "nenhuns", "nenhuma", "nenhumas", "mais", "menos", "muito", "muitos", "muita", "muitas", "pouco", "poucos", "pouca", "poucas", "todo", "todos", "toda", "todas", "algum", "alguns", "alguma", "algumas", "tanto", "tantos", "tanta", "tantas", "quanto", "quantos", "quanta", "quantas", "vario", "varios", "varia", "varias", "diverso", "diversos", "diversa", "diversas", "outro", "outros", "outra", "outras", "um", "uns", "uma", "umas", "certo", "certos", "certa", "certas", "qualquer", "quaisquer", "cada"]

pronomes = pronomes_pessoais + pronomes_pessoais_atonos + pronomes_pessoais_tonicos + \
           pronomes_possessivos + pronomes_demonstrativos + pronomes_relativos + \
           pronomes_interrogativos + pronomes_indefinidos

nomes = ['bolsonaro', 'fernando', 'manuela', 'haddad','davila', 'luiz', 'inacio', 'lula', 'silva']

caracteres_especiais = ['r$']

def get_words_from_schwartz_list():
    f = open('stopwords.txt', 'r')
    stopwords = f.read().split('\n')
    return stopwords

STOPWORDS = preposicoes + artigos + nomes + combinacoes + pronomes + stopwords.words('portuguese') + get_words_from_schwartz_list()

CANDIDATES = ['amoedo', 'alckmin', 'bolsonaro', 'ciro', 'haddad']

def remove_accents(s):
    return(''.join(c for c in unicodedata.normalize('NFKD', s) if c in string.printable[10:62] or c == ' ' or c == '\n')).lower()

def get_repetition_mean(response):
    repetitions = [i['value'] for i in response]
    #print(repetitions)
    distinct_n_repetitions = set(repetitions)
    sum_ = sum([repetitions.count(i) for i in distinct_n_repetitions])
    n_repetitions = len([repetitions.count(i) for i in distinct_n_repetitions])
    return (sum_/n_repetitions), min(distinct_n_repetitions), max(distinct_n_repetitions)

palavras = ["brasil", "economia", "criar", "combater", "desenvolvimento", "pais", "queremos", "brasileiros", "educacao", "governo", "paises", "politica", "nacional", "criacao", "empresas"]

def read_file(candidate):
    f = open(candidate + '.txt','r')
    print(candidate)
    text = f.read()
    bla = [unidecode.unidecode(i).lower() for i in text.split() if unidecode.unidecode(i.lower()) not in STOPWORDS and len(i) > 1]
    print(bla.count('R$'))
    text = ' '.join(bla)
    text = remove_accents(text)
    j = 0
    for i in text.split():
        if i == 'r':
            print(text.split()[j-1], text.split()[j+1])
        j += 1
    #print(sorted(set(text.split())))
    tl = text.split()
    response = [{'text':i, 'value':bla.count(i)} for i in set(tl) if bla.count(i) > 2]
    h = []
    for k in palavras:
        for i in response:
            if i['text'] == k:
                h.append(i['value'])
                break
        else:
            h.append(0)
    print(h)
    #print(sorted(response, key=lambda k: k['value'], reverse=True)[:10])
    repetitions_mean, min_, max_ = get_repetition_mean(response)
    response = [dict(r, l=((r['value']- min_)/(max_-min_)*36 + 14)) for r in response]
    #response = [r for r in response if r['value'] > int(repetitions_mean)]
    #print(f.name)
    a = open(f.name + str(1) ,'w')
    a.write(str(response))
    a.close()
    text = ' '.join([i for i in text.split() if i not in STOPWORDS])
    return response 

def get_candidates_bag_of_words():
    responses = []
    for candidate in CANDIDATES:
        responses.append(read_file(candidate))
    return responses
