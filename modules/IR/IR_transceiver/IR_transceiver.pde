/* Webmote - Tranceiver Code

Authors: Daniel Myers and Alex Wilson

Description:
This code runs on all transcievers belonging to the webmote system
and is intended to allow two way communication via xbee modules.

Modus Operandi:
Refer to the README file in the webmote directory.

Thanks to Ken Shirriff for the IRremote library.
http://www.arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
 * An IR LED must be connected to the output PWM pin 3.
*/

#include <EEPROM.h>
#include <IRremote.h>


#define recordWaitTime 3 //in minutes
#define MAXMSGLEN 100
#define RECV_PIN 11
#define BUTTON_PIN 8
#define STATUS_PIN 13

IRrecv irrecv(RECV_PIN);
IRsend irsend;

decode_results results;

bool DEBUG = 0;

char message[MAXMSGLEN];
char message2[MAXMSGLEN];
char inChar = -1;
int index = 0;
char commandType;
String data;
int messageDestination;
int transceiverID = 0;
String rawDataString;
unsigned int rawData[RAWBUF];
int rawDataBit0;
int rawDataBit1;
char* codeLenHEX;
int flag = 0;

// Storage for the recorded code
int codeType = 0; // The type of code
unsigned long codeValue; // The code value if not raw
unsigned int rawCodes[RAWBUF]; // The durations if raw
int codeLen; // The length of the code
int toggle = 0; // The RC5/6 toggle state

void setup() {
    Serial.begin(9600);
    // EEPROM.write(0, 0); // Flash messageDestination on EEPROM
    restoreID();
    irrecv.enableIRIn(); // Start the receiver
    pinMode(BUTTON_PIN, INPUT);
    pinMode(STATUS_PIN, OUTPUT);
}

void loop() {
    if (!transceiverID) {
        requestID();
    }
  
    if (Serial.available() > 2) {
        while (Serial.available()) {
            if (index < MAXMSGLEN - 1) {
                inChar = Serial.read();
                message[index++] = inChar;
                message[index] = '\0';
            }
            delay(5); //When set to 10, this delay causes the serial buffer to overflow and drop the final bits of the serial string. If this is set to 1, we don't get the last digit
        }
        if (String(message) == "reset") {
            EEPROM.write(0, 0);
            transceiverID = 0;
            Serial.println("Transceiver was reset.");
        } else {
            parseMessage(message);
            if (transceiverID == messageDestination & flag == 0) {
                switch (commandType) {
                    case 'p':
                        playCommand();
                        break;
                    case 'r':
                        recordCommand();
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
    delay(5000); //make sure we don't flood the server
    Serial.println("IR_ID_REQUEST");
}

void restoreID() {
    transceiverID = EEPROM.read(0);
    dPrint("Restored ID as: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
}

void parseMessage(String message) {
    // bit 0 - Transciever ID #
    messageDestination = atoi(&message[0]);
    // bit 1 - Command Type (r, p, d, a, etc.)
    commandType = char(message[1]);
    // DATA**
    data = message.substring(2);
    // bit 2 - Data Protocol (NEC, Raw, etc. represented as integer values)
    codeType = atoi(&(message.substring(2,3))[0]);
    // bit 3 and 4 - IR code length as a HEX number
    codeLen = strtol((&(message.substring(3,5))[0]), &codeLenHEX , 16);
    // bit 5 to end - IR Code
    
    //Serial.print(message);
    dPrint("\n");
    if (codeType == 0) {
      char messageData[codeLen];
            for (int i = 1; i <= (codeLen); i++) {
                rawDataBit1 = strtol((&(message.substring( (i-1)*2+5 , (i-1)*2+7 ))[0]), &codeLenHEX , 16);
                rawData[i] =  rawDataBit1;
            }
            dPrint("\n");
            
            
            for (int i = 1; i <= codeLen; i++) {
              if (i % 2) {
                  // Mark
                  rawCodes[i - 1] = rawData[i]*USECPERTICK - MARK_EXCESS;
                  dPrint(" m");
              } 
              else {
                  // Space
                  rawCodes[i - 1] = rawData[i]*USECPERTICK + MARK_EXCESS;
                  dPrint(" s");
              }
              dPrintDEC(rawCodes[i - 1]);
            }
            
            codeValue = 0;
        }
    else codeValue = atol(&message[5]);

    dPrint("\nParsed Message: \n");
    dPrint("\tDestination: ");
    dPrintDEC(messageDestination);
    dPrint("\n\tCommand Type: ");
    dPrintDEC(commandType);
    dPrint("\n\tIR Protocol: ");
    switch (codeType) {
        case 1:
            dPrint("NEC");
            break;
        case 2:
            dPrint("SONY");
            break;
        case 3:
            dPrint("RC5");
            break;
        case 4:
            dPrint("RC6");
            break;
        case 0:
            dPrint("RAW");
            break;
        default:
            dPrintDEC(codeType);
            break;
    }
    dPrint("\n\tIR Code Data: ");
    if (codeType == 0) {
      for (int i = 1; i <= codeLen; i++) {
        dPrintDEC(rawData[i]);
        dPrint(" ");
      }
    }
    else 
      dPrintLONG(codeValue);
    dPrint("\n\tIR Code Length: ");
    dPrintDEC(codeLen);
    dPrint("\n");
}

void playCommand() {
    dPrint("Play command with data: ");
    digitalWrite(STATUS_PIN, HIGH);
    //parseIRData(data);
    dPrintLONG(codeValue);
    dPrint("\n");

    sendCode(0, codeValue);
    delay(100);
    Serial.flush();

    digitalWrite(STATUS_PIN, LOW);
}

void recordCommand() {
    dPrint("Record command\n");
    digitalWrite(STATUS_PIN, HIGH);
    irrecv.enableIRIn();
    // Eventually should add a timeout here
    while (!irrecv.decode(&results)) {}
    storeCode(&results);
    
    if(codeType == UNKNOWN) {
        String dataStringHold;
        dPrint("\nRaw Code HEX data:\n");
        Serial.print(String(transceiverID) + String("p") + "0" + String(codeLen,HEX));
        for (int i = 1; i <= codeLen; i++) {
                dataStringHold = String(char((&results)->rawbuf[i]));
                if( int((&results)->rawbuf[i]) < 16 ) {Serial.print("0");}
                Serial.print(( ((&results)->rawbuf[i]) ), HEX);
        }
        Serial.print("\n");
    }
    
    irrecv.resume();
    dPrint("\nSent to server: ");
    if(codeType != UNKNOWN)
        Serial.println(String(transceiverID) + String("p") + String(codeType) + String(codeLen,HEX) + String(codeValue));
    digitalWrite(STATUS_PIN, LOW);
}

void assignID() {
    digitalWrite(STATUS_PIN, HIGH);
    EEPROM.write(0, atoi(&data[0]));
    transceiverID = atoi(&data[0]);
    dPrint("Assigned ID to transceiver: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
    digitalWrite(STATUS_PIN, LOW);
}

void dPrint(String str) {
    if (DEBUG) {
        Serial.print(str);
    }
}

void dPrintBYTE(byte in) {
    if (DEBUG) {
        Serial.print(in, HEX);
    }
}

void dPrintHEX(unsigned long in) {
    if (DEBUG) {
        Serial.print(in, HEX);
    }
}

void dPrintDEC(unsigned int in) {
    if (DEBUG) {
        Serial.print(in, DEC);
    }
}

void dPrintLONG(unsigned long in) {
    if (DEBUG) {
        Serial.print(in, DEC);
    }
}

// This extracts the IR protocol, IR signal data, and other information from the message data
void parseIRData(String data) {
    codeType = data[0];
    codeLen = 32;
    //codeValue = data.substring(1);

    dPrint("\nParsed IR Data: \n");
    dPrint("\tCode Type: ");
    dPrintDEC(codeType);
    dPrint("\n\tCode Length: ");
    dPrintDEC(codeLen);
    dPrint("\n\tIR Data: ");
    dPrint(data);
    dPrint("\n");
}

// Stores the code for later playback
// Most of this code is just logging
void storeCode(decode_results *results) {
    codeType = results->decode_type;
    codeType = UNKNOWN;
    int count = results->rawlen;
    //codeType = UNKNOWN;
    if (codeType == UNKNOWN) {
        dPrint("Received unknown code, saving as raw\n");
        codeLen = results->rawlen - 1;
        // To store raw codes:
        // Drop first value (gap)
        // Convert from ticks to microseconds
        // Tweak marks shorter, and spaces longer to cancel out IR receiver distortion
        for (int i = 1; i <= codeLen; i++) {
            if (i % 2) {
                // Mark
                rawCodes[i - 1] = results->rawbuf[i]*USECPERTICK - MARK_EXCESS;
                dPrint(" m");
            } 
            else {
                // Space
                rawCodes[i - 1] = results->rawbuf[i]*USECPERTICK + MARK_EXCESS;
                dPrint(" s");
            }
            dPrintDEC(rawCodes[i - 1]);
        }
        dPrint("\n");
    }
    else {
        if (codeType == NEC) {
            dPrint("Received NEC: ");
            if (results->value == REPEAT) {
                // Don't record a NEC repeat value as that's useless.
                dPrint("repeat; ignoring.");
            return;
        }
    } 
    else if (codeType == SONY) {
        dPrint("Received SONY: ");
    } 
    else if (codeType == RC5) {
        dPrint("Received RC5: ");
    } 
    else if (codeType == RC6) {
        dPrint("Received RC6: ");
    } 
    else {
        dPrint("Unexpected codeType ");
        dPrintDEC(codeType);
    dPrint(" ");
    }
    dPrintLONG(results->value);
    dPrint("\n");
    codeValue = results->value;
    codeLen = results->bits;
  }
}

void sendCode(int repeat, long int new_code) {
    codeValue = new_code;
    if (codeType == NEC) {
        if (repeat) {
            irsend.sendNEC(REPEAT, codeLen);
            dPrint("Sent NEC repeat");
        } 
        else {
            irsend.sendNEC(codeValue, codeLen);
            dPrint("Sent NEC ");
            dPrintHEX(codeValue);
            dPrint("\n");
        }
    }
    else if (codeType == SONY) {
        irsend.sendSony(codeValue, codeLen);
        dPrint("Sent Sony ");
        dPrintHEX(codeValue);
        dPrint("\n");
    } 
    else if (codeType == RC5 || codeType == RC6) {
        if (!repeat) {
            // Flip the toggle bit for a new button press
            toggle = 1 - toggle;
        }
        // Put the toggle bit into the code to send
        codeValue = codeValue & ~(1 << (codeLen - 1));
        codeValue = codeValue | (toggle << (codeLen - 1));
        if (codeType == RC5) {
            irsend.sendRC5(codeValue, codeLen);
            dPrint("Sent RC5 ");
            dPrintHEX(codeValue);
            dPrint("\n");
        } 
        else {
            irsend.sendRC6(codeValue, codeLen);
            dPrint("Sent RC6 ");
            dPrintHEX(codeValue);
            dPrint("\n");
        }
    }
    else if (codeType == 0 /* i.e. raw */) {
        // Assume 38 KHz
        irsend.sendRaw(rawCodes, codeLen, 38);
        dPrint("Sent raw\n");
    }
}
