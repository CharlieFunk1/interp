#include <WebSocketsServer.h>
#include <Adafruit_NeoPixel.h>

#define PIN 13

const char* ssid     = "Omicron Percei8";
const char* password = "pooptaco";
const int pinLed0 = 14; 

//Address local_IP(192, 168, 0, 250);
// Set your Gateway IP address
//Address gateway(192, 168, 0, 1);
//IPAddress subnet(255, 255, 0, 0);

Adafruit_NeoPixel strip = Adafruit_NeoPixel(106, PIN, NEO_GRB + NEO_KHZ800);

WebSocketsServer webSocket = WebSocketsServer(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t lenght) {
    //Serial.printf("[%u] get Message: %s\r\n", num, payload);
    //Serial.printf("DEBUG BEDUF BGUED DEBUG");
    switch(type) {
        case WStype_DISCONNECTED: 
            strip.show();
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
               String _payload = String((char *) &payload[0]);
               //Serial.println(_payload);
              
               String led_red = (_payload.substring(0,3));
               String led_green = (_payload.substring(_payload.indexOf(":")+3));
               String led_blue = (_payload.substring(_payload.indexOf(";")+3));
               String led_number = (_payload.substring(_payload.indexOf(".")+1));
               int ledR = led_red.toInt();
               int ledG = led_green.toInt();
               int ledB = led_blue.toInt();
               int ledN = led_number.toInt();
               //Serial.println("\e[31mGO\e[0m");
               updateLed (ledR,ledG,ledB,ledN);
              
            }   
            break;     
             
        case WStype_BIN:
            {
              hexdump(payload, lenght);
            }
            // echo data back to browser
            webSocket.sendBIN(num, payload, lenght);
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

  strip.begin();
  strip.show();
}

void loop() {
  webSocket.loop();
}

void updateLed(int ledR, int ledG, int ledB, int led_number){
  strip.setPixelColor(led_number, strip.Color(ledR, ledG, ledB));
  strip.show();
  
}
