import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

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
	private int[][] data = new int[25][25];
	
	int testSet = 9;
	int setItem = 0;
    public DataCreator2() {
        setBackground(SystemColor.activeCaption);
        setLayout(null);
        
        JButton clearButton = new JButton("Clear");
        clearButton.setFont(new Font("Tahoma", Font.BOLD, 11));
        clearButton.setForeground(Color.RED);
        clearButton.setBounds(10, 306, 89, 23);
        add(clearButton);
        
        clearButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				
				data = new int[25][25];
			}
		});
        
        this.addMouseListener(this);
        this.addMouseMotionListener(this);
        
        JButton saveButton = new JButton("Save");
        saveButton.setFont(new Font("Tahoma", Font.BOLD, 11));
        saveButton.setForeground(Color.RED);
        saveButton.setBounds(151, 306, 89, 23);
        add(saveButton);
        
        saveButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				
				String path = testSet+"_"+setItem+".png";
			    BufferedImage image = new BufferedImage(25, 25, BufferedImage.TYPE_INT_RGB);
			    for (int x = 0; x < 25; x++) {
			        for (int y = 0; y < 25; y++) {
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
			    
				    
			}
		});
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        g.setColor(Color.white);
        g.fillRect(0, 0, 250, 250);
        
        if(mouseDown){
        	g.setColor(Color.black);
        	if(mouseX<250 && mouseY<250){
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
        jFrame.setSize(265, 400);
        jFrame.getContentPane().add(new DataCreator2());
        jFrame.setVisible(true);
    }

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