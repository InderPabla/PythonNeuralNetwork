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

public class LaneLineDataCreatorSlope extends JPanel implements MouseMotionListener, MouseListener, KeyListener{
	 private boolean mouseDown = false;
	 private float mouseX = 0f;
	 private float mouseY = 0f;
	 private float oldMouseX = 0f;
	 private float oldSlope = 0f;
	 private float oldPosition = 0f;
	 
	 private String imagesDataFolder = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/ImagesDataSet1";
	 //private String realData = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/RealData5/raw_data.txt";
	 private String realData = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/output_1.txt";
	 private File[] files;
	 private int fileIndex = 0;
	 private float animationFileIndex = 0;
	 private float animationSpeed = 0.02f;
	 
	 private boolean animationMode = false;
	 private File rawFile;
	 private float scaleFactor = 4f;
	 private float originalImageWidth = 100f;
	 private float originalImageHeight = 56f;
	 private float boxSize = 10f;
	 private float lineWidth = 1f;
	 
	 
	 private float[][] points;
	 private Rectangle[][] control;
	 
	 private boolean movingPoint = true;
	 private float movingPointIndex= 0;
	 private int numberOfPoints = 4;
	 
	 @Override
	 public void paintComponent(Graphics g) {
	        super.paintComponent(g);
	        Rectangle[] drawControl;
	        
	        Graphics2D g2 = (Graphics2D) g;
	        
	        if(animationMode == false){
	        	try {
	 				Image image = ImageIO.read(files[fileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}

		        g2.setColor(Color.red);
		        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
		        
		        if(points[fileIndex][1] == 1f){
	        		if(fileIndex>0){
	        			
			        	for(int i = 0; i<4;i++){
			        		points[fileIndex][i] = points[fileIndex-1][i];
			        		//control[fileIndex][i] = new Rectangle(control[fileIndex-1][i]);
			        	}
		        	}
		        }
		        
		        float staticCenterY = (originalImageHeight*scaleFactor)/2f;
		        float staticYTop = -200f*scaleFactor;
		        float staticYBottom = 200f*scaleFactor;
		        
		        float x1 = points[fileIndex][0];
		        float m1 = points[fileIndex][1];
		        float b1 = staticCenterY-(x1*m1);
		        
		        float x2 = points[fileIndex][2];
		        float m2 = points[fileIndex][3];
		        float b2= staticCenterY-(x2*m2);
		        
		        
		        float x1_1 = (staticYTop-(b1))/m1;
		        float x1_2 = (staticYBottom-(b1))/m1;


		        float x2_1  = (staticYTop-(b2))/m2;
		        float x2_2  = (staticYBottom-(b2))/m2;
		        
		        
		        g2.drawLine((int)x1_1, (int)staticYTop, (int)x1_2, (int)staticYBottom);
		        
		        g2.drawLine((int)x2_1, (int)staticYTop, (int)x2_2, (int)staticYBottom);
		        
		        drawControl = control[fileIndex];
		        
		        for(int i = 0;i<4;i++){
		        	g.setColor(Color.green);
		        	if(i%2==0)
		        		g.setColor(Color.red);
		        	g2.setStroke(new BasicStroke(1f));
		        	g.drawRect(drawControl[i].x,drawControl[i].y,drawControl[i].width,drawControl[i].height);
		        }
	        }
	        else if(animationMode == true && (int)animationFileIndex < files.length - 1){
	        	try {
	 				Image image = ImageIO.read(files[(int)animationFileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}
	        	
	        	animationFileIndex += animationSpeed;
	        	
	        	
		        
		        float staticCenterY = (originalImageHeight*scaleFactor)/2f;
		        float staticYTop = -200f*scaleFactor;
		        float staticYBottom = 200f*scaleFactor;
		        
		        float x1 = points[(int)animationFileIndex][0];
		        float m1 = points[(int)animationFileIndex][1];
		        float b1 = staticCenterY-(x1*m1);
		        
		        float x2 = points[(int)animationFileIndex][2];
		        float m2 = points[(int)animationFileIndex][3];
		        float b2= staticCenterY-(x2*m2);    
		        
		        float splitY = originalImageHeight*scaleFactor;
		        staticYBottom = splitY;
		        
		        float x1_1 = (staticYTop-(b1))/m1;
		        float y1_1 = staticYTop;
		        float x1_2 = (staticYBottom-(b1))/m1;
		        float y1_2 = staticYBottom;

		        float x2_1  = (staticYTop-(b2))/m2;
		        float y2_1 = staticYTop;
		        float x2_2  = (staticYBottom-(b2))/m2;
		        float y2_2 = staticYBottom;
		        
		        float xi = -(b1-b2)/(m1-m2);
		        float yi = (m1*xi)+b1;
		        
		        
		        
		        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
		        g2.setColor(Color.green);
		        
		        //g2.drawLine((int)x1_1, (int)staticYTop, (int)x1_2, (int)staticYBottom);
		        //g2.drawLine((int)x2_1, (int)staticYTop, (int)x2_2, (int)staticYBottom);
		        g2.drawLine((int)xi, (int)yi, (int)x1_2, (int)staticYBottom);
		        g2.drawLine((int)xi, (int)yi, (int)x2_2, (int)staticYBottom);
	        	
	        	
	        }
	        else{
	        	animationMode = false;
	        }
	        
	        g.setColor(Color.red);
	        g.setFont(new Font("TimesRoman", Font.BOLD, 15)); 
	        g.drawString("File Index At: "+fileIndex, 10, 240); //new Font(Font.MONOSPACED, Font.BOLD, 15)
	        repaint();
	 }
	
	
	
	/**
	 * Create the application.
	 */
	public LaneLineDataCreatorSlope() {
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
        
        points = new float[files.length][4];
        control = new Rectangle[files.length][4];
        rawFile = new File(realData);
        
        
        
        if(rawFile.exists()){
        	System.out.println("Exists");
        	Scanner scanner  = null;
        	try {
        		scanner = new Scanner(new FileReader(rawFile));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
        	
        	
        	for(int i = 0; i<points.length; i++){
            	points[i][0] = scanner.nextFloat()*(originalImageWidth*scaleFactor);
            	points[i][1] = scanner.nextFloat();
            	points[i][2] = scanner.nextFloat()*(originalImageWidth*scaleFactor);
            	points[i][3] = scanner.nextFloat();
            	
            	for(int j = 0; j<4; j++){
	           		 float scaledBox = (boxSize*scaleFactor);
	           		 float dispX = 0f;
	           		 float dispY = 0f;
	    
	           		 if(j == 0){
	           			 dispX = points[i][0] + (boxSize*scaleFactor);
	           			 dispY = ((originalImageHeight*scaleFactor)/2f) + scaledBox;
	           		 }
	           		 else if(j == 1){
	           			 dispX = points[i][0] - (boxSize*scaleFactor)*2f;
	           			 dispY = ((originalImageHeight*scaleFactor)/2f) - scaledBox*2f;
	           		 }
	           		 else if(j == 2){
	           			 dispX = points[i][0] - (boxSize*scaleFactor)*2f;
	           			 dispY = ((originalImageHeight*scaleFactor)/2f) + scaledBox;
	           		 }
	           		 else if(j == 3){
	           			 dispX = points[i][0] + (boxSize*scaleFactor);
	           			 dispY = ((originalImageHeight*scaleFactor)/2f) - scaledBox*2f; 
	           		 }
	           		 
	           		 control[i][j] = new Rectangle((int)dispX,(int)dispY,(int)scaledBox,(int)scaledBox);
           		 
           	 	}
        	}
        	scanner.close();
        }
        else{
        	
        	for(int i = 0; i<points.length; i++){
            	points[i][0] = (originalImageWidth*scaleFactor)/2f;
            	points[i][1] = 1f;
            	points[i][2] = (originalImageWidth*scaleFactor)/2f;
            	points[i][3] = -1f;
            	for(int j = 0; j<4; j++){
    	       		 float scaledBox = (boxSize*scaleFactor);
    	       		 float dispX = 0f;
    	       		 float dispY = 0f;
    	
    	       		 if(j == 0){
    	       			 dispX = points[i][0] + (boxSize*scaleFactor);
    	       			 dispY = ((originalImageHeight*scaleFactor)/2f) + scaledBox;
    	       		 }
    	       		 else if(j == 1){
    	       			 dispX = points[i][0] - (boxSize*scaleFactor)*2f;
    	       			 dispY = ((originalImageHeight*scaleFactor)/2f) - scaledBox*2f;
    	       		 }
    	       		 else if(j == 2){
    	       			 dispX = points[i][0] - (boxSize*scaleFactor)*2f;
    	       			 dispY = ((originalImageHeight*scaleFactor)/2f) + scaledBox;
    	       		 }
    	       		 else if(j == 3){
    	       			 dispX = points[i][0] + (boxSize*scaleFactor);
    	       			 dispY = ((originalImageHeight*scaleFactor)/2f) - scaledBox*2f; 
    	       		 }
    	       		 
    	       		 control[i][j] = new Rectangle((int)dispX,(int)dispY,(int)scaledBox,(int)scaledBox);
           		 
           	 	}
            	 
            	
            }
        	
        	
	        try {
				rawFile.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
        }
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

	public void saveLineData(){
		PrintWriter writer = null;
		try {
			writer = new PrintWriter(rawFile);
			for(int i = 0; i<files.length;i++){
				
				writer.println( scalePointXAsOutput(points[i][0])+" "+
								points[i][1]+" "+
								scalePointXAsOutput(points[i][2])+" "+
								points[i][3]);
			}
			
		} catch (FileNotFoundException e) {

			e.printStackTrace();
		}
		writer.close();
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
	public void mousePressed(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
		mouseDown = true;
		
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
		mouseDown = false;
		movingPoint = false;
		
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		// TODO Auto-generated method stub
		mouseX = e.getX();
		mouseY = e.getY();
		
		if(mouseDown) {
			//points[fileIndex][1] = oldSlope+((mouseX-oldMouseX)/1000f);
			
			if(movingPoint == false){
				for(int i =0;i<numberOfPoints;i++){
					if(control[fileIndex][i].contains(mouseX, mouseY) == true){
						movingPointIndex = i;
						break;
					}
				}
				
				oldMouseX = mouseX;
				if(movingPointIndex%2f != 0)
					oldSlope = points[fileIndex][(int)movingPointIndex];
				else
					oldPosition = points[fileIndex][(int)movingPointIndex];
					
				movingPoint = true;
			}
			else{
				if(movingPointIndex%2f != 0){
					//points[fileIndex][(int)movingPointIndex] = oldSlope+((mouseX-oldMouseX)/(Math.abs(100f-points[fileIndex][(int)movingPointIndex])));
					points[fileIndex][(int)movingPointIndex] = oldSlope + (mouseX-oldMouseX)/500f;

				}
				else{
					points[fileIndex][(int)movingPointIndex] = (mouseX-oldMouseX) + oldPosition;
				}
				
			}
		}
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
		
		if(e.getKeyCode() == KeyEvent.VK_Q){
			animationMode = true;
			animationFileIndex = 0f;
			
		}
		
		if(e.getKeyCode() == KeyEvent.VK_E){
			saveLineData();
			
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
        jFrame.getContentPane().add(new LaneLineDataCreatorSlope());
        jFrame.setVisible(true);
        
	}


}
