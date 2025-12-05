// Requisito PIM: Módulo crítico em C estruturado 
#include <stdio.h>
#include <stdlib.h>

int validarNota(double nota) {
    return (nota >= 0.0 && nota <= 10.0);
}

int main(int argc, char *argv[]) {
    // O Python vai chamar: ./calculo_media 8.5 7.0
    // Argumentos: [0]programa, [1]Nota, [2]Frequencia(como peso ou extra)
    
    if (argc < 3) {
        return 1; // Erro
    }

    double nota_prova = atof(argv[1]);
    double trabalho = atof(argv[2]); // Vamos considerar o 2º arg como nota de trabalho/atividade

    if (!validarNota(nota_prova) || !validarNota(trabalho)) {
        printf("-1"); // Código de erro para o Python ler
        return 0;
    }

    // Lógica de Negócio "Crítica": Média Ponderada
    // Prova peso 7, Trabalho peso 3
    double media = (nota_prova * 0.7) + (trabalho * 0.3);

    printf("%.2f", media); // Retorna APENAS o número para o Python capturar
    return 0;
}