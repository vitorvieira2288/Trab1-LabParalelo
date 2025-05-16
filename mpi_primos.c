#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>

int primo(long int n) {
    int i;
    for (i = 3; i < (int)(sqrt(n) + 1); i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main(int argc, char *argv[]) {
    double t_inicial, t_final;
    int cont = 0, total = 0;
    long int i, n;
    int meu_ranque, num_procs, inicio, salto;
    MPI_Status status;

    if (argc < 2) {
        printf("Valor inválido! Entre com um valor do maior inteiro\n");
        return 0;
    } else {
        n = strtol(argv[1], (char **) NULL, 10);
    }

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &meu_ranque);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    t_inicial = MPI_Wtime();

    inicio = 3 + meu_ranque * 2;
    salto = num_procs * 2;
    for (i = inicio; i <= n; i += salto) {
        if (primo(i) == 1) cont++;
    }

    if (num_procs > 1) {
        if (meu_ranque != 0) {
            

            // 1. MPI_Send
			/*
            MPI_Send(&cont, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
			*/
            // 2. MPI_Isend
            /*
            MPI_Request request;
            MPI_Isend(&cont, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &request);
            MPI_Wait(&request, &status);
            */

            // 3. MPI_Rsend
            /*
            MPI_Rsend(&cont, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
            */

            // 4. MPI_Bsend
            /*
            int buffer_size = MPI_BSEND_OVERHEAD + sizeof(int);
            char *buffer = (char *)malloc(buffer_size);
            MPI_Buffer_attach(buffer, buffer_size);
            MPI_Bsend(&cont, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
            MPI_Buffer_detach(&buffer, &buffer_size);
            free(buffer);
            */

            // 5. MPI_Ssend
            
            MPI_Ssend(&cont, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
            
        } else {
           

           //MPI_Recv 
			/*
            total = cont; 
            int received_cont;
            for (int j = 1; j < num_procs; j++) {
                MPI_Recv(&received_cont, 1, MPI_INT, j, 0, MPI_COMM_WORLD, &status);
                total += received_cont;
            }
			*/
            //MPI_Irecv
            
            total = cont; 
            int received_cont[num_procs - 1];
            MPI_Request requests[num_procs - 1];
            for (int j = 1; j < num_procs; j++) {
                MPI_Irecv(&received_cont[j - 1], 1, MPI_INT, j, 0, MPI_COMM_WORLD, &requests[j - 1]);
            }
            for (int j = 0; j < num_procs - 1; j++) {
                MPI_Wait(&requests[j], &status);
                total += received_cont[j];
				printf("teste5\n");
            }
            
        }
    } else {
        total = cont;
    }

    t_final = MPI_Wtime();

    if (meu_ranque == 0) {
        total += 1; /* Acrescenta o dois, que também é primo */
        printf("Quant. de primos entre 1 e n: %d \n", total);
        printf("Tempo de execucao: %1.3f \n", t_final - t_inicial);
    }

    MPI_Finalize();
    return 0;
}
