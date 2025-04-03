#include <Servo.h>

Servo mouthServo;
bool speaking = false; // Track speech status

void setup()
{
    Serial.begin(9600);
    mouthServo.attach(9); // Connect servo to pin 9
}

void loop()
{
    if (Serial.available())
    {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command == "START")
        {
            speaking = true; // Speech has started
        }
        else if (command == "STOP")
        {
            speaking = false;     // Speech has ended
            mouthServo.write(90); // Close mouth
        }
    }

    if (speaking)
    {
        moveMouthContinuously(); // Keep moving mouth while speaking
    }
}
a void moveMouthContinuously()
{
    mouthServo.write(120);
    delay(200);
    mouthServo.write(90);
    delay(200);
}