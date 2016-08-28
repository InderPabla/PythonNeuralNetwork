import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.imageio.ImageIO;
import javax.swing.JButton;
import java.awt.Panel;
import javax.swing.JLabel;
import java.awt.SystemColor;
import java.awt.Font;


public class ImageShower extends JPanel implements MouseMotionListener, MouseListener{
	private boolean mouseDown = false;
	private float mouseX = 0f;
	private float mouseY = 0f;
	private int[][] data = new int[15][15];
	private int[] info = new int[10];
	int testSet = 70;
	int setItem = 0;
	
	Socket socket;
	InetAddress ip;
	OutputStream outToServer;
	DataOutputStream out;
	
	InputStream inToServer;
	DataInputStream in;
	
	byte[] writeData = new byte[15*15];
	Image m;
    public ImageShower() {
        setBackground(SystemColor.activeCaption);
        setLayout(null);
        
        JButton clearButton = new JButton("Clear");
        clearButton.setFont(new Font("Tahoma", Font.BOLD, 11));
        clearButton.setForeground(Color.RED);
        clearButton.setBounds(10, 372, 61, 23);
        add(clearButton);
        
        clearButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				
				data = new int[15][15];
			}
		});
        
        this.addMouseListener(this);
        this.addMouseMotionListener(this);
        
        JButton saveButton = new JButton("Save");
        saveButton.setFont(new Font("Tahoma", Font.BOLD, 11));
        saveButton.setForeground(Color.RED);
        saveButton.setBounds(81, 372, 61, 23);
        add(saveButton);
        
        JButton startConnectionButton = new JButton("Connect");
        startConnectionButton.setForeground(Color.RED);
        startConnectionButton.setFont(new Font("Tahoma", Font.BOLD, 11));
        startConnectionButton.addActionListener(new ActionListener() {
        	public void actionPerformed(ActionEvent arg0) {
        		 try{

        	        	ip = InetAddress.getLocalHost();
        	        	socket = new Socket(ip,5000);
        	        	
        	        	outToServer = socket.getOutputStream();
        	            out = new DataOutputStream(outToServer);
        	        	
        	            inToServer = socket.getInputStream();
        	            in = new DataInputStream(inToServer);
        	            
        	            Thread mainThread = new Thread(mainRunnable);
        	    		mainThread.start(); // Start the main thread.
        	            
        	        }
        	        catch(Exception error){System.out.println(error);}
        	}
        });
        startConnectionButton.setBounds(152, 372, 86, 23);
        add(startConnectionButton);
        
        
        
        
        saveButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				
				String path = testSet+"_"+setItem+".png";
			    BufferedImage image = new BufferedImage(15, 15, BufferedImage.TYPE_INT_RGB);
			    for (int x = 0; x < 15; x++) {
			        for (int y = 0; y < 15; y++) {
			        	Color c = Color.white;
			        	if(data[x][y]==1)
			        		c = Color.black;
			            image.setRGB(y, x, c.getRGB());
			        }
			    }

			    File ImageFile = new File(path);
			    try {
			        ImageIO.write(image, "png", ImageFile);
			    } catch (IOException e) {
			        e.printStackTrace();
			    }
			    
			    setItem++;
			    if(setItem == 10){
			    	testSet++;
			    	setItem = 0;
			    }
			    data = new int[15][15];
				    
			}
		});
        
        
        startConnectionButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				/*try {
					socket.close();
				} catch (IOException e) {}
				System.exit(0);*/
				
				
				    
			}
		});
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        g.setColor(Color.white);
        g.fillRect(0, 0, 150, 150);
        
        
        g.drawImage(m, 0, 0, 50, 50, null);
        
        repaint();
    }

    public static void main(String[] args) {
    	try {
	        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
	    } catch(Exception e) {
	        System.out.println("Error setting native LAF: " + e);
	    }
    	
        JFrame jFrame = new JFrame();
        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jFrame.setSize(265, 450);
        jFrame.getContentPane().add(new ImageShower());
        jFrame.setVisible(true);
    }

    
    Runnable mainRunnable = new Runnable() {
		public void run() {
			while(true){
				/*try {
					Thread.sleep(300);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}*/
				
				
				try {
					//System.out.println("GOT IT");
					while(in.available()>0){
						byte b = in.readByte();
						
						System.out.print(b+" ");
					}
					//System.out.println("DONE IT");
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				System.out.println("getting");
				try {
					m = ImageIO.read(new File("C:\\Users\\Pabla\\Desktop\\ImageAnalysis\\a.png"));
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				try {
					out.writeInt(12);
					out.flush();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				
		    	
			}
		}
	};
	
	@Override
	public void mouseClicked(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		mouseDown = true;
	}

	@Override
	public void mouseReleased(MouseEvent arg0) {
		// TODO Auto-generated method stub
		mouseDown = false;
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
		
	}
}