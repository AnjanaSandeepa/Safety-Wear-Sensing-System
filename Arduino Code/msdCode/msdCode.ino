#include <Servo.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

const int buzzer = 13; //D7
const int servo = 14; //D5
const int red = 12; //D6
const int green = 15; //D8

Servo myservo;
LiquidCrystal_I2C lcd(0x3F, 16, 2);

int incomingByte;

int pos =0; //position of servo
String crs = "null";  //Serial read String
bool serial = false;  //Serial read String validation
int cri = 0;  //Serial read integer

int const_byteCount = 50;
int const_countH = 30;
int interval = 4000;
int const_waitingTime = 5000;

int countH = 0;
int countN = 0;
int countL = 0;
int countP = 0;
int byteCount = 0;

unsigned long previousMillis = 0;
unsigned long currentMillis = 0;

void setup() {
  Serial.begin(9600);

  Wire.begin(2, 0);
  lcd.init();
  lcd.backlight();

  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("WELCOME...");

  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);

  pinMode(buzzer, OUTPUT);

  myservo.attach(servo);
  myservo.write(0);
  delay(1000);
  myservo.write(60);
  delay(1000);
  myservo.write(0);

}

void loop()
{
  if (Serial.available() > 0)
  {
    if(serial== false)
    {
      crs = Serial.readString();

      cri = crs.toInt();

      if(cri != 0)
      {
        const_waitingTime = cri % 100;
        cri = cri /100;
        interval = (cri % 100)*100;
        cri = cri /100;
        const_countH = cri % 100;
        cri = cri /100;
        const_byteCount = cri % 100;

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.printf("Fb = %d",const_byteCount);
        lcd.setCursor(9, 0);
        lcd.printf("AC = %d",const_countH);
        lcd.setCursor(0, 1);
        lcd.printf("FR = %d",interval/100);
        lcd.setCursor(9, 1);
        lcd.printf("WT = %d",const_waitingTime);
        delay(2000);
      }
    serial=true;
    }

    incomingByte = Serial.read();

    if(incomingByte== 'A')
    {
      serial=false;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.printf("SYSTEM RESETED");
      delay(1000);
    }

    while(incomingByte =='P'){

      digitalWrite(green, HIGH);

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("  ALWAYS OPEN");
      lcd.setCursor(0, 1);
      lcd.print("   MODE IS ON");

      if(pos < 170)
      {
        tone(buzzer, 2000);
        delay(1000);
        noTone(buzzer);

        for (pos = 0; pos <= 180; pos += 1)
        {
          myservo.write(pos);
          delay(20);
        }
        pos = 180;
      }

      delay(1000);


      if(Serial.read() == 'Q')
      {
        for (pos = 180; pos >= 0; pos -= 1)
        {
          myservo.write(pos);
          delay(20);
        }
      tone(buzzer, 2000);
      delay(1000);
      noTone(buzzer);
      digitalWrite(green, LOW);
      break;
      }
      else
      {
        incomingByte =='P';
      }
    }

    byteCount +=1;

    digitalWrite(green, LOW);
    digitalWrite(red, HIGH);

    lcd.clear();
    lcd.setCursor(5, 0);
    lcd.print("Hi... ");
    lcd.setCursor(0, 1);
    lcd.print("  PLEASE WAIT");

    if(byteCount <= const_byteCount)
    {
      if (incomingByte == 'H')
      {
        countH += 1;
      }
      else if (incomingByte == 'L')
      {
        countL += 1;
      }
    }

    if(byteCount == const_byteCount)
    {
      if(countH >= const_countH)
      {
        countP += 1;

        digitalWrite(green, HIGH);
        digitalWrite(red, LOW);

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("  YOUR WARE IS");
        lcd.setCursor(5, 1);
        lcd.print("DETECTED");

        tone(buzzer, 2000);
        delay(1000);
        noTone(buzzer);

        for (pos = 0; pos <= 180; pos += 1)
        {
          myservo.write(pos);
          delay(20);
        }

        lcd.clear();
        lcd.setCursor(4, 0);
        lcd.print("YOU CAN GO");
        lcd.setCursor(7, 1);
        lcd.print("NOW");

        delay(const_waitingTime);

        lcd.clear();
        lcd.setCursor(3, 0);
        lcd.print("THANK YOU...");
        lcd.setCursor(0, 1);
        lcd.printf("   PERSON = %d",countP);
        delay(2000);

        for (pos = 180; pos >= 0; pos -= 1)
        {
          myservo.write(pos);
          delay(20);
        }

        tone(buzzer, 2000);
        delay(1000);
        noTone(buzzer);

        Serial.print(countP);

        Serial.begin(9600);
        delay(1000);
      }
      else
      {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("  YOUR WARE IS");
        lcd.setCursor(3, 0);
        lcd.print("NOT DETECTED");
      }
      countH =0;
      countL =0;
      byteCount =0;
      Serial.begin(9600);
    }
  }
  else
  {
    unsigned long currentMillis = millis();

    if ((currentMillis - previousMillis) >= interval)
    {
    digitalWrite(green, LOW);
    digitalWrite(red, LOW);

    lcd.clear();
    lcd.setCursor(3, 0);
    lcd.print("WELCOME...");

    previousMillis = currentMillis;
    }
  }
}