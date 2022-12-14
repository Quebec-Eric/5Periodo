import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.ArrayList;

class Produtos {

    private String nome_Produto;
    private int valor_Produto;
    private int id_Produto;

    Produtos(String nom, int valor, int id) {
        this.id_Produto=id;
        this.nome_Produto = nom;
        this.valor_Produto = valor;
    }

    public int getValor() {
        return this.valor_Produto;

    }


    public String toStrinng() {
        return this.id_Produto +":" +this.nome_Produto + ":" + this.valor_Produto +"|";
    }
}


public class Server extends Thread {

    private static Produtos[] produtos = new Produtos[5];
    private static ArrayList<Produtos> ProdutosCompras = new ArrayList();

    private static String MostrarProdutos() throws IOException {
        String todosOsProdutos = "";
        for (int i = 0; i < produtos.length; i++) {
            todosOsProdutos += produtos[i].toString();
        }
        return todosOsProdutos;

    }

    private static String MostrarPrecoFinal() throws IOException {

        int valor_Final = 0;
        String resultado = "";
        for (int i = 0; i < ProdutosCompras.size(); i++) {
            resultado += ProdutosCompras.get(i) + "/";
            valor_Final += ProdutosCompras.get(i).getValor();
        }
        resultado += "||" + valor_Final;
        return resultado;

    }

    public static void CriarProdutos(){
        produtos[0]= new Produtos("Banada",3, 1);
        produtos[1]= new Produtos("Refri",10, 2);
        produtos[2]= new Produtos("Pao",2, 3);
        produtos[3]= new Produtos("Cerveja",8, 4);
        produtos[4]= new Produtos("Biscoito",5, 5);
        return;
    }




    public static void AdicionarProcuto(int idPodutor){
        ProdutosCompras.add(produtos[idPodutor-1]);
    }

    public static void main(String[] args) {
        CriarProdutos();

        new Thread(new Runnable() {
            @Override
            public void run() {
                ExecutorService executor = null;
                try (ServerSocket server = new ServerSocket(666)) {
                    executor = Executors.newFixedThreadPool(5);
                    System.out.println("Porta TCP!");
                    while (true) {
                        final Socket socket = server.accept();
                        executor.execute(new Runnable() {
                            @Override
                            public void run() {
                                String inputLine = "";
                                System.err.println("connected");
                                try (PrintWriter out = new PrintWriter(
                                        socket.getOutputStream(), true);
                                        BufferedReader in = new BufferedReader(
                                                new InputStreamReader(socket
                                                        .getInputStream()))) {
                                    while (!inputLine.equals("!quit")
                                            && (inputLine = in
                                                    .readLine()) != null) {
                                        if (inputLine.equals("Listar")) {

                                            String str = MostrarProdutos();
                                            DataOutputStream saida = new DataOutputStream(socket.getOutputStream());
                                            saida.writeBytes(str);
                                        } else if (inputLine.equals("Comprar")) {
                                            String str = MostrarPrecoFinal();
                                            DataOutputStream saida = new DataOutputStream(socket.getOutputStream());
                                            saida.writeBytes(str);

                                        }

                                    }
                                } catch (IOException ioe) {
                                }
                            }
                        });
                    }
                } catch (IOException ioe) {}
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try (DatagramSocket socket = new DatagramSocket(666)) {
                    byte[] buf = new byte[socket.getReceiveBufferSize()];
                    DatagramPacket packet = new DatagramPacket(buf, buf.length);

                    System.out.println(" UDP 666");
                    while (true) {
                        socket.receive(packet);
                        
                        String recebedio =(new String(packet.getData()));
                        if (!recebedio.equals("Comprar") && !recebedio.equals("Listar")) {
                            AdicionarProcuto(Integer.parseInt(recebedio));
                        }
                    }
                } catch (IOException ioe) {}
            }
        }).start();
    }
}
