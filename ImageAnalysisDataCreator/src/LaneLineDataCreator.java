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
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Comparator;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.UIManager;

public class LaneLineDataCreator extends JPanel implements MouseMotionListener, MouseListener, KeyListener{
	 private boolean mouseDown = false;
	 private float mouseX = 0f;
	 private float mouseY = 0f;
	 private float oldMouseX = 0f;
	 private float oldMouseY = 0f;
	 private float oldPositionX = 0f;
	 private float oldPositionY = 0f;
	 private String imagesDataFolder = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/ImagesDataSet3";
	 private String realData = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/LaneDetectionData/RealData3/raw_data.txt";
	 private File[] files;
	 private int fileIndex = 0;
	 private float animationFileIndex = 0;
	 private float animationSpeed = 0.1f;
	 private Rectangle[][] savingPoints;
	 private Color[] pointsColor;
	 private String[] text;
	 private boolean movingPoint = true;
	 private int movingPointIndex= 0;
	 private int numberOfPoints = 4;
	 
	 private boolean animationMode = false;
	 private File rawFile;
	 private float scaleFactor = 4f;
	 private float originalImageWidth = 100f;
	 private float originalImageHeight = 56f;
	 private float boxSize = 10f;
	 private float lineWidth = 1f;
	 @Override
	 public void paintComponent(Graphics g) {
	        super.paintComponent(g);
	        
	        Rectangle[] drawPoints;

	        if(animationMode == false){
		        
	        	try {
	 				Image image = ImageIO.read(files[fileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}
	        	 
		        //if(savingPoints[fileIndex][0].y == 0 || savingPoints[fileIndex][1].y == 0 || savingPoints[fileIndex][2].y == 0 || savingPoints[fileIndex][3].y == 0){
		        if(savingPoints[fileIndex][0].x == 0){
	        		if(fileIndex>0){
			        	for(int i = 0; i<numberOfPoints;i++){
			        		savingPoints[fileIndex][i] = new Rectangle(savingPoints[fileIndex-1][i]);
			        	}
		        	}
		        }
		        
		        
		        drawPoints = savingPoints[fileIndex];
		        
		        for(int i = 0;i<numberOfPoints;i++){
		        	g.setColor(pointsColor[i]);
		        	g.drawRect(drawPoints[i].x,drawPoints[i].y,drawPoints[i].width,drawPoints[i].height);
		        	//g.drawString(text[i], drawPoints[i].x+(drawPoints[i].width/2), drawPoints[i].y+(drawPoints[i].height/2));
		        }
		        
		        Graphics2D g2 = (Graphics2D) g;
		        g2.setColor(Color.red);
		        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
		        g2.drawLine(drawPoints[0].x, drawPoints[0].y, drawPoints[1].x, drawPoints[1].y);
		        g2.drawLine(drawPoints[2].x, drawPoints[2].y, drawPoints[3].x, drawPoints[3].y);
	        }
	        else if(animationMode == true && (int)animationFileIndex < files.length - 1){
	        	try {
	 				Image image = ImageIO.read(files[(int)animationFileIndex]);
	 	        	g.drawImage(image, 0, 0, (int)(originalImageWidth*scaleFactor), (int)(originalImageHeight*scaleFactor), null, null);
	 	        } catch (IOException e) {
	 				e.printStackTrace();
	 			}
	        	
	        	animationFileIndex += animationSpeed;
	        	drawPoints = savingPoints[(int)animationFileIndex];
	        	Graphics2D g2 = (Graphics2D) g;
		        g2.setColor(Color.red);
		        g2.setStroke(new BasicStroke(lineWidth*scaleFactor));
		        g2.drawLine(drawPoints[0].x, drawPoints[0].y, drawPoints[1].x, drawPoints[1].y);
		        g2.drawLine(drawPoints[2].x, drawPoints[2].y, drawPoints[3].x, drawPoints[3].y);
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
	public LaneLineDataCreator() {
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

        pointsColor = new Color[numberOfPoints];
        text = new String[numberOfPoints];
        for(int i = 0; i<numberOfPoints;i++){
        	
        	if(i%2 == 0)
        		pointsColor[i] = Color.red;
        	else
        		pointsColor[i] = Color.green;
        	
        	if(i<numberOfPoints/2)
        		text[i] = "1";
        	else 
        		text[i] = "2";
        	
        }
        
        savingPoints = new Rectangle[files.length][numberOfPoints];
        for(int i = 0; i<files.length;i++){
        	for(int j = 0; j<numberOfPoints;j+=2){
        		int scaledBox = (int)(scaleFactor*boxSize);
            	savingPoints[i][j] = new Rectangle(j*scaledBox,scaledBox,scaledBox,scaledBox);
            	savingPoints[i][j+1] = new Rectangle(j*scaledBox,(int)(originalImageHeight*scaleFactor) - (int)scaledBox,scaledBox,scaledBox);
            }
        }
        
        rawFile = new File(realData);
        try {
			rawFile.createNewFile();
		} catch (IOException e) {
			e.printStackTrace();
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
	public float scalePointYAsOutput(float point){
		return point/(originalImageHeight*scaleFactor);
	}
	public void saveLineData(){
		PrintWriter writer = null;
		try {
			writer = new PrintWriter(rawFile);
			for(int i = 0; i<files.length;i++){
				
				/*writer.println( scalePointXAsOutput(savingPoints[i][0].x + savingPoints[i][0].width/2)+" "+scalePointYAsOutput(savingPoints[i][0].y + savingPoints[i][0].height/2)+" "+
								scalePointXAsOutput(savingPoints[i][1].x + savingPoints[i][1].width/2)+" "+scalePointYAsOutput(savingPoints[i][1].y + savingPoints[i][1].height/2)+" "+
								scalePointXAsOutput(savingPoints[i][2].x + savingPoints[i][2].width/2)+" "+scalePointYAsOutput(savingPoints[i][2].y + savingPoints[i][2].height/2)+" "+
								scalePointXAsOutput(savingPoints[i][3].x + savingPoints[i][3].width/2)+" "+scalePointYAsOutput(savingPoints[i][3].y + savingPoints[i][3].height/2));*/
				
				writer.println( scalePointXAsOutput(savingPoints[i][0].x)+" "+
								scalePointXAsOutput(savingPoints[i][1].x)+" "+
								scalePointXAsOutput(savingPoints[i][2].x)+" "+
								scalePointXAsOutput(savingPoints[i][3].x));
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
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		mouseDown = true;
		oldMouseX = mouseX;
		oldMouseY = mouseY;
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
		
		if(mouseDown) {
			if(movingPoint == false){
				for(int i =0;i<numberOfPoints;i++){
					if(savingPoints[fileIndex][i].contains(mouseX, mouseY) == true){
						movingPointIndex = i;
						oldPositionX = savingPoints[fileIndex][i].x;
						oldPositionY = savingPoints[fileIndex][i].y;
						break;
					}
				}
				movingPoint = true;
			}
			else{
				
				int scaledBox = (int)(boxSize*scaleFactor);
				int xPos = (int)(mouseX-oldMouseX) + (int)oldPositionX;
				
				int yPos = (int)(originalImageHeight*scaleFactor) - (int)scaledBox;
				if(movingPointIndex %2 == 0){
					yPos = scaledBox;
				}

				savingPoints[fileIndex][movingPointIndex].setLocation(xPos,yPos);
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
        jFrame.getContentPane().add(new LaneLineDataCreator());
        jFrame.setVisible(true);
        
	}


}
