#include <EEPROM.h>
#include <IRremote.h>
#include <stdarg.h>

#define MAXMSGLEN 256
#define RECV_PIN 11
#define IR_PIN 3
#define BUTTON_PIN 8
#define STATUS_PIN 13

#define PANASONICADDRESS 0x4004

decode_results results;
// Storage for the recorded code
int codeType = -1; // The type of code
unsigned long codeValue; // The code value if not raw
/*unsigned int rawCodes[RAWBUF]; // The durations if raw*/
unsigned int rawCodes[200]; // The durations if raw
int codeLen; // The length of the code
int toggle = 0; // The RC5/6 toggle state
IRrecv irrecv(RECV_PIN);
IRsend irsend;

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

void printIRInfo() {
    dPrint("\nCode type is: ");
    dPrintDEC(codeType);
    dPrint("\nCode length is: ");
    dPrintDEC(codeLen);
    dPrint("\nCode value is: ");
    if (codeType == UNKNOWN) {
        if (DEBUG) {
            for (int i = 0; i < RAWBUF; i++) {
                printfEmu("%02X", rawCodes[i]);
            }
        }
    } else {
        dPrintLONG(codeValue);
        dPrint("\n");
    }
}

void setup() {
    Serial.begin(9600);
    restoreID();
    pinMode(RECV_PIN, INPUT);
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
            //When set to 10, this delay causes the serial buffer to overflow 
            //and drop the final bits of the serial string. If this is set to 1, we don't get the last digit
            delay(5); 
        }
        if (String(message) == "reset") {
            EEPROM.write(0, 0);
            transceiverID = 0;
            Serial.println("Transceiver was reset.");
        } else {
            parseMessage(message);
            if (transceiverID == messageDestination) {
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
    delay(5000);
    Serial.println("IR_ID_REQUEST");
}

void restoreID() {
    transceiverID = EEPROM.read(0);
    dPrint("Restored ID as: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
}

void parseMessage(String message) {
    // AAAA - Transciever ID #
    // BBBB - Command Type (r, p, d, a, etc.)
    sscanf(&message[0], "%4x%2x", &messageDestination, &commandType);
    Serial.print(commandType);
}

void assignID() {
    digitalWrite(STATUS_PIN, HIGH);
    sscanf(&message[6], "%4x", &transceiverID);
    EEPROM.write(0, transceiverID);
    digitalWrite(STATUS_PIN, LOW);

    dPrint("Assigned ID to transceiver: ");
    dPrintDEC(transceiverID);
    dPrint("\n");
}

void playCommand() {
    printIRInfo();
    dPrint("\nPlaying a command\n");
    digitalWrite(STATUS_PIN, HIGH);

    // Restore values for playback
    sscanf(&message[6], "%4x%4x", &codeType, &codeLen);

    if (codeType == UNKNOWN) {
        // NOT TESTED
        for (int i = 0; i < RAWBUF; i++) {
            sscanf(&message[14 + i*4], "%4X", &rawCodes[i]);
        }
    } else {
        sscanf(&message[14], "%lx", &codeValue);
    }
    Serial.flush();

    // Play the code
    sendCode(false);
    digitalWrite(STATUS_PIN, LOW);
    digitalWrite(IR_PIN, LOW);

    printIRInfo();
}

void recordCommand() {
    digitalWrite(STATUS_PIN, HIGH);
    irrecv.enableIRIn();
    while (!irrecv.decode(&results)) {}
    storeCode(&results);

    // Send message
    // Message format in Hex is AAAABBBBCCCCC...
    // AAAA is the codeType
    // BBBB is the codeLen
    // CCCCC... is either the codeValue (known code types) or the rawCodes (unknown code type)

    // Print out codeType
    printfEmu("%04X", codeType);

    // Print out codeLenHEX
    printfEmu("%04X", codeLen);

    if (codeType == UNKNOWN) {
        // Print all of rawCodes (array of unsigned ints)
        for (int i = 0; i < RAWBUF; i++) {
            printfEmu("%02X", rawCodes[i]);
        }
    } else {
        // Print codeValue
        printfEmu("%08lX", codeValue);
    }    
    Serial.print("\n");
    irrecv.resume();
    digitalWrite(STATUS_PIN, LOW);
}

void storeCode(decode_results *results) {
    codeType = results->decode_type;
/*    codeType = UNKNOWN;*/
    int count = results->rawlen;
    if (codeType == UNKNOWN) {
        dPrint("\nReceived unknown code, saving as raw\n");
        codeLen = results->rawlen - 1;
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
    } else {
        if (codeType == NEC) {
            dPrint("\nReceived NEC: ");
            if (results->value == REPEAT) {
                // Don't record a NEC repeat value as that's useless.
                dPrint("repeat; ignoring.");
                return;
            }
        }
        else if (codeType == SONY) {
            dPrint("\nReceived SONY: ");
        } 
        else if (codeType == RC5) {
            dPrint("\nReceived RC5: ");
        } 
        else if (codeType == RC6) {
            dPrint("\nReceived RC6: ");
        } 
        else if (codeType == SHARP) {
            dPrint("\nReceived Sharp: ");
        } 
        else if (codeType == PANASONIC) {
            dPrint("\nReceived Panasonic: ");
        }
        else if (codeType == JVC) {
            dPrint("\nReceived JVC: ");
        }
/*        else if (codeType == Sanyo) {*/
/*            dPrint("\nReceived Sanyo: ");*/
/*        }*/
/*        else if (codeType == Mitsubishi) {*/
/*            dPrint("\nReceived Mitsubishi: ");*/
/*        }*/
        else {
            dPrint("\nUnexpected codeType ");
            dPrintDEC(codeType);
            dPrint(" ");
        }

        codeValue = results->value;
        codeLen = results->bits;

    }
    printIRInfo();
}

void sendCode(int repeat) {
    if (codeType == NEC) {
        if (repeat) {
            irsend.sendNEC(REPEAT, codeLen);
            dPrint("\nSent NEC repeat");
        } 
        else {
            irsend.sendNEC(codeValue, codeLen);
            dPrint("\nSent NEC ");
            dPrintHEX(codeValue);
            dPrint("\n");
        }
    }
    else if (codeType == SONY) {
        irsend.sendSony(codeValue, codeLen);
        dPrint("\nSent Sony ");
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
            dPrint("\nSent RC5 ");
            dPrintHEX(codeValue);
            dPrint("\n");
        } 
        else {
            irsend.sendRC6(codeValue, codeLen);
            dPrint("\nSent RC6 ");
            dPrintHEX(codeValue);
            dPrint("\n");
        }
    }
    else if (codeType == SHARP) {
        irsend.sendSharp(codeValue, codeLen);
        dPrint("\nSent Sharp ");
        dPrintHEX(codeValue);
        dPrint("\n");
    }
    else if (codeType == PANASONIC) {
        irsend.sendPanasonic(PANASONICADDRESS, codeValue);
        dPrint("\nSent Panasonic ");
        dPrintHEX(codeValue);
        dPrint("\n");
    }
    else if (codeType == JVC) {
        irsend.sendJVC(codeValue, 16, 0);
        dPrint("\nSent JVC ");
        dPrintHEX(codeValue);
        dPrint("\n");
    }
/*    else if (codeType == SANYO) {*/
/*        irsend.sendSanyo(codeValue, codeLen);*/
/*        dPrint("\nSent Sanyo ");*/
/*        dPrintHEX(codeValue);*/
/*        dPrint("\n");*/
/*    }*/
/*    else if (codeType == MITSUBISHI) {*/
/*        irsend.sendMitsubishi(codeValue, codeLen);*/
/*        dPrint("\nSent Mitsubishi ");*/
/*        dPrintHEX(codeValue);*/
/*        dPrint("\n");*/
/*    }*/
    else if (codeType == 0 /* i.e. raw */) {
        // Assume 38 KHz
        irsend.sendRaw(rawCodes, codeLen, 38);
        dPrint("\nSent raw\n");
    }
}
