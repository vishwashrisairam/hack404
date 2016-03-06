/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package webcamcapture;


import java.io.BufferedReader;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.opencv.core.*;
import org.opencv.highgui.Highgui;
import org.opencv.highgui.VideoCapture;    


import java.io.File;
import java.io.IOException; 
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.Inet4Address;

import org.apache.http.HttpEntity; 
import org.apache.http.HttpResponse; 
import org.apache.http.HttpVersion;
import org.apache.http.client.ClientProtocolException; 
import org.apache.http.client.HttpClient; 
import org.apache.http.client.methods.HttpPost; 
import org.apache.http.entity.mime.MultipartEntity; 
import org.apache.http.entity.mime.content.ContentBody;
import org.apache.http.entity.mime.content.FileBody; 
import org.apache.http.entity.mime.content.StringBody; 
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient; 
import org.apache.http.params.CoreProtocolPNames;
import org.apache.http.util.EntityUtils; 
        
/**
 *
 * @author darshit
 */


public class WebCamCapture {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        // TODO code application logic here
       
    	System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
       
      httpRequestSend request = new httpRequestSend();
       VideoCapture camera = new VideoCapture(0);
    	int x=0;
    	if(!camera.isOpened()){
    		System.out.println("Error");
    	}
    	else {
    		Mat frame = new Mat();
    	    while(true){
    	    	if (camera.read(frame)){
    	    		System.out.println("Frame Obtained");
    	    		System.out.println("Captured Frame Width " + 
    	    		frame.width() + " Height " + frame.height());
    	    		Highgui.imwrite("camera"+x+".jpg", frame);
    	    		//System.out.println("OK");
                       // break;
                        
                        request.request("https://fireacc.herokuapp.com/dash", "camera"+x+".jpg");
                        x++;
    	    	}
            try {
                //}
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                System.out.println("stuck");
            }
            }
    	}
    	camera.release();
    
    }
} 
class httpRequestSend{
    void request(String url,String file_name) throws IOException{
        try {
            HttpClient httpclient = new DefaultHttpClient();
            httpclient.getParams().setParameter(CoreProtocolPNames.PROTOCOL_VERSION, HttpVersion.HTTP_1_1);

            HttpPost httppost = new HttpPost(url);
            
            
            String file_path = "C:/Users/darshit/Documents/NetBeansProjects/WebCamCapture/"+file_name;
            File fileToUse = new File(file_path);
            FileBody data = new FileBody(fileToUse,"image/jpeg");
           
           
            System.out.println(Inet4Address.getLocalHost().getHostAddress());
            /*MultipartEntity mpEntity = new MultipartEntity();
            ContentBody cbFile = new FileBody(fileToUse, "image/jpeg");
            mpEntity.addPart("userfile", cbFile);*/


   // httppost.setEntity(mpEntity);
            //String file_type = "JPG" ;
            
            MultipartEntity reqEntity = new MultipartEntity();
             ContentBody cbFile = new FileBody(fileToUse, "image/jpeg");
            reqEntity.addPart("file", data);
           
            //reqEntity.addPart("file", cbFile);
            
            httppost.setEntity(reqEntity); 
            //httppost.setEntity(mpEntity); 
             System.out.println("executing request " + httppost.getRequestLine());
            HttpResponse response = httpclient.execute(httppost);
            HttpEntity entity = response.getEntity();
            InputStreamReader is;
           
            StringBuffer sb = new StringBuffer();
            System.out.println("finalResult " + sb.toString());
            //String line=null;
            /*while((reader.readLine())!=null){
                sb.append(line + "\n");
            }*/
            
            //StringBuilder sb = new StringBuilder();
            try {
                    BufferedReader reader = 
           new BufferedReader(new InputStreamReader(entity.getContent()));
            String line = null;

            while ((line = reader.readLine()) != null) {
                sb.append(line);
        }
            }           
            catch (IOException e) { e.printStackTrace(); }
            catch (Exception e) { e.printStackTrace(); }
            
            String result=sb.toString();
            System.out.println("finalResult " + sb.toString());
           // System.out.println( response ); 
           // String responseString = new BasicResponseHandler().handleResponse(response);
            //System.out.println();
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(httpRequestSend.class.getName()).log(Level.SEVERE, null, ex);
            System.out.printf("dsf\n");
        }
    }  
    
    
}

