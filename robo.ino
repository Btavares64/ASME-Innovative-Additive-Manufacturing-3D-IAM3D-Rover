#include <Servo.h>

Servo servoX;  // x axis arm movement
Servo servoY ;  // y axis movement

int posX = 0;
int posY = 0;

void setup() 
{
  Serial.begin(9600);

  // ########### FOR ARM ########################################
  // this is the x position servo 
  servoX.attach(9);  // for pin 9
  servoX.write(0);   // start sero at degree 0
  
  // this is the y position servo
  servoY.attach(10);
  servoY.write(0); 
}

void loop() 
{
  if (Serial.available() > 0) 
  {
    // input in order to move the servo
    char input = Serial.read();

    // ##### AAAARRRRMMMMM #############
    // ##### MOVEMENTS FOR X POSITION ARM MOVE #############
    if (input == 'j')
    {
      posX += 10; 

      if (posX > 180)
      {
        posX = 180;
      } 
      servoX.write(posX);        
    }
    else if (input == 'l')
    {
      posX -= 10;
      // create limitation
      if (posX < 0)
      {
        posX = 0;
      }
      servoX.write(posX);                                                  
    }
    // ##### MOVEMENTS FOR Y POSITION ARM MOVEMENT #############
    if (input == 'i')
    {
      posY += 10; 

      if (posY > 180)
      {
        posY = 180;
      } 
      servoY.write(posY);        
    }
    else if (input == 'k')
    {
      posY -= 10;
      // create limitation
      if (posY < 0)
      {
        posY = 0;
      }
      servoY.write(posY);                                                  
    }
    
    delay(10);
  }
}

/*
some notes to conside while programming the functions for the rover:

- To control the direction of the rover
* w = forward
* a = left
* s = back
* d = right

- to move the robotic arm
* i = arm up
* j = move arm to left 
* k = arm down
* l = move arm to right

- to clamp object
* g = grab


Some hardware needed to control the rover:
- HC-05 wireless reciever bluetooth 
- https://www.amazon.com/Wireless-Bluetooth-Receiver-Transceiver-Transmitter/dp/B01MQKX7VP/ref=asc_df_B01MQKX7VP?tag=bingshoppinga-20&linkCode=df0&hvadid=79920803409643&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=82352&hvtargid=pla-4583520395163557&psc=1
- FPV reciever and camera to send analog input to the laptop that will view the feed

*/
