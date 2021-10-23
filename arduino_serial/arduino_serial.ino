// Example 5 - Receive with start- and end-markers combined with parsing
#include <Adafruit_NeoPixel.h>
#define PIN 3  //arduino pin that led strips data cable is connected to
#define NUM_PIXELS 106  // number of pixels in strip

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
char messageFromPC[numChars] = {0};
int integerFromPC = 0;
float floatFromPC = 0.0;

boolean newData = false;

int arr[3];

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

//============

void setup() {
    Serial.begin(115200);
    //Serial.println("This demo expects 3 pieces of data - text, an integer and a floating point value");
    //Serial.println("Enter data in this style <255, 255, 255>  ");
    //Serial.println();
    strip.begin();
    strip.show();
}

//============

void loop() {
  //Serial.println("test");
  
  char ser = Serial.read();
  if (ser == '!') {
    for (int i=0; i<NUM_PIXELS; i++)  {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        showPixel(i, arr[0], arr[1], arr[2]);
        newData = false;
        strip.show();
    }
  }
        //strip.show();
  }       
}
//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    arr[0] = atoi(strtokIndx); // copy it to messageFromPC
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    arr[1] = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    arr[2] = atoi(strtokIndx);     // convert this part to a float

}

//============

void showPixel(int i, int red, int green, int blue) {
    strip.setPixelColor(i, strip.Color(red, green, blue));
}
