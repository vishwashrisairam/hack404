# hack404 - FireAcc

## About FireAcc
FireAcc is a casualty detection(casualties like road accidents,fire breakout,etc) and notification hack aimed at improving the notification delivery to the concerned authorities(ambulance,fire brigade,police station,etc) by providing instantaneous notification on occurence of any casualty.
  
##Team members
- V Vishwashri Sairam
- Patel Darshit
- Harsh Jadav
  
## Technologies and Apis Used
- OpenCv library of Java
- Flask
- Clarifai api
- Twillio api
- Heroku 
  
![Alt text](/relative/path/to/img.jpg?raw=true "Optional Title")

## Description 
- The hack assumes cctv or other surveillance cameras for detecting the casualty . So we used **OpenCV** libraries available for **Java** to simulate
the activity of cctv camera. It converts the webcam of laptop as a camera continuously capturing images after a particular timeframe and 
sending the images to the server.
- The server is developed using  **Flask**. The image received is sent for processing using the api of **Clarifai** which  processes the 
image and extracts features and tags relevant to the picture.
- The tags and features returned by the api are compared with the pretrained data(tags) for selecting whom to notify . Some cases are:
    * road accidents :- ambulance and police should be notified
    * fire breakout :- fire brigade and ambulance should be notified
- A log of all the data is maintained by a **MongoDb** database which can also be used for future analysis.
- Notification  to the concerned authority is done through **Twillio** api which includes the time and loaction of the causualty and it is done immediately after detection of casualty. (within one minute they are notified)
- A web dashboard for displaying the logs is also designed .
- The hack is deployed on **Heroku**. Link:- http://fireacc.herokuapp.com
