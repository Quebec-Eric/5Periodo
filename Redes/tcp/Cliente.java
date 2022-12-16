import java.io.*;
import java.net.*;

class Cliente
{
   private static int portaServidor = 1024;

   public static String lerString () throws Exception {
      BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
      return in.readLine();
   }

   public static void main(String argv[]) throws Exception
   {
      //Efetua a primitiva socket
      Socket socket = new Socket("127.0.0.1", portaServidor);

      //Efetua a primitiva send
      DataOutputStream saida = new DataOutputStream(socket.getOutputStream());
      saida.writeBytes(lerString() + '\n');


      //Efetua a primitiva receive
      BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
      System.out.println("FROM SERVER: " + entrada.readLine());

      //Efetua a primitiva close
      socket.close();
   }
}
