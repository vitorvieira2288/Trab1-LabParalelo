# Trabalho de Programação Paralela

O trabalho consiste em executar programas paralelos de encontrar números primos em um intervalo, usando o algoritmo de Naive, e o Bag of Tasks em todas as combinações de sends
e revcs do MPI que façam sentido com o algoritmo, coletar os tempos de execução e então obter o speed-up e eficiência em todos os casos.

## Runner

O Runner é um programa em Python implementado neste trabalho para executar os programas de forma automática e gerar relatórios.
Ao executar o Runner, podemos definir qual dos dois algoritmos será executado (naive ou bag of tasks) e então ele criará uma pasta
`relatório/<algoritmo>/` e, para cada versão do algoritmo contido na pasta do algoritmo, ele criará uma nova pasta.
Essa nova pasta contém 4 arquivos txt. Um com todos os tempos de execução para 1 processo, e a média no final. Um com os tempos e média
para 2 processos, e um para 4 processos. E um arquivo chamado `avaliacao.txt`, que contém os speed-ups e eficiências.

Para rodar o runner, execute no terminal na raiz do projeto:

```
python3 runner <pasta> -e <quantidade_de_execucoes>
```

O parâmetro de quantidade de execuções indica quantas vezes um único programa é executado. Pode ser omitido, sendo o valor padrão igual a 30.

Exemplo de uso: Para rodar cada programa da pasta naive 10 vezes, rode:

```
python3 runner naive -e 10
```

***Nota1***: Caso a execução do mpirun não funcione, entre no arquivo `runner/run_mpi.py` e verifique se o comando da linha 71 corresponde a forma com que
você normalmente roda o mpirun.

***Nota2***: O runner sempre recompila todos os programas com o mpicc. Caso algum programa não compile, verifique a função de compilar do módulo `runner/run_mpi.py`
para garantir que a linha 37 está em conformidade com a forma com que você roda o mpicc.

## Algoritmos

Para conferir os algoritmos, basta olhar a pasta `naive`, ou a pasta `bag_of_tasks`
