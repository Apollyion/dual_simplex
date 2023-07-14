# Definindo funções importantes para a implementação do algoritmo dual simplex
# Autor: Lucas José Lemos Braz

import numpy as np
#import pandas as pd
import math
import sys


# Função para ler o arquivo de entrada e retornar a matrix A e os vetores b e c, tipo de prob e número de variáveis e
# restrições Primeira linha do arquivo: número de variáveis N e número de restrições M Segunda linha do arquivo: 0 se
# for minimização e 1 se for maximização Terceira linha: N caracteres do vetor c M linhas seguintes: matriz A,
# onde o primeiro caractere é o tipo de restrição (0 para <=, 1 para >= e 2 para =), seguido de N caracteres Linha
# Seguinte: M caracteres do vetor b Linha Seguinte: N caracteres, onde 0 se for não negativas e 1 se for livres,
# 2 se for negativas.

def ler_arquivo_entrada(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Extrair o número de variáveis (N) e número de restrições (M) e tipo de problema (0 para minimização, 1 para maximização)
    tipo_problema, M, N = map(int, linhas[0].strip().split())

    # Extrair o vetor c
    c = list(map(float, linhas[1].strip().split()))

    # Extrair a matriz A, o vetor b e o sinal de restrição ( -1 para <=, 1 para >= e 0 para =)
    sinal_restricao = []
    A = []

    b = []
    for h in range(2,(2*M)+1,2):
        sinal_restricao.append(int(linhas[h].strip()))
        A.append(list(map(float, linhas[h+1].strip().split())))
        b.append(A[-1].pop(-1))
        #print(b)

    # Extrair as restrições de sianis das varivaies (-1 se menor ou igual e 1 se maior ou igual)
    # Caso a variável seja livre, a restrição terá apenas um valor coringa que adotaremos como sendo o 0.
    sinal_variaveis =[]
    valor_limite = []
    for h in range(2*M+2,len(linhas)):
        sinal_variaveis.append(list(map(int,linhas[h].strip().split())))
        if sinal_variaveis[-1][0] != 0:
            valor_limite.append(sinal_variaveis[-1].pop(-1))
        else:
            valor_limite.append(0)

    # Usar flatten
    sinal_variaveis = [item for sublist in sinal_variaveis for item in sublist]

    return A, b, c, tipo_problema, sinal_restricao, sinal_variaveis, valor_limite


# Função para converter o problema de maximização para minimização
def converter_max_min(c, tipo_problema):
    if tipo_problema == 1:
        c_convert = [-x for x in c]
        return c_convert
    else:
        return c

# TODO: Função para tratar as varivaies que tem valor limite != 0 e sinal != 0
# Eu defino uma nova restrisçao e trato o sinal.

# Função para lidar com variaveis != 0
def tratar_variaveis(A, b, sinal_restricao, sinais_variaveis, valor_limite):
    A_add = A.copy()
    b_add = b.copy()
    sinal_restricao_add = sinal_restricao.copy()
    for i in range(len(valor_limite)):
        if valor_limite[i] != 0:
            # Adiciona uma nova restrição no final da matriz A que tem N zeros e um 1 na posição da variável
            # que tem valor limite != 0
            A_add.append([0]*len(A[0]))
            A_add[-1][i] = 1
            # Adiciona o valor limite no vetor b
            b_add.append(valor_limite[i])
            # Adiciona o sinal de restrição
            sinal_restricao_add.append(sinais_variaveis[i])



    return A_add, b_add, sinal_restricao_add




# Função para remover inequaçao seguindo a regra de sinal_restricao
# 0 para <=, 1 para >= e 2 para =
def remover_inequacao(A, c, sinal_restricao, sinais_variaveis):
    A_convert = np.array(A.copy())
    tipo_variavel = []
    c_convert = c.copy()
    sinais_var_convt = sinais_variaveis.copy()
    tipo_variavel = (np.zeros_like(sinais_variaveis)).tolist()

    for i in range(len(sinal_restricao)):
        # É iqualdade então mantem.
        # Se -1 então é menor ou igual, então adiciona uma variável de folga "negativa" na linha e zeros nas outras.
        # Adiciona 0 no vetor c
        if sinal_restricao[i] == -1:
            g = np.zeros((len(sinal_restricao),1))
            g[i][0] = 1
            A_convert = np.concatenate((A_convert,g),axis=1)
            c_convert.append(0)
            sinais_var_convt.append(1)
            tipo_variavel.append('f')

        # Se 1 então é maior ou igual, então adiciona uma variável de folga na linha e zeros nas outras.
        # Adiciona 0 no vetor c
        # Eu posso criar um vetor coluna onde o [i] é igual a 1 e o resto é zero

        elif sinal_restricao[i] == 1:
            g = np.zeros((len(sinal_restricao),1))
            g[i][0] = -1
            A_convert = np.concatenate((A_convert,g),axis=1)
            c_convert.append(0)
            sinais_var_convt.append(1)
            tipo_variavel.append('f')

    return A_convert, c_convert, sinais_var_convt, tipo_variavel


# O problema está adiconado o item atual e o proximop mas agora eu não sei o que fazer, devo tratar todas ?
#

# Função para transformar as variáveis livres e negativas em não negativas
# -1 se menor ou igual e 1 se maior ou igual e 0 se livre
# Caso seja nao negativa, so mantem;
# Caso seja negativa, multiplica a coluna da variavel por -1, inclusive a coluna referente ao vetor c;
# Caso seja livre, troca a variavel por duas variaveis nao negativas, uma positiva e outra negativa,
# e no vetor C substitui a variavel por duas variaveis, uma positiva e outra negativa;
# Levando em consideração que A é uma Matriz e c é um vetor.
def transformar_variaveis_nao_negativas(A, b, c, sinais_variaveis, tipo_variavel):
    A = A.copy()
    c = c.copy()
    b = b.copy()
    tipo_variavel = tipo_variavel.copy()
    sinais_variaveis = np.array(sinais_variaveis)

    num_variaveis = A.shape[1]
    num_restricoes = A.shape[0]

    if num_variaveis != len(sinais_variaveis):
        print("ERRO: O PROBLEMA ESTÁ FORA DO PADRÃO.")
        sys.exit()

    # Transformar variáveis negativas
    for i in range(num_variaveis):
        if sinais_variaveis[i] == -1:  # Variável negativa
            A[:, i] *= -1
            c[i] *= -1
            #tipo_variavel[i] = '0'

    # Transformar variáveis livres
    A_transformed = []
    b_transformed = []
    c_transformed = []
    tipo_variavel_transformed = []

    for i in range(num_variaveis):
        if sinais_variaveis[i] == 0:  # Variável livre
            # Introduzir duas variáveis não negativas
            A_transformed.append(A[:, i])
            A_transformed.append(-A[:, i])
            b_transformed.append(b)
            b_transformed.append([ele * (-1) for ele in b])
            c_transformed.append(c[i]) # TODO: POSSIVEL BUG
            c_transformed.append(-c[i])
            tipo_variavel_transformed.append(0)
            tipo_variavel_transformed.append(0)
        else:  # Variável não negativa
            A_transformed.append(A[:, i])
            b_transformed.append(b)
            c_transformed.append(c[i])
            tipo_variavel_transformed.append(tipo_variavel[i])

    A_transformed = np.array(A_transformed).T
    b_transformed = np.array(b_transformed[0])
    c_transformed = np.array(c_transformed)

    return A_transformed.tolist(), b_transformed.tolist(), c_transformed.tolist(), tipo_variavel_transformed


# Função para sinal negativo do vetor b.
# Caso seja negativo, multiplica a o elemento do vetor por -1, e multiplica a linha da matriz por A -1.
def remover_negativos_b(A, b):
    for i in range(len(b)):
        if b[i] < 0:
            b[i] = b[i] * (-1)
            A[i] = [ele * (-1) for ele in A[i]]
    return A, b


# Finalmente transoforma na forma padrão
def transformar_padrao(A, b, c, tipo_problema, sinais_variaveis, sinal_restricao, valor_limite):
    # Converter problema de maximização para minimização
    c = converter_max_min(c, tipo_problema)

    # Tratar a restrição de sinal
    A, b, sinal_restricao = tratar_variaveis(A, b, sinal_restricao, sinais_variaveis, valor_limite)

    # Remover inequações
    A, c, sinais_variaveis, tipo_variavel = remover_inequacao(A, c, sinal_restricao, sinais_variaveis)

    # Transformar variáveis livres e negativas em não negativas
    A, b, c, tipo_variavel = transformar_variaveis_nao_negativas(A, b, c, sinais_variaveis, tipo_variavel)

    # Remover negativos do vetor b
    A, b = remover_negativos_b(A, b)

    return A, b, c, tipo_variavel


def imprimir_forma_padrao(A, b, c, tipo_variavel):
    num_variaveis = len(c)
    num_restricoes = len(b)
    A = np.array(A.copy())
    A = np.where(np.logical_or(A == 0, A == -0), 0, A)
    A = list(A)

    count_f = 1
    # Imprimir a função objetivo
    objetivo = ""
    if c[0] >= 0 and tipo_variavel[0] == 0:
        objetivo += " {}x{}".format(c[0], 1)
    elif c[0] < 0 and tipo_variavel[0] == 0:
        objetivo += " -{}x{}".format(-c[0], 1)
    for i in range(1, num_variaveis):
        if c[i] >= 0 and tipo_variavel[i] == 0:
            objetivo += " +{}x{}".format(c[i], i + 1)
        elif c[i] < 0 and tipo_variavel[i] == 0:
            objetivo += " -{}x{}".format(-c[i], i + 1)
        elif c[i] >= 0 and tipo_variavel[i] == 'f':
            objetivo += " +{}f{}".format(c[i], count_f)
            count_f += 1
        elif c[i] < 0 and tipo_variavel[i] == 'f':
            objetivo += " -{}f{}".format(-c[i], count_f)
            count_f += 1
    print("Min ", objetivo)

    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] >= 0 and tipo_variavel[0] == 0:
            restricao += " {}x{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 0:
            restricao += " -{}x{}".format(-A[i][0], 1)
        elif A[i][0] >= 0 and tipo_variavel[0] == 'f':
            restricao += " {}f{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 'f':
            restricao += " -{}f{}".format(-A[i][0], 1)

        f = 1
        for j in range(1, num_variaveis):
            if A[i][j] >= 0 and tipo_variavel[j] == 0:
                restricao += " +{}x{}".format(A[i][j], j + 1)
            elif A[i][j] < 0 and tipo_variavel[j] == 0:
                restricao += " -{}x{}".format(-A[i][j], j + 1)
            elif A[i][j] >= 0 and tipo_variavel[j] == 'f':
                restricao += " +{}f{}".format(A[i][j], f)
                f += 1
            elif A[i][j] < 0 and tipo_variavel[j] == 'f':
                restricao += " -{}f{}".format(-A[i][j], f)
                f += 1
        restricao += " = {}".format(b[i])
        print('\t' + restricao)

    # Imprimir as condições de não negatividade
    print("\t\t", end="")
    f_f = 1
    for i in range(num_variaveis):
        if tipo_variavel[i] == 0:
            print("x{},".format(i + 1), end=" ")
        elif tipo_variavel[i] == 'f':
            print("f{},".format(f_f), end=" ")
            f_f += 1
    print(">= 0", end=" ")




# Tenho a forma padrão, agora preciso criar a primeira fase
# A primeira fase é criada adicionando uma variável de 'y' para cada restrição
# A função objetivo é minimizar a soma de todas as variáveis 'y' que tem peso 1

# Eu tenho que adiconar tipo_variavel = 'y' para cada variável 'y' adicionada
# Quando for imprimir o primeira fase, eu tenho que imprimir as variáveis 'y' também
# Depois de resolver a primeira fase, eu tenho que se a solução ótima é 0, se for,
# eu posso remover as variáveis 'y' e resolver o problema original

# É importante manter em mente o vetor que as variaveis da primeira fase, para ver se tem y na base.


# FUnção para criar a primeira fase
def cria_primeira_fase(A, c, tipo_variavel):
    A = np.array(A)
    c = np.array(c)

    num_variaveis = len(c)
    num_restricoes = len(A)

    # Criando a matriz A da primeira fase
    # Adiciona uma matrix identidade de tamanho num_restricoes
    A_primeira_fase = np.concatenate((A, np.identity(num_restricoes)), axis=1)

    # Criando o vetor c da primeira fase
    # Um vetor de zeros de tamanho num_varivaeis, e um vetor de 1 de tamanho num_restricoes
    c_primeira_fase = np.concatenate((np.zeros(num_variaveis), np.ones(num_restricoes)), axis=0)

    # Manter em mente o tipo de variável
    tipo_variavel_primeira_fase = tipo_variavel + ['y'] * num_restricoes

    return A_primeira_fase.tolist(), c_primeira_fase.tolist(), tipo_variavel_primeira_fase


# Função para imprimir a primeira fase
def imprimir_primeira_fase(A, b, c, tipo_variavel):
    num_variaveis = len(c)
    num_restricoes = len(b)
    num_variaveis_y = num_variaveis - num_restricoes  # numero de variáveis y

    A = np.array(A.copy())
    A = np.where(np.logical_or(A == 0, A == -0), 0, A)
    A = list(A)



    objetivo = "\t" * (num_variaveis_y-num_variaveis)
    for i in range(num_variaveis):
        if tipo_variavel[i] == 'y':
            objetivo += " +{}y{}".format(c[i], i + 1 - num_variaveis_y)
        else:
            objetivo += " "
    print("Min ", objetivo)

    # Imprimir as restrições
    # Mantendo em mente que se tipo_variavel for 0 é x, se for 'f' é folga e se for 'y' é y
    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] >= 0 and tipo_variavel[0] == 0:
            restricao += " {}x{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 0:
            restricao += " -{}x{}".format(-A[i][0], 1)
        elif A[i][0] >= 0 and tipo_variavel[0] == 'f':
            restricao += " {}f{}1".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 'f':
            restricao += " -{}f{}1".format(-A[i][0], 1)

        f = 1
        y = 1
        for j in range(1, num_variaveis):
            if A[i][j] >= 0 and tipo_variavel[j] == 0:
                restricao += " +{}x{}".format(A[i][j], j + 1)
            elif A[i][j] < 0 and tipo_variavel[j] == 0:
                restricao += " -{}x{}".format(-A[i][j], j + 1)
            elif A[i][j] >= 0 and tipo_variavel[j] == 'f':
                restricao += " +{}f{}".format(A[i][j], f)
                f += 1
            elif A[i][j] < 0 and tipo_variavel[j] == 'f':
                restricao += " -{}f{}".format(-A[i][j], f)
                f += 1
            elif A[i][j] >= 0 and tipo_variavel[j] == 'y':
                restricao += " +{}y{}".format(A[i][j], y)
                y += 1
            elif A[i][j] < 0 and tipo_variavel[j] == 'y':
                restricao += " -{}y{}".format(-A[i][j], y)
                y += 1
        restricao += " = {}".format(b[i])
        print('\t' + restricao)

    # Imprimir as condições de não negatividade
    print("\t\t", end="")
    f_f = 1
    for i in range(num_variaveis):
        if tipo_variavel[i] == 0:
            print("x{},".format(i + 1), end=" ")
        elif tipo_variavel[i] == 'f':
            print("f{},".format(f_f), end=" ")
            f_f += 1
    for i in range(num_restricoes):
        print(" " + "y{},".format(i + 1), end="")
    print(" >= 0")

# XTODO: Corrigir funções de impressão
# XTODO: Função para ler o arquivo txt
# xTODO: Imprimir o Auxiliar
# xTODO: Mostrar as soluções basicas por iteração (Para o Auxiliar e para o Primal)
# TODO: Função para criar Dual;
# TODO: Imprimir o Dual;
# TODO: Resolver o Dual (Usando o Primal);
# XTODO: Imprimir solução otima Primal;
# TODO: Imprimir solução otima Dual;
# TODOX: Readme explicando o funcionamento básico e compilação do código;
# XTODO :PEQUENO RELATÓRIO contendo um breve resumo do simplex.



# FINALMENTE IMPLEMTANDO O SIMPLEX
# Função para resolver o simplex primeira fase
def simplex_primeira_fase(A, b, c, tipo_variavel):
    itercao = 1
    A = np.array(A.copy())
    b = np.array(b.copy())
    c = np.array(c.copy())
    m, n = A.shape


    # Determinar a base inicial
    base_indices = [i for i, var in enumerate(tipo_variavel) if var == 'y']
    B = A[:, base_indices]
    N = A[:, [i for i in range(n) if i not in base_indices]]

    # Criando a matriz c_B e c_N
    c_B = c[base_indices]
    c_N = c[[i for i in range(n) if i not in base_indices]]
    try:
        B_inv = np.linalg.inv(B)
    except:
        print("O problema não tem solução viável")
        return

    # Varivael para saber qual a organização original das variáveis para poder aplicar a regra de Bland
    organizacao_original = [i for i in range(n)]
    org_N = [i for i in range(len(N[0]))]
    org_B = [i for i in range(len(N[0]), len(N[0]) + len(B[0]))]

    # Roda o simplex até encontrar o otimo ou parar por inviabilidade
    print("\n")
    print("Iteração {}".format(itercao) + " | Colunas Basicas: {}".format([i+1 for i in base_indices]) + " | Colunas Não Basicas: {}".format([i+1 for i in range(n) if i not in base_indices]))
    while True:
        # Calcula a
        # Realiza o teste de otimalidade
        otimo = c_N - c_B @ B_inv @ N
        # Se o vetor for maior que zero então encontramos o otimo
        if all(otimo >= 0):
            if np.dot(c_B, np.linalg.inv(B).dot(b)) == 0:
                return B_inv, B, N, c_B, c_N, base_indices, org_B, org_N
            else:
                print("Problema inviável")
                return None, None, None, None, None, None, None, None

        # Seleciona o indice j, pegando um valor negativo do vetor otimo que tenha o menor indice referente a org_N

        indices_negativos = list(np.where(otimo < 0)[0])
        org_N_aux = [org_N[i] for i in indices_negativos]
        j = indices_negativos[np.argmin(org_N_aux)]# Retorna a posição do menor valor de org_N_aux
        #j = org_N[indice_min_org_N]


        # Calcula a direção simplex
        d_b = -B_inv @ N[:, j]
        # Realiza o teste de inviabilidade
        if all(d_b >= 0):
            print("Problema Ilimitado")
            return None, None, None, None, None, None, None, None

        #Calcula x_b
        x_b = B_inv @ b

        # Seleciona o indice k, pegando o menor valor de x_b/d_b para os valores negativos de d_b, se tiver empate pega o menor indice referente a org_B
        negative_indices = np.where(d_b < 0)[0]
        b_div_d_b = -x_b[negative_indices] / d_b[negative_indices]
        min_ratio_indices = np.where(b_div_d_b == np.min(b_div_d_b))[0]

        if len(min_ratio_indices) == 1:
            k = int(negative_indices[min_ratio_indices])
        else:
            org_B_aux = [org_B[i] for i in min_ratio_indices]
            k = int(negative_indices[np.argmin(org_B_aux)])
        #k = org_B[indice_min_org_B]
        # Troca as variáveis de base, K do conjunto B e J do conjunto N, e atualiza as c_B, c_N, B_inv, B e N

        base_k_aux = base_indices[k]
        base_indices[k] = org_N[j]
        org_N[j] = base_k_aux
        org_B = base_indices.copy()

        c_B_aux = c_B[k]
        c_B[k] = c_N[j]
        c_N[j] = c_B_aux

        B_aux = B[:,k].copy()
        B[:, k] = N[:,j].copy()
        N[:, j] = B_aux

        itercao += 1
        print("Iteração {}".format(itercao) + " | Colunas Basicas: {}".format([i+1 for i in base_indices]) + " 1| Colunas Não Basicas: {}".format([i+1 for i in range(n) if i not in base_indices]))


        B_inv = np.linalg.inv(B)



def criar_problema_auxiliar(A, b, c, tipo_variavel, base_indices):
    A = np.array(A.copy())
    b = np.array(b.copy())
    c_aux = np.array(c.copy())
    tipo_variavel = tipo_variavel.copy()
    base_indices = base_indices.copy()
    m, n = A.shape

    # Eu crio uma nova linha na matriz A, onde tiver y, e adiciono mais um.
    # Adicono uma nova restrição =0 em b
    # Adiciono novo custo em c = 0
    # Adiciona Z em tipo de variavel
    # Adiciona o indice da nova variavel no base_indices

    # Adicionando a nova linha e coluna em A
    nova_linha_zeros = np.zeros((1, A.shape[1]))
    # Inserir a nova linha de zeros abaixo da matriz original
    A_aux = np.vstack((A, nova_linha_zeros))
    # Inserir a nova coluna de zeros a direita da matriz original
    nova_coluna_zeros = np.zeros((A_aux.shape[0], 1))
    A_aux = np.hstack((A_aux, nova_coluna_zeros))

    # Adicionando Z em tipo_variavel
    tipo_variavel.append('z')

    # Na ultima coluna de A_aux, eu troco por 1 se tipo_variavel for 'y' ou 'z'
    for i in range(len(tipo_variavel)):
        if tipo_variavel[i] == 'y' or tipo_variavel[i] == 'z':
            A_aux[-1, i] = 1

            # Adicionando o novo custo em c
            c_aux = np.append(c_aux, 0)

    # Adicionando a nova restrição em b
    b_aux = np.append(b, 0)

    # Adicionando o indice da nova variavel no base_indices
    base_indices.append(A_aux.shape[1] - 1)

    return A_aux, b_aux, c_aux, tipo_variavel, base_indices


def imprime_resultado(A, b, c, tipo_variavel, base_indices):
    A = np.array(A.copy())
    m, n = A.shape
    x_B = np.zeros(n)
    x_B[base_indices] = np.linalg.solve(A[:, base_indices], b)
    c = np.array(c.copy())  # Convertendo c em um array NumPy
    # Verificar se base_indices contém apenas valores válidos
    if any(i >= n for i in base_indices):
        raise ValueError("Índices inválidos em base_indices.")

    custo = np.dot(c[base_indices], x_B[base_indices])

    print("\n")
    print("Custo encontrado: {}".format(custo))
    print("Vetor x: [", end=" ")
    for i in range(n):
        if i in base_indices:
            print("{:.2f},".format(x_B[i]), end="")
            #print("{:.2f},".format(x_B[i]), end="")
        else:
            print("0.00,", end="")
    print("]")

def imprime_resultado_dual(base_indices, A, b, c):
    A = np.array(A.copy())
    b = np.array(b.copy())
    c = np.array(c.copy())
    
    m, n = A.shape

    # Construir matriz básica e calcular valores de u
    B = A[:, base_indices]
    B_inv = np.linalg.inv(B)
    u = np.dot(c[base_indices], B_inv)

    # Calcular custo dual
    dual_cost = np.dot(u, b)

    # Imprimir resultados
    print("Custo Dual: ", dual_cost)
    print("Valores de u: ", u)


def imprimir_auxiliar(A, b, c, tipo_variavel, base_indices):
    num_variaveis = len(c)
    num_restricoes = len(b)
    A = np.array(A.copy())
    A = np.where(np.logical_or(A == 0, A == -0), 0, A)
    A = list(A)

    count_f = 1
    count_y = 1
    # Imprimir a função objetivo
    objetivo = ""
    if c[0] >= 0 and tipo_variavel[0] == 0:
        objetivo += " {}x{}".format(c[0], 1)
    elif c[0] < 0 and tipo_variavel[0] == 0:
        objetivo += " -{}x{}".format(-c[0], 1)
    for i in range(1, num_variaveis):
        if c[i] >= 0 and tipo_variavel[i] == 0:
            objetivo += " +{}x{}".format(c[i], i + 1)
        elif c[i] < 0 and tipo_variavel[i] == 0:
            objetivo += " -{}x{}".format(-c[i], i + 1)
        elif c[i] >= 0 and tipo_variavel[i] == 'f':
            objetivo += " +{}f{}".format(c[i], count_f)
            count_f += 1
        elif c[i] < 0 and tipo_variavel[i] == 'f':
            objetivo += " -{}f{}".format(-c[i], count_f)
            count_f += 1
        elif c[i] >= 0 and tipo_variavel[i] == 'y':
            objetivo += " +{}y{}".format(c[i], count_y)
            count_y += 1
        elif c[i] < 0 and tipo_variavel[i] == 'y':
            objetivo += " -{}y{}".format(-c[i], count_y)
            count_y += 1
        else:
            objetivo += " +{}{}".format(c[i], tipo_variavel[i])
    print("Min ", objetivo)

    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] >= 0 and tipo_variavel[0] == 0:
            restricao += " {}x{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 0:
            restricao += " -{}x{}".format(-A[i][0], 1)
        elif A[i][0] >= 0 and tipo_variavel[0] == 'f':
            restricao += " {}f{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 'f':
            restricao += " -{}f{}".format(-A[i][0], 1)
        else:
            restricao += " +{}z".format(A[i][0])

        f = 1
        y = 1
        for j in range(1, num_variaveis):
            if A[i][j] >= 0 and tipo_variavel[j] == 0:
                restricao += " +{}x{}".format(A[i][j], j + 1)
            elif A[i][j] < 0 and tipo_variavel[j] == 0:
                restricao += " -{}x{}".format(-A[i][j], j + 1)
            elif A[i][j] >= 0 and tipo_variavel[j] == 'f':
                restricao += " +{}f{}".format(A[i][j], f)
                f += 1
            elif A[i][j] < 0 and tipo_variavel[j] == 'f':
                restricao += " -{}f{}".format(-A[i][j], f)
                f += 1
            elif A[i][j] >= 0 and tipo_variavel[j] == 'y':
                restricao += " +{}y{}".format(A[i][j], y)
                y += 1
            elif A[i][j] < 0 and tipo_variavel[j] == 'y':
                restricao += " -{}y{}".format(-A[i][j], y)
                y += 1
            else:
                restricao += " +{}z".format(A[i][j])
        restricao += " = {}".format(b[i])
        print('\t' + restricao)

    # Imprimir as condições de não negatividade
    f_f = 1
    y_y = 1
    print("\t\t\t", end="")
    for i in range(num_variaveis):
        if tipo_variavel[i] == 0:
            print("x{},".format(i + 1), end=" ")
        elif tipo_variavel[i] == 'f':
            print("f{},".format(f_f), end=" ")
            f_f += 1
        elif tipo_variavel[i] == 'y':
            print("y{},".format(y_y), end=" ")
            y_y += 1
        else:
            print("z,", end=" ")

    # Imprimindo variaveis de folga
    print(" >= 0")




def simplex(A, b, c, base_indices):
    A = np.array(A.copy())
    b = np.array(b.copy())
    c = np.array(c.copy())
    m, n = A.shape
    base_indices = base_indices.copy()

    B = A[:, base_indices].copy()
    N = A[:, [i for i in range(n) if i not in base_indices]].copy()

    # Criando a matriz c_B e c_N
    c_B = c[base_indices].copy()
    c_N = c[[i for i in range(n) if i not in base_indices]].copy()
    try:
        B_inv = np.linalg.inv(B)
    except:
        print("O problema não tem solução viável")
        return

    # Varivael para saber qual a organização original das variáveis para poder aplicar a regra de Bland
    org_B = base_indices.copy()
    # org_N vai receber o tamanho do vetor de C exceto os indices da base
    org_N = [i for i in range(len(c)) if i not in base_indices]
    itercao = 1
    print("\n")
    print("Iteração {}".format(itercao) + " | Colunas Basicas: {}".format(
        [i + 1 for i in base_indices]) + " | Colunas Não Basicas: {}".format(
        [i + 1 for i in range(n) if i not in base_indices]))
    while True:
        # Calcula a
        # Realiza o teste de otimalidade
        otimo = c_N - c_B @ B_inv @ N
        # Se o vetor for maior que zero então encontramos o otimo
        if all(otimo >= 0):
            return B_inv, B, N, c_B, c_N, base_indices, org_B, org_N
        # Seleciona o indice j, pegando um valor negativo do vetor otimo que tenha o menor indice referente a org_N

        indices_negativos = list(np.where(otimo < 0)[0])
        org_N_aux = [org_N[i] for i in indices_negativos]
        j = indices_negativos[np.argmin(org_N_aux)]# Retorna a posição do menor valor de org_N_aux
        #j = org_N[indice_min_org_N]


        # Calcula a direção simplex
        d_b = -B_inv @ N[:, j]
        # Realiza o teste de inviabilidade
        if all(d_b >= 0):
            print("Problema Ilimitado")
            return None, None, None, None, None, None, None, None

        #Calcula x_b
        x_b = B_inv @ b

        # Seleciona o indice k, pegando o menor valor de x_b/d_b para os valores negativos de d_b, se tiver empate pega o menor indice referente a org_B
        negative_indices = np.where(d_b < 0)[0]
        b_div_d_b = -x_b[negative_indices] / d_b[negative_indices]
        min_ratio_indices = np.where(b_div_d_b == np.min(b_div_d_b))[0]

        if len(min_ratio_indices) == 1:
            k = int(negative_indices[min_ratio_indices])
        else:
            org_B_aux = [org_B[i] for i in min_ratio_indices]
            k = int(negative_indices[np.argmin(org_B_aux)])
        #k = org_B[indice_min_org_B]
        # Troca as variáveis de base, K do conjunto B e J do conjunto N, e atualiza as c_B, c_N, B_inv, B e N

        base_k_aux = base_indices[k]
        base_indices[k] = org_N[j]
        org_N[j] = base_k_aux
        org_B = base_indices.copy()

        c_B_aux = c_B[k]
        c_B[k] = c_N[j]
        c_N[j] = c_B_aux

        B_aux = B[:,k].copy()
        B[:, k] = N[:,j].copy()
        N[:, j] = B_aux
        itercao += 1
        print("Iteração {}".format(itercao) + " | Colunas Basicas: {}".format(
            [i + 1 for i in base_indices]) + " | Colunas Não Basicas: {}".format(
            [i + 1 for i in range(n) if i not in base_indices]))
        B_inv = np.linalg.inv(B)


def calcular_valores_dual(A, c, base_indices):
    A = np.array(A.copy())
    c = np.array(c.copy())
    base_indices = base_indices.copy()
    m, n = A.shape


    B = A[:, base_indices]  # Matriz básica
    c_B = c[base_indices]  # Coeficientes da função objetivo das variáveis básicas

    inv_B = np.linalg.inv(B)  # Inversa da matriz básica

    valores_dual = c_B.T @ inv_B  # Valores das variáveis do problema dual

    return valores_dual

def dual_simplex(A, c, b, base_indices):
    A = np.array(A.copy())
    b = np.array(b.copy())
    c = np.array(c.copy())
    m, n = A.shape

    itercao = 1
    while True:
        # Passo 1: Calcular os custos relativos
        B = A[:, base_indices]
        c_B = c[base_indices]
        B_inv = np.linalg.inv(B)
        y = np.dot(c_B, B_inv)

        # Passo 2: Verificar a otimalidade
        if np.all(B_inv @ b >= 0):
            return base_indices

        # Passo 3: Encontrar a variável entrante
        entra = np.argmin(y)

        # Passo 4: Calcular a direção simplex
        k = np.eye(m)[entra]
        d = -np.dot(k, B_inv)

        # Passo 5: Verificar a ilimitabilidade
        if np.all(d >= 0):
            return "Problema ilimitado"

        # Passo 6: Encontrar a variável saindo
        ratios = b / d
        sai = np.argmin(ratios[ratios > 0])

        # Passo 7: Atualizar a base
        base_indices[sai] = entra
        print("Iteração {}".format(itercao) + " | Colunas Basicas: {}".format(
            [i + 1 for i in base_indices]) + " | Colunas Não Basicas: {}".format(
            [i + 1 for i in range(n) if i not in base_indices]))

# FUnção para criar o dual
def cria_dual(A, b, c, tipo_variavel):
    A_aux = np.array(A)
    b = np.array(b)
    c = np.array(c)

    # Transposta da matriz A do Pl original na forma padrão
    linhas = np.shape(A_aux)[0] # linhas da matriz original
    colunas = np.shape(A_aux)[1] # colunas da matriz original
    transposta = np.empty((colunas, linhas)) 
     
    # e agora vamos preencher a matriz transposta
    for i in range(np.shape(A_aux)[0]):
        for j in range(np.shape(A_aux)[1]):
            transposta[j][i] = A_aux[i][j]

    # Dessa forma, temos a matriz A do dual
    A = np.array(transposta)

    num_variaveis = len(b)
    num_restricoes = len(c)
 
    # Manter em mente o tipo de variável
    tipo_variavel_dual = ['u'] * num_variaveis

    return A, b, c, tipo_variavel_dual

# Função para imprimir o dual
def imprimir_dual(A, b, c, tipo_variavel):
    num_variaveis = len(b)
    num_restricoes = len(c)
    A = np.array(A.copy())
    A = np.where(np.logical_or(A == 0, A == -0), 0, A)
    A = list(A)

    # Imprimir a função objetivo
    objetivo = ""
    if b[0] >= 0 and tipo_variavel[0] == 'u':
        objetivo += " {}u{}".format(b[0], 1)
    elif b[0] < 0 and tipo_variavel[0] == 'u':
        objetivo += " -{}u{}".format(-b[0], 1)
    for i in range(1, num_variaveis):
        if b[i] >= 0 and tipo_variavel[i] == 'u':
            objetivo += " +{}u{}".format(b[i], i + 1)
        elif b[i] < 0 and tipo_variavel[i] == 'u':
            objetivo += " -{}u{}".format(-b[i], i + 1)
        
    print("Max ", objetivo)
    

    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] >= 0 and tipo_variavel[0] == 'u':
            restricao += " {}u{}".format(A[i][0], 1)
        elif A[i][0] < 0 and tipo_variavel[0] == 'u':
            restricao += " -{}u{}".format(-A[i][0], 1)
        
        for j in range(1, num_variaveis):
            if A[i][j] >= 0 and tipo_variavel[j] == 'u':
                restricao += " +{}u{}".format(A[i][j], j + 1)
            elif A[i][j] < 0 and tipo_variavel[j] == 'u':
                restricao += " -{}u{}".format(-A[i][j], j + 1)
           
        restricao += " <= {}".format(c[i])
        print('\t' + restricao)

    # Imprimir as condições de livre
    print("\t\t", end="")
    
    for i in range(num_variaveis):
        if tipo_variavel[i] == 'u':
            print("u{},".format(i + 1), end=" ")
        
    print(" livre", end=" ")

    
def solucao_eh_viavel(base_dual, A, c):
    base_dual = [int(ele) for ele in base_dual.split(" ")]
    base_dual = np.array(base_dual.copy())

    A = np.array(A.copy())
    c = np.array(c.copy())

    # Verifica se é invertivel
    try :
        inv_B_dual = np.linalg.inv(A[:, base_dual])
    except:
        return False
    #Calcula valores de u
    u_dual = c[base_dual] @ inv_B_dual

    #Verifica condição U_dual . A <= c
    if all(u_dual @ A <= c):
        return True
    else:
        return False
