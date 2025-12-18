// ################## GITHUB NOTICE ################################
- IGNORE THIS CODE, IM CONCERNED ABOUT THE NOTES AT THE BOTTOM
#define DEVICE_ON 3

// GOBAL VARIABLES
int brightness = 0;

void setup() 
{
  //intialize serial communication
  Serial.begin(9600);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(DEVICE_ON, OUTPUT);
}

void loop() 
{
  // limit brightness should be 255
  int limit = 255;
  int fade = 5;
  analogWrite(DEVICE_ON, brightness);

  brightness += fade;  // increment the brightness by 5 

  if (brightness == limit)
  {
    brightness = 0;
  }

  delay(100);
}


/*
some notes to conside while programming the functions for the rover:

- To control the direction of the rover
* w = forward
* a = left
* s = back
* d = right

- to move the robotic arm
* "up arrow" = arm up
* "left arrow" = move arm to left 
* "down arrow" = arm down
* "right arrow" = move arm to right

- to clamp object
* g = grab


Some hardware needed to control the rover:
- HC-05 wireless reciever bluetooth 
- https://www.amazon.com/Wireless-Bluetooth-Receiver-Transceiver-Transmitter/dp/B01MQKX7VP/ref=asc_df_B01MQKX7VP?tag=bingshoppinga-20&linkCode=df0&hvadid=79920803409643&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=82352&hvtargid=pla-4583520395163557&psc=1
- FPV reciever and camera to send analog input to the laptop that will view the feed

*/