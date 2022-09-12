#include<Servo.h> 

 
Servo myservo; 
int servoPin = 12;
int pos = 0; 
int temp = 0;


void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin);
  Serial.flush();
}

void loop() {
  while (Serial.available() > 0) {
    float temp = Serial.parseFloat(); //숫자로 된 문자열을 숫자로 바꿔준다.
    if (temp<=37.5)
    {
      for(pos = 100; pos>=1; pos-=1)
      { 
        myservo.write(pos); 
        delay(20); 
      } 
      delay (3000);
      
      for(pos = 0; pos < 100; pos += 1) 
      { 
        myservo.write(pos);
        delay(20); //delay값을 조정하여 모터의 속도를 컨터롤가능
        
      } 
    } 
  }
}

 
