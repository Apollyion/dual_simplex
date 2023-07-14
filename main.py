# Importando bibliotecas
import dualsimplex as ds
import numpy as np
import sys

def tem_none(lista):
    try:
        for ele in lista:
            if ele is None:
                return True
        return False
    except TypeError:
        return True

# nome_arquivo = "otimo.lp"
nome_arquivo = input("Digite o nome do arquivo: ")

caminhho_arquivo = "problemas/" + nome_arquivo + ".txt"
A, b, c, tipo_problema, sinal_restricao, sinais_variaveis, valor_limite = ds.ler_arquivo_entrada(caminhho_arquivo)

# Forma padrão
A, b, c, tipo_variavel = ds.transformar_padrao(A, b, c, tipo_problema, sinais_variaveis, sinal_restricao, valor_limite)

print("FORMA PADRÃO DO PROBLEMA:")

ds.imprimir_forma_padrao(A, b, c, tipo_variavel)

print('\n'+ '----------------------------------' + '\n')

# Primeira fase
A_fase1, c_fase1, tipo_variavel_fase1= ds.cria_primeira_fase(A, c, tipo_variavel)

print("PROBLEMA DE PRIMEIRA FASE DO SIMPLEX:")
ds.imprimir_primeira_fase(A_fase1, b, c_fase1, tipo_variavel_fase1)
B_inv, B, N, c_B, c_N, base_indices, org_B, org_N = ds.simplex_primeira_fase(A_fase1, b, c_fase1,tipo_variavel_fase1)
if tem_none(base_indices):
    exit()   
ds.imprime_resultado(A_fase1, b, c_fase1, tipo_variavel_fase1, base_indices)
print('\n'+ '----------------------------------' + '\n')
A_aux, b_aux, c_aux, tipo_variavel, base_indices = ds.criar_problema_auxiliar(A_fase1, b, c, tipo_variavel_fase1, base_indices)
print("PROBLEMA AUXILIAR DO SIMPLEX:")
ds.imprimir_auxiliar(A_aux, b_aux, c_aux, tipo_variavel, base_indices)
B_inv, B, N, c_B, c_N, base_indices, org_B, org_N  = ds.simplex(A_aux, b_aux, c_aux, base_indices)
if tem_none(base_indices):
    exit()   
print("RESULTADO PARA O PROBLEMA SIMPLEX")
ds.imprime_resultado(A_aux, b_aux, c_aux, tipo_variavel, base_indices)


print('\n'+ '----------------------------------' + '\n')
print("PROBLEMA DUAL:")
# todo: Colocar função que imprime o dual aqui
A_dual, b_dual, c_dual, tipo_variavel_dual = ds.cria_dual(A, b, c, tipo_variavel)
ds.imprimir_dual(A_dual, b_dual, c_dual, tipo_variavel_dual )

print('\n'+ '----------------------------------' + '\n')

# Resolvendo a partir do primal
print("RESULTADO PARA O PROBLEMA DUAL")
variaveis_dual = ds.calcular_valores_dual(A_aux, c_aux,base_indices)
print("Variáveis do dual: ", variaveis_dual)
print('\n'+ '----------------------------------' + '\n')

 #  Aplicando o simplex dual
while True:
    # Solicitando uma solução básica viável
    solucao = input("Digite uma solução básica viável: Partindo de 0, separando por um espaço: ")

    # Verificando se a solução é viável
    if ds.solucao_eh_viavel(solucao, A, c):  
        print("Solução viável encontrada.")
        solucao = [int(ele) for ele in solucao.split(" ")]
        base_indices_dual = ds.dual_simplex(A, c, b, solucao)
        ds.imprime_resultado_dual(base_indices_dual, A, b, c)
        break  # Sai do loop se a solução for viável
    else:
        print("Solução inviável. Tente novamente.")





