#include <WebSocketsServer.h>
#include <Adafruit_NeoPixel.h>
#include <iostream>
using namespace std;

#define PIN 14
#define NUM_PIXELS 106

const char* ssid     = "op8ext";
const char* password = "pooptaco";
const int pinLed0 = 13; 

//Address local_IP(192, 168, 0, 250);
// Set your Gateway IP address
//Address gateway(192, 168, 0, 1);
//IPAddress subnet(255, 255, 0, 0);

Adafruit_NeoPixel ledstrip = Adafruit_NeoPixel(106, PIN, NEO_GRB + NEO_KHZ800);

WebSocketsServer webSocket = WebSocketsServer(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t lenght) {
    //Serial.printf("[%u] get Message: %s\r\n", num, payload);
    //Serial.printf("DEBUG BEDUF BGUED DEBUG");
    switch(type) {
        case WStype_DISCONNECTED:
              { 
               for (int i = 0; i < NUM_PIXELS; i++) {
                   ledstrip.setPixelColor(i, 0, 0, 0);
               }
               ledstrip.show();
              }
            break;
              
        case WStype_CONNECTED: 
            {
              IPAddress ip = webSocket.remoteIP(num);
              Serial.printf("[%u] Connected from %d.%d.%d.%d url: %s\r\n", num, ip[0], ip[1], ip[2], ip[3], payload);    
            }
            break;
        
        case WStype_TEXT:
            {
               //Serial.printf("[%u] get Text: %s\r\n", num, &payload);
               
              
            }   
            break;     
             
        case WStype_BIN:
            {
              //hexdump(payload, lenght);
              int k=0;
              int strip[NUM_PIXELS][3];

              
              for (int i = 0; i < NUM_PIXELS; i++) {
                for (int j = 0; j < 3; j++) {
                  
                  strip[i][j] = payload[k];
                  //Serial.println(k);
                  k++;
                }
              //Serial.println("JLOOP");  
            }
            //FOR TESTING OUTPUT.  DISPLAYS STRIP.
            //for (int i = 0; i < NUM_PIXELS; i++) {
            //  for (int j = 0; j < 3; j++) {
            //    Serial.println(strip[i][j]);
            //    
            //}
            //Serial.println("LED");
            //}  
            //Serial.println("STRIP");
            //FOR TESTING OUTPUT.  DISPLAYS STRIP.
            
            for (int l = 0; l < (NUM_PIXELS -1); l++) {
              ledstrip.setPixelColor(l, strip[l][0], strip[l][1], strip[l][2]);
            }
            ledstrip.show();
            }
            break;
            
    }
    
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(pinLed0, OUTPUT); 
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED) {
     Serial.print(".");
     delay(200);
  }
    
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);  
   
  Serial.println("Start Websocket Server");
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  ledstrip.begin();
  ledstrip.show();
}

void loop() {
  webSocket.loop();
}

//void updateLed(strip){
 // for (int i = 0; i < NUM_PIXELS; i++) {
 // strip.setPixelColor(i, strip.Color(strip[i][0], strip[i][1], strip[i][2]));
 // }
 // strip.show();
  
//}
