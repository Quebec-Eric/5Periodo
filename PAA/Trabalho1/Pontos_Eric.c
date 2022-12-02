#include <float.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

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

Pontos_Eric *divisao_E_conquista(Pontos_Eric x[], Pontos_Eric y[], int esquerda,
                                 int direita) {
  Pontos_Eric *res = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);

  double delt = 0;
  int meio = 0;
  int contador = 0;

  meio = esquerda + (direita - esquerda) / 2;

  Pontos_Eric *esquerda_P = divisao_E_conquista(x, y, esquerda, meio);
  Pontos_Eric *direita_P = divisao_E_conquista(x, y, meio + 1, direita);

  if (calcular_Distancia(esquerda_P[0], esquerda_P[1]) <
      calcular_Distancia(direita_P[0], direita_P[1])) {
    res = esquerda_P;
  } else {
    res = direita_P;
  }

  delt = calcular_Distancia(res[0], res[1]);

  Pontos_Eric *linhaD = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * sizeof(y));

  for (int i = 0; i < sizeof(y); i++) {
    if (delt > abs(x[meio].eixo_x - y[i].eixo_x)) {
      linhaD[contador] = y[i];
      contador++;
    }
  }

  for (int i = 0; i < contador; i++) {
    int j = i + 1;
    while (j < contador && delt > calcular_Distancia(linhaD[i], linhaD[j])) {
      delt = calcular_Distancia(linhaD[i], linhaD[j]);
      res[0] = linhaD[i];
      res[1] = linhaD[j];
    }
  }

  return res;
}

void heapify(Pontos_Eric lista[], int i, int tamanho, bool x) {
  int e = esq(i);
  int d = dir(i);
  int maior = -1;

  // heapify pelo eixo X
  if (x) {
    if (e < tamanho && lista[e].eixo_x > lista[i].eixo_x)
      maior = e;
    else
      maior = i;

    if (d < tamanho && lista[d].eixo_x > lista[maior].eixo_x)
      maior = d;
  }
  // heapify pelo eixo Y
  else {
    if (e < tamanho && lista[e].eixo_Y > lista[i].eixo_Y)
      maior = e;
    else
      maior = i;

    if (d < tamanho && lista[d].eixo_Y > lista[maior].eixo_Y)
      maior = d;
  }

  if (maior != i) {
    // trocar maior por i
    Pontos_Eric buffer = lista[i];
    lista[i] = lista[maior];
    lista[maior] = buffer;

    // heapify posicao que era maior e contem i
    heapify(lista, maior, tamanho, x);
  }
}

Pontos_Eric *heapSort(Pontos_Eric lista[], int tamanho, bool x) {

  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * tamanho);

  // Copiar lista pra resposta
  for (int i = 0; i < tamanho; i++) {
    resposta[i] = lista[i];
  }

  // Construir heap
  for (int i = sizeof(resposta) / 2; i >= 0; i--) {
    heapify(resposta, i, sizeof(resposta), x);
  }

  // ordenar
  for (int i = sizeof(resposta) - 1; i > 0; i--) {
    // trocar 0 com último
    Pontos_Eric buffer = resposta[0];
    resposta[0] = resposta[i];
    resposta[i] = buffer;

    // heapify resposta[0]
    heapify(resposta, 0, i, x);
  }

  return resposta;
}

Pontos_Eric *algoritmoNLogN1(Pontos_Eric ordenadaX[], Pontos_Eric ordenadaY[],
                             int esq, int dir) {
  // Declaracoes

  Pontos_Eric *resposta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * 2);
  // Caso base 2 pontos
  if (dir - esq == 1) {
    resposta[0] = ordenadaX[esq];
    resposta[1] = ordenadaX[dir];
  }
  // Caso base 3 pontos - compara as 3 distâncias possíveis
  else if (dir - esq == 2) {
    if (calcular_Distancia(ordenadaX[esq], ordenadaX[dir]) >
        calcular_Distancia(ordenadaX[esq], ordenadaX[esq + 1])) {
      resposta[0] = ordenadaX[esq];
      resposta[1] = ordenadaX[dir];
    } else {
      resposta[0] = ordenadaX[esq];
      resposta[1] = ordenadaX[esq + 1];
    }

    if (calcular_Distancia(ordenadaX[esq + 1], ordenadaX[dir]) >
        calcular_Distancia(resposta[0], resposta[1])) {
      resposta[0] = ordenadaX[esq + 1];
      resposta[1] = ordenadaX[dir];
    }
  }
  // Recursão 4 ou mais pontos
  else {
    // Declaracoes locais
    double delta;
    int mid, contador;
    Pontos_Eric *esquerda, *direita;

    // Elemento do meio
    mid = esq + (dir - esq) / 2;

    // Calcular pontos mais proximos de cada metade
    esquerda = algoritmoNLogN1(ordenadaX, ordenadaY, esq, mid);
    direita = algoritmoNLogN1(ordenadaX, ordenadaY, mid + 1, dir);

    // verificar o menor dos dois
    if (calcular_Distancia(esquerda[0], esquerda[1]) <
        calcular_Distancia(direita[0], direita[1])) {
      resposta = esquerda;
    } else {
      resposta = direita;
    }

    // Calcular delta
    delta = calcular_Distancia(resposta[0], resposta[1]);

    // criar lista ordenada pelo eixo Y dos elementos + ou - delta do meio pelo
    // eixo X
    int tt = sizeof(ordenadaX) - 1;
    Pontos_Eric *faixaDelta = (Pontos_Eric *)malloc(sizeof(Pontos_Eric) * tt);

    contador = 0;

    // passar por todos os pontos -- Tempo O(n)
    for (int i = 0; i < sizeof(ordenadaY); i++) {
      // testar se a distância do ponto ao meio é menor que delta
      if (delta > abs(ordenadaX[mid].eixo_x - ordenadaY[i].eixo_x)) {
        faixaDelta[contador] = ordenadaY[i];
        contador++;
      }
    }

    // Verificar do menor para o maior se a distancia entre dois pontos da
    // faixaDelta é menor que delta O(n), pois o while interno é O(1), no máximo
    // 7 tentativas
    for (int i = 0; i < contador; i++) {
      int j = i + 1;
      while (j < contador &&
             delta > calcular_Distancia(faixaDelta[i], faixaDelta[j])) {
        delta = calcular_Distancia(faixaDelta[i], faixaDelta[j]);
        resposta[0] = faixaDelta[i];
        resposta[1] = faixaDelta[j];
      }
    }
  }

  return resposta;
}

Pontos_Eric *algoritmoNLogN(Pontos_Eric lista[]) {
  // Declaracoes
  Pontos_Eric *resposta;
  Pontos_Eric *ordenadaX, *ordenadaY; // listas ordenadas pelo eixo X e eixo Y

  // obter listas ordenadas
  ordenadaX = heapSort(lista, sizeof(lista), true);
  ordenadaY = heapSort(lista, sizeof(lista), false);

  // Calcular pontos mais próximos
  resposta = algoritmoNLogN1(ordenadaX, ordenadaY, 0, sizeof(ordenadaX) - 1);

  return resposta;
}

void iniciando_Divisao_E_Conquista(Pontos_Eric Pontos[], int quantidade) {

  // Resposta resp[2];
  Pontos_Eric *e = heapSort(Pontos, quantidade, true);
  Pontos_Eric *y = heapSort(Pontos, quantidade, false);

  for (int i = 0; i < quantidade; i++) {
    printf("%lf %lf %i\n", e[i].eixo_x, e[i].eixo_Y, e[i].indice);
  }

  return;
}

void iniciar_Problema(Pontos_Eric Pontos[], int quantidade_pontos) {
  comparar_Todos(Pontos, quantidade_pontos);
     Pontos_Eric *res=algoritmoNLogN(Pontos);
    double distancia = calcular_Distancia(res[0],res[1]);
    Resposta *resposta=(Resposta*)malloc(sizeof(Resposta)*2);
    resposta[0].resposta=res[0];
    resposta[1].resposta=res[1];
    toString(resposta,distancia);
  return;
}

int main(int argc, char **argv) {
  mostrar_Rf();
  int quantidade = entrada_Dados();
  Pontos_Eric pontos_no_espaco[quantidade];
  for (int i = 0; i < quantidade; i++) {
    pontos_no_espaco[i] = gerar_Dados(quantidade, i);
    // printf("%lf %lf %i\n",
    // pontos_no_espaco[i].eixo_x,pontos_no_espaco[i].eixo_Y ,
    // pontos_no_espaco[i].indice);
  }
  iniciar_Problema(pontos_no_espaco, quantidade);
  return 0;
}