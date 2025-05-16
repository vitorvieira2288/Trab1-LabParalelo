#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int primo(int n) {
    int i;
    for (i = 3; i < (int)(sqrt(n) + 1); i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main(int argc, char *argv[]) { /* mpi_primosbag.c */
    clock_t inicio, final;
    double time;
    int cont = 0, total = 0;
    int i, n;
    
    /* Verifica o número de argumentos passados */
    if (argc < 2) {
        printf("Entre com o valor do maior inteiro como parâmetro para o programa.\n");
        return 0;
    } else {
        n = strtol(argv[1], (char **) NULL, 10);
    }

    /* Registra o tempo inicial de execução do programa */
    inicio = clock();


    for (int i = 3; i < n; i += 2) {
        if (primo(i) == 1)
            cont++;
    } 

    /* Registra o tempo final de execução */
    final = clock();

    time = ((double)(final - inicio)) / CLOCKS_PER_SEC;

    printf("%ld %ld %f", inicio, final, time);

    cont += 1;    /* Acrescenta o 2, que é primo */
    printf("Quant. de primos entre 1 e %d: %d \n", n, cont);
    printf("Tempo de execucao: %1.3f \n", time);     
    
    
    return(0);
}
