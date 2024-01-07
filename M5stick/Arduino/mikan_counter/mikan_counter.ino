#include <M5StickC.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <ssl_client.h>
#include <WiFiClientSecure.h>
#include <ArduinoOSCWiFi.h>

const char* ssid = "tower";
const char* passwd = "chiho123";

HardwareSerial serial_ext(2);

static const int RX_BUF_SIZE = 20000;
static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };
unsigned long nextUpdate = 0;
unsigned long sum=0;
unsigned long count=0;
float avg = 0.0;
uint8_t person[1];
char buf[16];

char ipaddr[] = "192.168.7.7";
int port = 3333; 
void setup() {
  M5.begin();
  M5.Lcd.setRotation(3);
  M5.Lcd.setCursor(0, 30, 4);
  M5.Lcd.println("m5stick_uart_wifi_converter");
  setup_wifi();
  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
}

void loop() {
  M5.update();

  if (serial_ext.available()) {
    uint8_t rx_buffer[3];
    int rx_size = serial_ext.readBytes(rx_buffer, 3);
    if (rx_size == 3) {   //packet receive of packet_begin
      if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {

        serial_ext.readBytes(person,1);
        sum += person[0];
        count += 1;
      }
    }
  }
  // send once a minute
  if ( nextUpdate < millis() ) {
    avg = float(sum) / count;
    if(count==0) {
      avg = -1;
    }
    Serial.print("sum: ");
    Serial.println(sum);
    Serial.print("count: ");
    Serial.println(count);
    Serial.print("avg: ");
    Serial.println(avg);
    sprintf(buf,"%.2f",avg);
    Serial.print("stravg: ");
    Serial.println(buf);

    Serial.println("");
    OscWiFi.send(ipaddr, port, buf);

    sum = 0;
    count = 0;
    nextUpdate = millis() + 1000;
  }
}

void setup_wifi() {
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
