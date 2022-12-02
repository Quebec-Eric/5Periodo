#include <float.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

double distancia_global = 0;
typedef struct {
  int indice;
  double eixo_x;
  double eixo_Y;
} Pontos_Eric;

typedef struct {
  Pontos_Eric resposta;

} Resposta;

void mostrar_Rf() {
  printf("-----------------------\n");
  printf("Programa feito por Eric\n");
  printf("-----------------------\n\n\n");
  printf("Entre com a quantidade de dados\n");
  printf("Ex: 1000, 100000, 1000000\n");
}

Pontos_Eric gerar_Dados(int quantidade, int indice) {
  Pontos_Eric pontos;
  pontos.eixo_x = ((double)rand() / (double)(RAND_MAX)*quantidade);
  pontos.eixo_Y = ((double)rand() / (double)(RAND_MAX)*quantidade);
  pontos.indice = indice;
  return pontos;
}

int entrada_Dados() {
  int valor = 0;
  scanf("%d", &valor);
  return valor;
}

void toString(Resposta r[], double distancia) {

  printf("\nPrimeiro ponto esta [%lf] do eixo X e [%lf] do eixo Y\n",
         r[0].resposta.eixo_x, r[0].resposta.eixo_Y);
  printf("Segundo ponto esta [%lf] do eixo X e [%lf] do eixo Y\n",
         r[1].resposta.eixo_x, r[1].resposta.eixo_Y);
  printf("Com a distanncia de [%lf] \n", distancia);
  printf("-----------------------------------------------\n");
}

double calcular_Distancia(Pontos_Eric a, Pontos_Eric b) {
  double distancia = -1;

  double distancia_X = a.eixo_x - b.eixo_x;
  double distancia_Y = a.eixo_Y - b.eixo_Y;
  distancia = sqrt(pow(distancia_X, 2) + pow(distancia_Y, 2));
  return distancia;
}

void comparar_Todos(Pontos_Eric Pontos[], int quantidade_pontos) {
  Resposta resp[2];
  double menor_distancia = DBL_MAX;

  for (int i = 0; i < quantidade_pontos; i++) {
    for (int z = i + 1; z < quantidade_pontos; z++) {
      double ds = calcular_Distancia(Pontos[i], Pontos[z]);
      if (ds < menor_distancia) {
        distancia_global = ds;
        menor_distancia = ds;
        resp[0].resposta = Pontos[i];
        resp[1].resposta = Pontos[z];
      }
    }
  }
  printf("Utilizando algoritmo de 0(n²)");
  toString(resp, distancia_global);

  return;
}

int esq(int n) { return ((n + 1) * 2) - 1; }
int dir(int n) { return (n + 1) * 2; }


void swap(Pontos_Eric Pontos[], int i , int maior){
  Pontos_Eric temporario = Pontos[i];
  Pontos[i] = Pontos[maior];
  Pontos[maior] = temporario;
}

void criar_heap(Pontos_Eric Pontos[], int i, int tamanho, bool x) {
  int esquerda = esq(i);
  int direira = dir(i);
  int maior = -1;
  if (x) {
    if (esquerda < tamanho && Pontos[esquerda].eixo_x > Pontos[i].eixo_x)
      maior = esquerda;
    else
      maior = i;

    if (direira < tamanho && Pontos[direira].eixo_x > Pontos[maior].eixo_x)
      maior = direira;
  }
  else {
    if (esquerda < tamanho && Pontos[esquerda].eixo_Y > Pontos[i].eixo_Y)
      maior = esquerda;
    else
      maior = i;

    if (direira < tamanho && Pontos[direira].eixo_Y > Pontos[maior].eixo_Y)
      maior = direira;
  }

  if (maior != i) {
     swap(Pontos, i , maior);
    criar_heap(Pontos, maior, tamanho, x);
  }
}

Pontos_Eric *heapSort(Pontos_Eric Pontos[], int tamanho, bool x) {

  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * tamanho);
  for (int i = 0; i < tamanho; i++) {
    resposta[i] = Pontos[i];
  }
  for (int i = sizeof(resposta) / 2; i >= 0; i--) {
    criar_heap(resposta, i, sizeof(resposta), x);
  }
  for (int i = sizeof(resposta) - 1; i > 0; i--) {
    
    Pontos_Eric temporario = resposta[0];
    resposta[0] = resposta[i];
    resposta[i] = temporario;
    criar_heap(resposta, 0, i, x);
  }
  return resposta;
}



Pontos_Eric * retornar_2Pontos(Pontos_Eric ordenado_eixo_x[],int esquerda, int direira){
  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);
  resposta[0] = ordenado_eixo_x[esquerda];
  resposta[1] = ordenado_eixo_x[direira];

  return resposta;
}

Pontos_Eric * retornar_3Pontos(Pontos_Eric ordenado_eixo_x[],int esquerda, int direita){
  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);

  if (calcular_Distancia(ordenado_eixo_x[esquerda], ordenado_eixo_x[direita]) >
        calcular_Distancia(ordenado_eixo_x[esquerda], ordenado_eixo_x[esquerda + 1])) {
      resposta[0] = ordenado_eixo_x[esquerda];
      resposta[1] = ordenado_eixo_x[direita];
    } else {
      resposta[0] = ordenado_eixo_x[esquerda];
      resposta[1] = ordenado_eixo_x[esquerda + 1];
    }

    if (calcular_Distancia(ordenado_eixo_x[esquerda + 1], ordenado_eixo_x[direita]) >
        calcular_Distancia(resposta[0], resposta[1])) {
      resposta[0] = ordenado_eixo_x[esquerda + 1];
      resposta[1] = ordenado_eixo_x[direita];
    }

  return resposta;
}




Pontos_Eric *divisao_Conquista(Pontos_Eric ordenado_eixo_x[], Pontos_Eric ordenacao_eixo_Y[],int esq, int dir) {

  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);
  if (dir - esq == 1) {
    resposta = retornar_2Pontos( ordenado_eixo_x, esq,dir);
  }
  else if (dir -esq == 2) {
   resposta =retornar_3Pontos ( ordenado_eixo_x,esq,dir);  
  }
  else {
    double delta;
    int mid, contador=0;
    Pontos_Eric *esquerda, *direita;

    mid = esq + (dir - esq) / 2;

    esquerda = divisao_Conquista(ordenado_eixo_x, ordenacao_eixo_Y, esq, mid);
    direita = divisao_Conquista(ordenado_eixo_x, ordenacao_eixo_Y, mid + 1, dir);

    if (calcular_Distancia(esquerda[0], esquerda[1]) <
        calcular_Distancia(direita[0], direita[1])) {
      resposta = esquerda;
    } else {
      resposta = direita;
    }

    
    delta = calcular_Distancia(resposta[0], resposta[1]);

    int tt = sizeof(ordenado_eixo_x) - 1;
    Pontos_Eric *linha_D = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * tt);


    int tamano=sizeof(ordenacao_eixo_Y);
    for (int i = 0; i <tamano ; i++) {  
      if (delta > abs(ordenado_eixo_x[mid].eixo_x - ordenacao_eixo_Y[i].eixo_x)) {
        linha_D[contador] = ordenacao_eixo_Y[i];
        contador++;
      }
    }

    for (int i = 0; i < contador; i++) {
      int j = i + 1;
      while (j < contador &&
             delta > calcular_Distancia(linha_D[i], linha_D[j])) {
        delta = calcular_Distancia(linha_D[i], linha_D[j]);
        resposta[0] = linha_D[i];
        resposta[1] = linha_D[j];
      }
    }
  }

  return resposta;
}

Pontos_Eric *iniciando_Divisao_E_Conquista(Pontos_Eric Pontos[], int quantidade_pontos) {
  
  Pontos_Eric *resultado;
  Pontos_Eric *ordenado_eixo_x= (Pontos_Eric*)malloc(sizeof(Pontos_Eric)*quantidade_pontos);
  Pontos_Eric *ordenacao_eixo_Y= (Pontos_Eric*)malloc(sizeof(Pontos_Eric)*quantidade_pontos); 
  
  ordenado_eixo_x = heapSort(Pontos, quantidade_pontos, true);
  ordenacao_eixo_Y = heapSort(Pontos, quantidade_pontos, false);

  int tamanho= sizeof(ordenado_eixo_x) -1;
  int esquerda=0;
  resultado = divisao_Conquista(ordenado_eixo_x, ordenacao_eixo_Y, esquerda, tamanho);

  free(ordenado_eixo_x);
  free(ordenacao_eixo_Y);

  return resultado;
}



void iniciar_Problema(Pontos_Eric Pontos[], int quantidade_pontos) {
  
  printf("\nGostaria do algoritimo 1==O(n²) ou 2== O(nlogn)\n");
  int valor=entrada_Dados();
  if(valor ==1){
    comparar_Todos(Pontos, quantidade_pontos);
  }
  else{
    Pontos_Eric *res=iniciando_Divisao_E_Conquista(Pontos,quantidade_pontos);
    double distancia = calcular_Distancia(res[0],res[1]);
    Resposta *resposta=(Resposta*)malloc(sizeof(Resposta)*2);
    resposta[0].resposta=res[0];
    resposta[1].resposta=res[1];
    printf("\nAlgoritimo O(nlogn) \n");
    toString(resposta,distancia);
    free(res);
  }
  
  return;


}

int main(int argc, char **argv) {
  mostrar_Rf();
  int quantidade = entrada_Dados();
  Pontos_Eric pontos_no_espaco[quantidade];
  for (int i = 0; i < quantidade; i++) {
    pontos_no_espaco[i] = gerar_Dados(quantidade, i);
    
  }
  double time_spent=0.0;
  clock_t begin =clock();
  iniciar_Problema(pontos_no_espaco, quantidade);
  clock_t end = clock();
  time_spent+=(double)(end-begin)/CLOCKS_PER_SEC;
  printf("Tempo de execucao foi de %f segundos", time_spent);
  return 0;
}