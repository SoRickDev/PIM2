#include <stdio.h>  // Para printf, fprintf, stderr
#include <stdlib.h> // Para atof (converter string para double)


// Função helper para validar se a nota está entre 0 e 10
int validarNota(double nota) {
    if (nota < 0.0 || nota > 10.0) {
        return 0; // 0 = Inválido
    }
    return 1; // 1 = Válido
}

// Função principal
int main(int argc, char *argv[]) {
    
    // 1. Validar o número de argumentos
    // argc deve ser 4: [0]nome_programa, [1]N1, [2]N2, [3]T1
    if (argc != 4) {
        // Imprime a mensagem de erro no "stderr" (saída de erro)
        fprintf(stderr, "Erro: Numero de argumentos invalido.\n");
        fprintf(stderr, "Uso: %s <nota N1> <nota N2> <trabalho T1>\n", argv[0]);
        return 1; // Retorna 1 (código de erro)
    }

    // 2. Converter os argumentos de string para double
    double n1 = atof(argv[1]);
    double n2 = atof(argv[2]);
    double t1 = atof(argv[3]);

    // 3. Validar o range das notas
    if (!validarNota(n1) || !validarNota(n2) || !validarNota(t1)) {
        fprintf(stderr, "Erro: Todas as notas devem estar entre 0.0 e 10.0.\n");
        return 1; // Código de erro
    }

    // 4. Lógica do Cálculo (Módulo Crítico)
    double peso_provas = 4.0;
    double peso_trabalho = 2.0;
    double total_pesos = (peso_provas * 2) + peso_trabalho; // 10.0

    double mediaFinal = ((n1 * peso_provas) + (n2 * peso_provas) + (t1 * peso_trabalho)) / total_pesos;

    // 5. Imprimir o resultado final (e SÓ o resultado)
    // O Python vai ler esta saída (stdout)
    printf("%.2f", mediaFinal);

    return 0; // Retorna 0 (sucesso)
}