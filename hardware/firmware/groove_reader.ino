// groove_reader.ino – Arduino-based U-bottom groove reader
// All Rights Reserved ® Seliim Ahmed

#include <LiquidCrystal.h>

// Pin definitions
const int laserPin = 9;
const int photodiodePin = A0;
const int stepPin = 3;
const int dirPin = 4;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
    Serial.begin(115200);
    pinMode(laserPin, OUTPUT);
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    lcd.begin(16, 2);
    lcd.print("Groove Reader");
    delay(1000);
}

void loop() {
    // Sweep frequency
    for (int f = 1000; f <= 100000; f += 100) {
        analogWrite(laserPin, f / 1000);
        int reading = analogRead(photodiodePin);
        Serial.print(f);
        Serial.print(",");
        Serial.println(reading);
        delay(10);
    }

    // Move to next groove
    digitalWrite(dirPin, HIGH);
    for (int i = 0; i < 200; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(500);
    }

    delay(1000);
}
