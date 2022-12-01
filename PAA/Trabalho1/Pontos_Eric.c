#include <stdio.h>
#include <float.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

double distancia_global=0;
typedef struct 
{
    int indice;
    double eixo_x;
    double eixo_Y;
}Pontos_Eric;

typedef struct{
    Pontos_Eric resposta;

}Resposta;

void mostrar_Rf(){
    printf("-----------------------\n");
    printf("Programa feito por Eric\n");
    printf("-----------------------\n\n\n");
    printf("Entre com a quantidade de dados\n");
    printf("Ex: 1000, 100000, 1000000\n");
    
}

Pontos_Eric gerar_Dados(int quantidade , int indice){
    Pontos_Eric pontos; 
    pontos.eixo_x =((double)rand()/(double)(RAND_MAX)*quantidade);
    pontos.eixo_Y=((double)rand()/(double)(RAND_MAX)*quantidade);
    pontos.indice=indice;
    return pontos;
}

int entrada_Dados(){
    int valor=0;
    scanf("%d",&valor);
    return valor;
}

void toString(Resposta r[], double distancia){

    printf("\nPrimeiro ponto esta [%lf] do eixo X e [%lf] do eixo Y\n", r[0].resposta.eixo_x , r[0].resposta.eixo_Y);
    printf("Segundo ponto esta [%lf] do eixo X e [%lf] do eixo Y\n", r[1].resposta.eixo_x , r[1].resposta.eixo_Y);
    printf("Com a distanncia de [%lf] \n", distancia);
    printf("-----------------------------------------------\n");

}

double calcular_Distancia(Pontos_Eric a , Pontos_Eric b){
    double distancia =-1;

    double distancia_X= a.eixo_x -b.eixo_x;
    double distancia_Y=a.eixo_Y - b.eixo_Y;
    distancia= sqrt(pow(distancia_X,2)+pow(distancia_Y,2));
    return distancia;
}

void comparar_Todos(Pontos_Eric Pontos[] , int quantidade_pontos){
    Resposta resp[2];
    double menor_distancia=DBL_MAX;

    for (int  i = 0; i < quantidade_pontos; i++)
    {
        for (int z = i+1; z < quantidade_pontos; z++)
        {
            double ds = calcular_Distancia(Pontos[i],Pontos[z]);
            if (ds<menor_distancia)
            {
                distancia_global= ds;
                menor_distancia=ds;
                resp[0].resposta=Pontos[i];
                resp[1].resposta=Pontos[z];

            }
                
        }
        
    }   
    printf("Utilizando algoritmo de 0(n²)");
    toString(resp,distancia_global);
    
    return;
}

int esq(int n){
    return ((n+1)*2)-1;
}
int dir(int n){
    return (n+1)*2;
}

void construcao_heap(Pontos_Eric P[], int i , int quantidade, bool x){

    int esqueda=esq(i);
    int direira=dir(i);
    int maior=-1;

    if(x){
        if(esqueda<quantidade&&P[esqueda].eixo_x>P[i].eixo_x){ 
        maior=esqueda;
        }
        else{
            maior=i;
        }

        if(direira<quantidade&&P[direira].eixo_x>P[i].eixo_x){
            maior=direira;
        }
    }
    else{
        if(esqueda<quantidade&&P[esqueda].eixo_Y>P[i].eixo_Y){ 
        maior=esqueda;
        }
        else{
            maior=i;
        }

        if(direira<quantidade&&P[direira].eixo_Y>P[i].eixo_Y){
            maior=direira;
        }        
    }


    if(maior!=i){

        Pontos_Eric m=P[i];
        P[i]=P[maior];
        P[i]=m;

        construcao_heap(P,maior,quantidade,x);
    }

}



Pontos_Eric * divisao_E_conquista(Pontos_Eric x[], Pontos_Eric y[],int esquerda , int direita){
    Pontos_Eric *res=(Pontos_Eric*)malloc(sizeof(Pontos_Eric)*2);

    double delt=0;
    int meio=0;
    int contador=0;
    
    meio=esquerda+(direita-esquerda)/2;
   Pontos_Eric *esquerda_P=divisao_E_conquista(x,y,esquerda,meio);
   Pontos_Eric *direita_P=divisao_E_conquista(x,y,meio+1,direita);


    if(calcular_Distancia(esquerda_P[0],esquerda_P[1])<calcular_Distancia(direita_P[0],direita_P[1])){
        res=esquerda_P;
    }else{
         res=direita_P;
    }

    delt = calcular_Distancia(res[0], res[1]);

    Pontos_Eric *linhaD= (Pontos_Eric*)malloc(sizeof(Pontos_Eric)*sizeof(y));


    for (int i = 0; i < sizeof(y); i++)
    {
        if(delt>abs(x[meio].eixo_x-y[i].eixo_x)){
            linhaD[contador]=y[i];
            contador++;
        }
    }
    
    for(int i=0;i<contador;i++){
        int j=i+1;
        while (j<contador&& delt>calcular_Distancia(linhaD[i],linhaD[j]))
        {
            delt=calcular_Distancia(linhaD[i],linhaD[j]);
            res[0]=linhaD[i];
            res[1]=linhaD[j];
        }
        
    }

    return res;
}




Pontos_Eric * heapShort(Pontos_Eric P[], int quantidade ,bool x ){
    Pontos_Eric *pontos =(Pontos_Eric*)malloc(sizeof(Pontos_Eric)*quantidade);

    for (int i = 0; i < quantidade; i++)
    {
        pontos[i]=P[i];
    }
    
    for (int i = quantidade/2; i >=0; i--)
    {
        construcao_heap(pontos,i,quantidade,x);
    }
    
    for(int i= quantidade-1;i>0;i--){

        Pontos_Eric b = pontos[0];
        pontos[0]=pontos[i];
        pontos[i]=b;

        construcao_heap(pontos,0,i,x);
    }
    
    return pontos;
}




void  iniciando_Divisao_E_Conquista(Pontos_Eric Pontos[], int quantidade){

    //Resposta resp[2];
    Pontos_Eric *e= heapShort(Pontos,quantidade,true);
    Pontos_Eric *y= heapShort(Pontos,quantidade,false);    
    
    divisao_E_conquista(e,y,0,sizeof(e)-1);
    
    /*for (int  i = 0; i < quantidade; i++)
    {
     printf("%lf %lf %i\n", e[i].eixo_x,e[i].eixo_Y,e[i].indice);
    
    } 
    */   
    
    

    return;
}

void iniciar_Problema(Pontos_Eric Pontos[], int quantidade_pontos){
    comparar_Todos(Pontos,quantidade_pontos);
    iniciando_Divisao_E_Conquista(Pontos, quantidade_pontos);
    return;
} 



int main(int argc, char **argv){
    mostrar_Rf();
    int quantidade = entrada_Dados();
    Pontos_Eric pontos_no_espaco[quantidade];
    for (int i = 0; i < quantidade; i++)
    {
        pontos_no_espaco[i]=gerar_Dados(quantidade,i);
       // printf("%lf %lf %i\n", pontos_no_espaco[i].eixo_x,pontos_no_espaco[i].eixo_Y , pontos_no_espaco[i].indice);
    }
    iniciar_Problema(pontos_no_espaco, quantidade);   
    return 0;
}