import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.ServerSocket;
import java.net.Socket;
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
		
        return id_Produto +":" +nome_Produto + ":R$" + valor_Produto +"|";
    }
}


public class Server {
	public static Produtos[] produtos = new Produtos[5];
    public static ArrayList<Produtos> ProdutosCompras = new ArrayList();

    private static String MostrarProdutos() throws IOException {
        String todosOsProdutos = "";
        for (int i = 0; i < produtos.length; i++) {
            todosOsProdutos += produtos[i].toStrinng();
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
		// TCP
		CriarProdutos();
		new Thread(new Runnable() {
			@Override
			public void run() {
				ExecutorService executor = null;
				try (ServerSocket server = new ServerSocket(1024)) {
					executor = Executors.newFixedThreadPool(5);
					System.out.println("Listening on TCP port 1234, Say hi!");
					while (true) {
						final Socket socket = server.accept();
						executor.execute(new Runnable() {
							@Override
							public void run() {
								String inputLine = "";
								System.err.println(
										socket.toString() + " ~> connected");
								try (PrintWriter out = new PrintWriter(
										socket.getOutputStream(), true);
										BufferedReader in = new BufferedReader(
												new InputStreamReader(socket
														.getInputStream()))) {
									while (!inputLine.equals("!quit")& (inputLine = in.readLine()) != null) {
										System.out.println(inputLine);
										if(inputLine.equals("Listar")){
											String pegar =MostrarProdutos();
											
											out.println(pegar);
										}
										if(inputLine.equals("Comprar")){
										String total=	MostrarPrecoFinal() ;
										out.println(total);
										}
										

										
									}
								} catch (IOException ioe) {
									ioe.printStackTrace();
								} finally {
									try {
										System.err.println(socket.toString()
												+ " ~> closing");
										socket.close();
									} catch (IOException ioe) {
										ioe.printStackTrace();
									}
								}
							}
						});
					}
				} catch (IOException ioe) {
					System.err.println("Cannot open the port on TCP");
					ioe.printStackTrace();
				} finally {
					System.out.println("Closing TCP server");
					if (executor != null) {
						executor.shutdown();
					}
				}
			}
		}).start();

		// UDP
		new Thread(new Runnable() {
			@Override
			public void run() {
				try (DatagramSocket socket = new DatagramSocket(1024)) {
					byte[] buf = new byte[socket.getReceiveBufferSize()];
					DatagramPacket packet = new DatagramPacket(buf, buf.length);

					System.out.println("Listening on UDP port 1234, Say hi!");
					while (true) {
						socket.receive(packet);
						
						String pegar =new String(packet.getData());
						
						//AdicionarProcuto(Integer.parseInt(pegar));
						
						socket.send(packet);
					}
				} catch (IOException ioe) {
					System.err.println("Cannot open the port on UDP");
					ioe.printStackTrace();
				} finally {
					System.out.println("Closing UDP server");
				}
			}
		}).start();
	}
}