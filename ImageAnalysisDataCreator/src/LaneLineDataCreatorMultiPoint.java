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

public class LaneLineDataCreatorMultiPoint extends JPanel implements MouseMotionListener, MouseListener, KeyListener{
	 private boolean mouseDown = false;
	 private float mouseX = 0f;
	 private float mouseY = 0f;
	 private float oldMouseX = 0f;
	 private float oldMouseY = 0f;
	 private float oldPositionX = 0f;
	 private float oldPositionY = 0f;
	 
	 private String imagesDataFolder = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/ImagesDataSet8";
	 private String realData = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/RealData8/raw_data.txt";
	 //private String realData = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/output_8.txt";
	 
	 private File[] files;
	 private int fileIndex = 0;
	 private float animationFileIndex = 0;
	 private float animationSpeed = 0.05f;
	 
	 Rectangle[][] points;
	 
	 private boolean animationMode = false;
	 private File rawFile;
	 private float scaleFactor = 4f;
	 private float originalImageWidth = 100f;
	 private float originalImageHeight = 56f;
	 private float boxSize = 10f;
	 private float lineWidth = 1f;
	 
	 private boolean movingPoint = true;
	 private int movingPointIndex= 0;
	 private int numberOfPoints = 8;
	 
	 @Override
	 public void paintComponent(Graphics g) {
	        super.paintComponent(g);
	        Rectangle[] drawRect;
	        
	        Graphics2D g2 = (Graphics2D) g;
	        
	        if(animationMode == false){
	        	try {
	 				Image image = ImageIO.read(files[fileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}

	        	
	        	if(points[fileIndex][0].x == 0){
	        		if(fileIndex>0){
			        	for(int i = 0; i<numberOfPoints;i++){
			        		points[fileIndex][i] = new Rectangle(points[fileIndex-1][i]);
			        	}
		        	}
		        }
	        	
	        	
	        	drawRect = points[fileIndex];
	        	g.setColor(Color.red);
	        	
	        	for(int i = 0; i<drawRect.length;i++){
	        		g.drawRect(drawRect[i].x, drawRect[i].y, drawRect[i].width, drawRect[i].height);
	        	}

		        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
		        g2.setColor(Color.red);
		        
	        	for(int i = 1; i<4;i++){
	        		g2.drawLine(drawRect[i].x,drawRect[i].y,drawRect[i-1].x,drawRect[i-1].y);
	        	}
	        	
	        	g2.setColor(Color.red);
	        	for(int i = 5; i<8;i++){
	        		g2.drawLine(drawRect[i].x,drawRect[i].y,drawRect[i-1].x,drawRect[i-1].y);
	        	}
	        }
	        else if(animationMode == true && (int)animationFileIndex < files.length - 1){
	        	try {
	 				Image image = ImageIO.read(files[(int)animationFileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}
	        	
	        	drawRect = points[(int)animationFileIndex];
	        	g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
			    g2.setColor(Color.green);  
		        
	        	for(int i = 1; i<4;i++){
	        		g2.drawLine(drawRect[i].x,drawRect[i].y,drawRect[i-1].x,drawRect[i-1].y);
	        	}
	        	
	        	g2.setColor(Color.green);
	        	for(int i = 5; i<8;i++){
	        		g2.drawLine(drawRect[i].x,drawRect[i].y,drawRect[i-1].x,drawRect[i-1].y);
	        	}
	        	
	        	animationFileIndex += animationSpeed;
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
	public LaneLineDataCreatorMultiPoint() {
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
        
      
        rawFile = new File(realData);
        points = new Rectangle[files.length][8];
        float scaledYOffset = (originalImageHeight*scaleFactor)/4f;
        float boxScaled = boxSize*scaleFactor;
        
        if(rawFile.exists() && rawFile.length()>0){
        	System.out.println("Exists");
        	Scanner scanner = null;
        	try {
				scanner = new Scanner(new FileReader(rawFile));
				for(int i = 0;i<points.length; i++){
		        	float y = 0;
		        	float x = 0;
		        	for(int j = 0; j<4; j++){
		        		y++;
		        		x = scanner.nextFloat()*originalImageWidth*scaleFactor;
		        		points[i][j] = new Rectangle((int)x,(int)(y*scaledYOffset)-(int)boxScaled,(int)boxScaled,(int)boxScaled);
		            }
		        	
		        	y = 0;
		        	for(int j = 4 ; j<8; j++){
		        		y++;
		        		x = scanner.nextFloat()*originalImageWidth*scaleFactor;
		        		points[i][j] = new Rectangle((int)x,(int)(y*scaledYOffset)-(int)boxScaled,(int)boxScaled,(int)boxScaled);
		            }
		        }
			} catch (FileNotFoundException e) {
				
				e.printStackTrace();
			}
        	scanner.close();
        }
        else{
        	
        	
	        try {
				rawFile.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
	        
	        
	        for(int i = 0;i<points.length; i++){
	        	float y = 0;
	        	for(int j = 0; j<4; j++){
	        		y++;
	        		
	        		points[i][j] = new Rectangle(0,(int)(y*scaledYOffset)-(int)boxScaled,(int)boxScaled,(int)boxScaled);
	            }
	        	
	        	y = 0;
	        	for(int j = 4 ; j<8; j++){
	        		y++;
	        		points[i][j] = new Rectangle((int)boxScaled,(int)(y*scaledYOffset)-(int)boxScaled,(int)boxScaled,(int)boxScaled);
	            }
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
        	File fileReplace = new File(imagesDataFolder+"/"+name+".png");
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
				writer.println( scalePointXAsOutput(points[i][0].x)+" "+
								scalePointXAsOutput(points[i][1].x)+" "+
								scalePointXAsOutput(points[i][2].x)+" "+
								scalePointXAsOutput(points[i][3].x)+" "+
								scalePointXAsOutput(points[i][4].x)+" "+
								scalePointXAsOutput(points[i][5].x)+" "+
								scalePointXAsOutput(points[i][6].x)+" "+
								scalePointXAsOutput(points[i][7].x));
				
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
		oldMouseX = mouseX;
		oldMouseY = mouseY;
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
			if(movingPoint == false){
				for(int i =0;i<numberOfPoints;i++){
					if(points[fileIndex][i].contains(mouseX, mouseY) == true){
						movingPointIndex = i;
						oldPositionX = points[fileIndex][i].x;
						oldPositionY = points[fileIndex][i].y;
						break;
					}
				}
				movingPoint = true;
			}
			else{
				int xPos = (int)(mouseX-oldMouseX) + (int)oldPositionX;
				points[fileIndex][movingPointIndex].x = xPos;
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
		
		if(e.getKeyCode() == KeyEvent.VK_Z){
			if(fileIndex>0){
	        	for(int i = 0; i<numberOfPoints;i++){
	        		points[fileIndex][i] = new Rectangle(points[fileIndex-1][i]);
	        	}
        	}
		}
		
		if(e.getKeyCode() == KeyEvent.VK_C){
			if(fileIndex<points.length-1){
				for(int i = 0; i<numberOfPoints;i++){
	        		points[fileIndex][i] = new Rectangle(points[fileIndex+1][i]);
	        	}
        	}
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
        jFrame.getContentPane().add(new LaneLineDataCreatorMultiPoint());
        jFrame.setVisible(true);
        
	}


}
