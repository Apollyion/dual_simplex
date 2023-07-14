# Readme - Solução do Algoritmo Simplex

Este readme fornece informações sobre como utilizar o código para solucionar o algoritmo simplex. Siga as instruções abaixo para garantir uma execução correta.

# Nomes e matrículas:
Evecleison Albuquerque do Nascimento - 494131
Lucas José Lemos Braz - 471993

## Requisitos

- Python 3.9 ou superior
- Biblioteca NumPy

## Instalação do NumPy

Para instalar a biblioteca NumPy, você pode utilizar o gerenciador de pacotes `pip` que já vem instalado com o Python. Execute o seguinte comando no terminal:

```bash
pip install numpy
```

## Preparando o problema

Antes de executar o código, certifique-se de ter o problema que deseja resolver no formato de um arquivo de texto (.txt). O arquivo deve ser colocado na pasta "problemas" no diretório do projeto.

Certifique-se de que o problema esteja no formato correto, seguindo as convenções criadas para o trabalho e exemplificadas no arquivo `modelo.md`. Caso a formatação não esteja correta o problema pode não ser resolvido corretamente.

## Executando o código

1. Certifique-se de ter instalado o Python 3.9 ou superior.
2. Abra o terminal e navegue até o diretório onde você baixou/clonou o código.
3. Execute o seguinte comando para rodar o arquivo main.py:

```
python main.py
```

4. Quando solicitado, digite o nome do arquivo, **sem a extensão .txt**, que contém o problema que deseja resolver.

5. **CASO O PROBLEMA SEJA INVIÁVEL OU ILIMITADO, NÃO SERÁ APRESENTADA A FASE SEGUINTE.**

6. Caso o problema seja viável e o programa peça para digitar uma solução básica para o dual, digite os números
   referentes as variáveis que vão entrar na base separados por espaço. Ex:1 3 5. Obs: a primeira coluna
   corresponde ao valor 0 e última coluna m-1, sendo m o número de restrições do dual.

O código será executado e o algoritmo simplex solucionará o problema presente no arquivo de texto.

## Resultados

Após a execução do código, os resultados serão exibidos no terminal. A saída do código irá se tratar das seguintes etapas:

1. Forma padrão do Simplex
2. Problema de primeira fase:
   2.1. Os resultados que estão na base na iteração atual
3. Problema Auxiliar:
   3.1. Os resultados que estão na base na iteração atual
4. Solução do Problema Original
5. Forma padrão do Dual
6. Solução do Dual

Certifique-se de verificar os resultados e interpretá-los corretamente.

Caso você tenha alguma dúvida ou problema, sinta-se à vontade para abrir uma issue no repositório ou entrar em contato com o desenvolvedor.

Aproveite o uso do algoritmo simplex!
