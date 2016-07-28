import java.awt.Color;
import java.awt.Graphics;
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


public class DataCreator2 extends JPanel implements MouseMotionListener, MouseListener{
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
    public DataCreator2() {
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
        	        	socket = new Socket(ip,12345);
        	        	
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
        
        if(mouseDown){
        	g.setColor(Color.black);
        	if(mouseX<150 && mouseY<150 && mouseX>0 && mouseY>0){
        		int mX = (((int)mouseX)/10)*10;
        		int mY = (((int)mouseY)/10)*10;
        		
        		data[(int)(((int)mouseY)/10)][(int)((int)mouseX/10)] = 1;
        		//g.fillRect(mX, mY, 10, 10);
        		
        	}
        	//g.drawOval((int)mouseX-5, (int)mouseY-5, 10, 10);
        }
        
        g.setColor(Color.black);
        
        for(int i = 0; i<data.length;i++){
        	
        	for(int j = 0; j<data[i].length;j++){
            	if(data[i][j] == 1)
            		g.fillRect(j*10, i*10, 10, 10);
            }
        }
        
        g.setColor(Color.red);
        
        for(int i = 0; i<info.length;i++){
        	
        	int value = info[i];
        	g.fillRect(20, 160 + (i*20), value+5, 10);
        	g.drawString(i+"", 10, 170 + (i*20));
        }
        
        
        //g.drawOval(0, 0, getWidth(), getHeight());
        
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
        jFrame.getContentPane().add(new DataCreator2());
        jFrame.setVisible(true);
    }

    
    Runnable mainRunnable = new Runnable() {
		public void run() {
			while(true){
				try {
					Thread.sleep(300);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				int index = 0;
		    	for(int i =0; i<data.length;i++)
		    		for(int j =0; j<data[i].length;j++)
		    		{
		    			byte d = (byte) data[i][j];
		    			
		    			writeData[index] = d;
		    			index++;
		    		}
		    		
		    	
		    			
		    	try {
					out.write(writeData);
					out.flush();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		    	
		    	
		    	try {
		    		index = 0;
		    		System.out.print("Packet Received: ");
		    		int count = 0;
		    		while(in.available()>0){
		    			byte b = in.readByte();
		    			
		    			if(count%4 == 0){
		    				
		    				info[index] = b;
		    				System.out.print(info[index]+" ");
		    				index++;
		    				
		    			}
		    			
		    			count++;
		    		}
		    		System.out.print("\n");
				} catch (Exception e) {
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