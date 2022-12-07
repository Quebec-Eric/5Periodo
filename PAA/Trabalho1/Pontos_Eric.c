//Programa de Eric Azevedo de Oliviera
//5 periodo Ciencia da Computacao
//Programa e analise de algoritimo


// Bibliotecas utilizadas
#include <float.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>



// struc para saber os pontos
typedef struct {
  int indice;
  double eixo_x;
  double eixo_Y;
} Pontos_Eric;

// struct para arquivar as respostas
typedef struct {
  Pontos_Eric resposta;

} Resposta;


double distancia_global=0;


//Funcao da tela inicial do programa 
void mostrar_Rf() {
  printf("-----------------------\n");
  printf("Programa feito por Eric\n");
  printf("-----------------------\n\n\n");
  printf("Entre com a quantidade de dados\n");
  printf("Ex: 1000, 100000, 1000000\n");
}

//Funcao para gerar os pontos de forma aleatorias 
Pontos_Eric gerar_Dados(int quantidade, int indice) {
  //variavel
  Pontos_Eric pontos;
  
  //agregando as variaves com valores double randomicos
  pontos.eixo_x = ((double)rand() / (double)(RAND_MAX)*quantidade);
  pontos.eixo_Y = ((double)rand() / (double)(RAND_MAX)*quantidade);
  pontos.indice = indice;

  //retornando os pontos
  return pontos;
}

//funcao para entrada de valores inteiros do teclado
int entrada_Dados() {
  int valor = 0;
  scanf("%d", &valor);
  return valor;
}

// to string para escrever os pontos e a distancia entre os pontos
void toString(Resposta r[], double distancia) {

  printf("\nPrimeiro ponto esta [%lf] do eixo X e [%lf] do eixo Y\n",
         r[0].resposta.eixo_x, r[0].resposta.eixo_Y);
  printf("Segundo ponto esta [%lf] do eixo X e [%lf] do eixo Y\n",
         r[1].resposta.eixo_x, r[1].resposta.eixo_Y);
  printf("Com a distanncia de [%lf] \n", distancia);
  printf("-----------------------------------------------\n");
}

//calcular a distacia euclidiana 
double calcular_Distancia(Pontos_Eric a, Pontos_Eric b) {
  return  sqrt(pow(a.eixo_x - b.eixo_x, 2) + pow(a.eixo_Y - b.eixo_Y, 2));
}

//algoritimo de brut force
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




//funcao para trocar a posicao do vetor da posicao i com a posicao maior
void swap(Pontos_Eric Pontos[], int i , int maior){
  Pontos_Eric temporario = Pontos[i];
  Pontos[i] = Pontos[maior];
  Pontos[maior] = temporario;
  return;
}

//funcao de contrucao  do hip 
void criar_heap(Pontos_Eric Pontos[], int i, int tamanho, bool x) {
  int esquerda = ((i+1)*2)-1;
  int direira = (i+1) * 2;
  int maior = -1;
  if (x==true) {
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

// Funcao para copiar os dados de um vator para outro
Pontos_Eric* copiar_Dados(Pontos_Eric dados_seraoNalisados[],Pontos_Eric Pontos[], int tamanho){
    for (int i = 0; i < tamanho; i++) {
    dados_seraoNalisados[i] = Pontos[i];
  }
  return dados_seraoNalisados;
}

//funcao para realizar a ordenacao , utilizanndo a funcao de contruir acima
Pontos_Eric *heapSort(Pontos_Eric Pontos[], int tamanho, bool x) {
  Pontos_Eric *dadosCopiados = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * tamanho);
    dadosCopiados=copiar_Dados(dadosCopiados,Pontos,tamanho);
  for (int i = tamanho / 2; i >= 0; i--) {
    criar_heap(dadosCopiados, i, tamanho, x);
  }
  for (int i = tamanho - 1; i > 0; i--) {
      swap(dadosCopiados,0,i);
      criar_heap(dadosCopiados, 0, i, x);
  }
  return dadosCopiados;
}


// se so existirem 2 pontos para sevem analisados 
Pontos_Eric * retornar_2Pontos(Pontos_Eric ordenado_eixo_x[],int esquerda, int direira,Pontos_Eric resposta[]){
  resposta[0] = ordenado_eixo_x[esquerda];
  resposta[1] = ordenado_eixo_x[direira];
  return resposta;
}

//funcao para ganhar tempo com 3 pontos apenas
Pontos_Eric * retornar_3Pontos(Pontos_Eric ordenado_eixo_x[],int esquerda, int direita){
  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);
  if (calcular_Distancia(ordenado_eixo_x[esquerda], ordenado_eixo_x[direita]) >
        calcular_Distancia(ordenado_eixo_x[esquerda], ordenado_eixo_x[esquerda + 1])) {
      resposta=retornar_2Pontos(ordenado_eixo_x, esquerda,direita,resposta);
    } else {
       resposta=retornar_2Pontos(ordenado_eixo_x, esquerda,esquerda+1,resposta);
    }
    if (calcular_Distancia(ordenado_eixo_x[esquerda + 1], ordenado_eixo_x[direita]) >
        calcular_Distancia(resposta[0], resposta[1])) {
      resposta=retornar_2Pontos(ordenado_eixo_x, esquerda+1,direita,resposta);
    }
  return resposta;
}



//funcao para fazer a divisao e conquista , dividndo o plano no meio e calular o delta fazendo a recusao
Pontos_Eric *divisao_Conquista(Pontos_Eric ordenado_eixo_x[], Pontos_Eric ordenacao_eixo_Y[],int esq, int dir) {

  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);
  if (dir - esq == 1) {
    resposta = retornar_2Pontos( ordenado_eixo_x, esq,dir,resposta);
  }
  else if (dir -esq == 2) {
   resposta =retornar_3Pontos ( ordenado_eixo_x,esq,dir);  
  }
  else {
    double delta;
    int mid, contador=0;
    Pontos_Eric *quadrande_Q, *quadrande_R;
    mid = esq + (dir - esq) / 2;
    quadrande_Q = divisao_Conquista(ordenado_eixo_x, ordenacao_eixo_Y, esq, mid);
    quadrande_R = divisao_Conquista(ordenado_eixo_x, ordenacao_eixo_Y, mid + 1, dir);

    if (calcular_Distancia(quadrande_Q[0], quadrande_Q[1]) <
        calcular_Distancia(quadrande_R[0], quadrande_R[1])) {
      resposta = quadrande_Q;
    } else {
      resposta = quadrande_R;
    }
    delta = calcular_Distancia(resposta[0], resposta[1]);
    size_t tt = sizeof(ordenado_eixo_x)/sizeof(Pontos_Eric) - 1;

    
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
        resposta=retornar_2Pontos(linha_D, i,j,resposta);
      }
    }
  free(linha_D);
  }
  return resposta;
}

//inicio do divisao e conquista , prerando e ordenndo os vetores em funcao de x e Y
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


void criar_Arquivo_Com_pontos(Pontos_Eric Pontos[], int quantidade){
char buf[128];
FILE *pont_arq; 
pont_arq = fopen("PontosComputados.txt", "w");
for (int i = 0; i < quantidade; i++)
{
  sprintf(buf, "%f", Pontos[i].eixo_x);
  fprintf(pont_arq," X== %s  ",buf);
  sprintf(buf, "%f", Pontos[i].eixo_Y);
  fprintf(pont_arq," Y== %s\n",buf);
}
fclose(pont_arq);


}

//funcao para escolher qual complexidade o user gostaria de uzar
void iniciar_Problema(Pontos_Eric Pontos[], int quantidade_pontos) {
  
  printf("\nGostaria do algoritimo 1==O(n²) ou 2== O(nlogn)\n");
  int valor=entrada_Dados();
  if(valor ==1){
    comparar_Todos(Pontos, quantidade_pontos);
  }
  else{
    Pontos_Eric *res=iniciando_Divisao_E_Conquista(Pontos,quantidade_pontos);
    double distancia = calcular_Distancia(res[0],res[1]);
    Resposta *resposta_proximos=(Resposta*)malloc(sizeof(Resposta)*2);
    resposta_proximos[0].resposta=res[0];
    resposta_proximos[1].resposta=res[1]; 
    printf("\nAlgoritimo O(nlogn) \n");
    toString(resposta_proximos,distancia);
    free(res);
    free(resposta_proximos);
  }
  
  return;


}

//inicio do prograa
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
  criar_Arquivo_Com_pontos(pontos_no_espaco,quantidade);
  return 0;
}