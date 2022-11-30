#include <stdio.h>
#include <float.h>
#include <stdlib.h>
#include <math.h>


int indice=0;
typedef struct 
{
    int indice;
    int eixo_x;
    int eixo_Y;
}Pontos_Eric;

void Mostrar_Rf(){
    printf("-----------------------\n");
    printf("Programa feito por Eric\n");
    printf("-----------------------\n\n\n");
    printf("Entre com a quantidade de dados\n");
    printf("Ex: 1000, 100000, 1000000\n");
    
}

Pontos_Eric Criar_Dados(int quantidade , int indice){

    Pontos_Eric pontos; 
    pontos.eixo_x =rand()%quantidade;
    pontos.eixo_Y=rand()%quantidade;
    pontos.indice=indice;
    return pontos;
}

int EntradaDado(){
    int valor=0;
    scanf("%d",&valor);
    return valor;
}

float Distancia_Euclidiana(Pontos_Eric PontosP1,Pontos_Eric Pontosp2){

    return sqrt( (PontosP1.eixo_x- Pontosp2.eixo_x)*
                (PontosP1.eixo_x- Pontosp2.eixo_x)+
                (PontosP1.eixo_Y- Pontosp2.eixo_Y)*
                (PontosP1.eixo_Y- Pontosp2.eixo_Y));
}

void Comparar_Todos(Pontos_Eric *PontosP, int quantidade){

    int Ponto1=0;
    int Ponto2=0;
    float distanncia=FLT_MAX;
    for (int i = 0; i < quantidade; i++)
    {
        for (int z=i+1; z <quantidade; z++)
        {
            if (Distancia_Euclidiana(PontosP[i],PontosP[z])< distanncia)
            {
                distanncia=Distancia_Euclidiana(PontosP[i],PontosP[z]);
                Ponto1=PontosP[i].indice;
                Ponto2=PontosP[z].indice;
            }
            
        }
        
    }
    
    printf("Os pontos mais proximos sao %d   %d \n",Ponto1,Ponto2);
    printf("Com a distancia de %lf", distanncia);
    



}


void Intercalar(Pontos_Eric*Pontos, int esquerda, int meio, int direita){

    int n1=0;
    int n2=0;
    int i=0;
    int j=0;
    int k =0;

    n1=meio-esquerda+1;
    n2=direita-meio;
    
    Pontos_Eric e1[n1+1];
    Pontos_Eric e2[n2+1];


    for (i = 0; i < n1; i++)
    {
        e1[i]=Pontos[esquerda+i];
    }


    for (j = 0; j < n2; j++)
    {
        e2[i]=Pontos[meio+j+1];
    }
    

    


}


void Mergsort(Pontos_Eric *Pontos, int esquerda, int direita){

    if(esquerda<direita){
        int meio = (Pontos,esquerda+direita)/2;
        Mergsort(Pontos,esquerda,meio);
        Mergsort(Pontos,meio+1, direita);
        Intercalar(Pontos,esquerda,meio,direita);
    }
}


void DivisaoEConquita(Pontos_Eric *PontosP, int n){




}



void Achar_Pontos_Proximos(Pontos_Eric *PontosP, int n){

    int fazer=0;
    printf("\nGotsaria de fazer 1=O(n²) ou  2=O(nlogn)\n");
    fazer=EntradaDado();
    if (fazer==1)
    {
        Comparar_Todos(PontosP,n);
    }
    else{
        DivisaoEConquista(PontosP,n);
    }
    

    return;
}



int main(int argc, char **argv){
    Mostrar_Rf();
    int valor=EntradaDado();    
    Pontos_Eric *PontosP = (Pontos_Eric*)malloc(valor*sizeof(Pontos_Eric));
    for (int i = 0; i <valor; i++)
    {
        PontosP[i]=Criar_Dados(valor,i);
    }
    Achar_Pontos_Proximos(PontosP,valor);
    return 0;
}
