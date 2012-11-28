#include <EEPROM.h>
#include <x10.h>
#include <stdarg.h>

#define ZERO_CROSS_PIN 12
#define DATA_TX_PIN 13
#define DATA_RX_PIN 1
#define MAXMSGLEN 255
#define BUTTON_PIN 6

char message[MAXMSGLEN];
char commandType;
int transceiverID = 0;
int index = 0;
char inChar = -1;
int messageDestination;
bool DEBUG = 0;

void printfEmu(char *fmt, ... ) {
    char tmp[128]; // resulting string limited to 128 chars
    va_list args;
    va_start (args, fmt );
    vsnprintf(tmp, 128, fmt, args);
    va_end (args);
    Serial.print(tmp);
}

void dPrint(String str) {
    if (DEBUG) Serial.print(str);
}

void dPrintBYTE(byte in) {
    if (DEBUG) Serial.print(in, HEX);
}

void dPrintHEX(unsigned long in) {
    if (DEBUG) Serial.print(in, HEX);
}

void dPrintDEC(unsigned int in) {
    if (DEBUG) Serial.print(in, DEC);
}

void dPrintLONG(unsigned long in) {
    if (DEBUG) Serial.print(in, DEC);
}

void printX10Info() {
//    dPrint("\nUnit Code is: ");
//    dPrintDEC(unitCode);
//    dPrint("\nHouse Code is: ");
//    dPrintDEC(houseCode);
//    dPrint("\nCommand Code is: ");
//    dPrintDEC(commandCode);
}

void setup() {
    Serial.begin(9600);
    restoreID();
    pinMode(BUTTON_PIN, INPUT);
    x10.begin(DATA_RX_PIN, DATA_TX_PIN, ZERO_CROSS_PIN);
}

void loop() {
    if (!transceiverID) {
        requestID();
    }
  
    if (Serial.available() > 3) {
        while (Serial.available()) {
            if (index < MAXMSGLEN - 1) {
                inChar = Serial.read();
                message[index++] = inChar;
                message[index] = '\0';
            }
            delay(5); 
        }
        if (String(message) == "reset_X10") {
            EEPROM.write(0, 0);
            transceiverID = 0;
            Serial.println("Transceiver was reset.");
        } else {
            parseMessage();
            if (transceiverID == messageDestination) {
                switch (commandType) {
                    case 'p':
                        playCommand();
                        break;
                    case 's':
                        getState();
                        break;
                    case 'a':
                        assignID();
                        break;
                    case 'd':
                        DEBUG = !DEBUG;
                        dPrint("Turned Debug On\n");
                        break;
                    default:
                        dPrint("Unrecognized Command");
                        break;
                }
            }
        }
        index = 0;
    }
}

void requestID() {
    delay(5000);
    Serial.println("X10_ID_REQUEST");
}

void restoreID() {
    transceiverID = EEPROM.read(0);
    dPrint("Restored ID as: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
}

void parseMessage() {
    // AAAA - Transciever ID #
    // BB - Command Type (p, s, a, d)
    int temp;
    sscanf(message, "%4x%2X", &messageDestination, &temp);
    commandType = char(temp);
}

void assignID() {
//    digitalWrite(STATUS_PIN, HIGH);
    sscanf(&message[6], "%4x", &transceiverID);
    EEPROM.write(0, transceiverID);
//    digitalWrite(STATUS_PIN, LOW);

    dPrint("Assigned ID to transceiver: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
}

void playCommand() {
    printX10Info();
    char house, unit, command;
    int tmp1, tmp2, tmp3;
    sscanf(&message[6], "%2X%2X%2X", &tmp1, &tmp2, &tmp3);
    house = char(tmp1);
    unit = char(tmp2);
    command = char(tmp3);
    x10.beginTransmission(house);
    x10.write(unit);
    x10.write(command);
    x10.endTransmission();
}

void getState() {
    dPrint("Not Implemented\n");
}
