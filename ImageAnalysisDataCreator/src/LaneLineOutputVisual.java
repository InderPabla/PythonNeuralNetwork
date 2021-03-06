import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.SystemColor;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.UIManager;

public class LaneLineOutputVisual extends JPanel implements MouseMotionListener, MouseListener, KeyListener{
	 private boolean mouseDown = false;
	 private float mouseX = 0f;
	 private float mouseY = 0f;
	
	 private String imagesDataFolder = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/ImagesDataSet3";
	 private String realData1 = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/output_3.txt";
	 private String realData2 = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/RealData3/raw_data.txt";
	 private File[] files;
	 private int fileIndex = 0;
	 private float animationFileIndex = 0;
	 private float animationSpeed = 0.05f;
	 private Rectangle[][] savingPoints1;
	 private Rectangle[][] savingPoints2;
	 
	 private boolean movingPoint = true;
	 private int movingPointIndex= 0;
	 private int numberOfPoints = 4;

	 private float scaleFactor = 4f;
	 private float originalImageWidth = 100f;
	 private float originalImageHeight = 56f;
	 private int boxSize = 10;
	 private float lineWidth = 1f;
	 float start = 0f;
	 
	 @Override
	 public void paintComponent(Graphics g) {
	        super.paintComponent(g);
	        
	        if(start>100){
	        Rectangle[] drawPoints1;
	        Rectangle[] drawPoints2;
	        
        	try {
 				Image image = ImageIO.read(files[(int)animationFileIndex]);
 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
 	        } catch (IOException e) {
 				e.printStackTrace();
 			}
        	
        	
        	Graphics2D g2 = (Graphics2D) g;
        	drawPoints1 = savingPoints1[(int)animationFileIndex];
	        g2.setColor(Color.red);
	        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
	        
	        
	        float intersectionX = 0;
	        float intersectionY = 0;
	        /*float a1 = (drawPoints1[1].y-drawPoints1[0].y)/(drawPoints1[1].x-drawPoints1[0].x);
	        float b1 = drawPoints1[0].y - (a1*drawPoints1[0].x); 
	        float a2 = (drawPoints1[3].y-drawPoints1[2].y)/(drawPoints1[3].x-drawPoints1[2].x);
	        float b2 = drawPoints1[2].y - (a2*drawPoints1[2].x);
	        float newX =  -(b1-b2)/(a1-a2);
	        float newY = (a1*newX)+b1;*/
	       
	        
	        //g2.drawLine(drawPoints1[0].x, drawPoints1[0].y, drawPoints1[1].x, drawPoints1[1].y);
	        //g2.drawLine(drawPoints1[2].x, drawPoints1[2].y, drawPoints1[3].x, drawPoints1[3].y);
	         //g2.drawLine((int)xi, (int)yi,  drawPoints1[1].x, drawPoints1[1].y);
	         //g2.drawLine((int)xi, (int)yi, drawPoints1[3].x, drawPoints1[3].y);
	         
	        
	        g2.setColor(Color.green);
	        drawPoints2 = savingPoints2[(int)animationFileIndex];
	        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
	        
	        
	        float x1 = drawPoints2[0].x;
	        float y1 = drawPoints2[0].y;
	        float x2 = drawPoints2[1].x;
	        float y2 = drawPoints2[1].y;
	        float x3 = drawPoints2[2].x;
	        float y3 = drawPoints2[2].y;
	        float x4 = drawPoints2[3].x;
	        float y4 = drawPoints2[3].y;
	        
	        float d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4);
	        float xi = ((x3-x4)*(x1*y2-y1*x2)-(x1-x2)*(x3*y4-y3*x4))/d;
	        float yi = ((y3-y4)*(x1*y2-y1*x2)-(y1-y2)*(x3*y4-y3*x4))/d;
	        
	        
	        g2.drawLine((int)xi, (int)yi, drawPoints2[1].x, drawPoints2[1].y);
	        g2.drawLine((int)xi, (int)yi, drawPoints2[3].x, drawPoints2[3].y);
	        
	        
	        g.setColor(Color.red);
	        g.setFont(new Font("TimesRoman", Font.BOLD, 15)); 
	        g.drawString("File Index At: "+fileIndex, 10, 240); //new Font(Font.MONOSPACED, Font.BOLD, 15)
	        
	        animationFileIndex += animationSpeed;
	        
	        if((int)animationFileIndex>=files.length)
	        	animationFileIndex = 0;
	        }
	        start+=0.01f;
	        repaint();
	        
	 }
	
	
	
	/**
	 * Create the application.
	 */
	public LaneLineOutputVisual() {
		setBackground(SystemColor.activeCaption);
        setLayout(null);
        
        files = new File(imagesDataFolder).listFiles();
        Arrays.sort(files, new Comparator<File>() {
            public int compare(File f1, File f2) {
                try {
                    String name1 = f1.getName().substring(0,f1.getName().indexOf("."));
                    String name2 = f2.getName().substring(0,f2.getName().indexOf("."));
                	int i1 = Integer.parseInt(name1);
                    int i2 = Integer.parseInt(name2);
                    return i1 - i2;
                } catch(NumberFormatException e) {
                    throw new AssertionError(e);
                }
            }
        });
        
        for(int i = 0; i<files.length;i++){
        	String name = files[i].getName();
        	System.out.println(name);
        }

        
        Scanner scanner = null;
        try {
        	scanner = new Scanner(new FileReader(new File(realData1)));
        	
        	savingPoints1 = new Rectangle[files.length][numberOfPoints];
            for(int i = 0; i<files.length;i++){
            	for(int j = 0; j<numberOfPoints;j++){  	
            		int scaledBox = (int)(boxSize*scaleFactor);
            		float x = scanner.nextFloat()*(originalImageWidth*scaleFactor);
            		
            		float y = (int)(originalImageHeight*scaleFactor) - (int)scaledBox;
    				if(j %2 == 0){
    					y = scaledBox;
    				}
 
                	savingPoints1[i][j] = new Rectangle((int)x,(int)y,scaledBox,scaledBox);
                }
            }
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        scanner.close();
        
        try {
        	scanner = new Scanner(new FileReader(new File(realData2)));
        	
        	savingPoints2 = new Rectangle[files.length][numberOfPoints];
            for(int i = 0; i<files.length;i++){
            	for(int j = 0; j<numberOfPoints;j++){
            		int scaledBox = (int)(boxSize*scaleFactor);
            		float x = scanner.nextFloat()*(originalImageWidth*scaleFactor);
            		
            		float y = (int)(originalImageHeight*scaleFactor) - (int)scaledBox;
    				if(j %2 == 0){
    					y = scaledBox;
    				}
 
                	savingPoints2[i][j] = new Rectangle((int)x,(int)y,scaledBox,scaledBox);
                	
                	
                	
    				
    				

                }
            }
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        scanner.close();
        
        
       
        this.setFocusable(true);
        this.requestFocusInWindow();
        this.addMouseListener(this);
        this.addMouseMotionListener(this);
        this.addKeyListener(this);
        
        
        //==============================FILE NAME CHANGE===========================================
        /*for(int i = 0; i<files.length;i++){
        	int index1 = files[i].getName().indexOf("-");
        	int index2 = files[i].getName().indexOf(".");
        	String name = files[i].getName().substring(index1+1, index2);
        	File fileReplace = new File(dataFolder+"/"+name+".png");
        	files[i].renameTo(fileReplace);
        	System.out.println(name);
        }*/
       //==============================FILE NAME CHANGE===========================================
       
	}

	public float scalePointXAsOutput(float point){
		return point/(originalImageWidth*scaleFactor);
	}
	public float scalePointYAsOutput(float point){
		return point/(originalImageHeight*scaleFactor);
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
		movingPoint = false;
		
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
		
		/*if(mouseDown){
			if(movingPoint == false){
				for(int i =0;i<numberOfPoints;i++){
					if(savingPoints[fileIndex][i].contains(mouseX, mouseY) == true){
						movingPointIndex = i;
						break;
					}
				}
				movingPoint = true;
			}
			else{
				savingPoints[fileIndex][movingPointIndex].setLocation((int)mouseX-savingPoints[fileIndex][movingPointIndex].width/2, (int)mouseY-savingPoints[fileIndex][movingPointIndex].height/2);
			}
		
		}*/
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
	}
	
	
	@Override
	public void keyPressed(KeyEvent arg0) {
		// TODO Auto-generated method stub

	}



	@Override
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub
		if(e.getKeyCode() == KeyEvent.VK_A){
			fileIndex--;
			if(fileIndex <0)
				fileIndex = 0;
			
			
		}
		
		if(e.getKeyCode() == KeyEvent.VK_D){
			fileIndex++;
			if(fileIndex>=files.length)
				fileIndex = files.length - 1;
		}

	}



	@Override
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub

		
	}
	
	
	
	
	public static void main(String[] args) {
		try {
	        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
	    } catch(Exception e) {
	        System.out.println("Error setting native LAF: " + e);
	    }
    	
        JFrame jFrame = new JFrame();
        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jFrame.setSize(420, 285);
        jFrame.getContentPane().add(new LaneLineOutputVisual());
        jFrame.setVisible(true);
        
	}


}
