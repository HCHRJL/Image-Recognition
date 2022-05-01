/////////////////////
////匯入函式庫與定義////
/////////////////////
#include <ros.h>
#include <geometry_msgs/Vector3.h>  ////訊息格式////

ros::NodeHandle  nh;                ////節點開始//(用於管理節點)////

///////////////////////////////////////
////訊息格式//定義變量//宣告常數與全域變數////
///////////////////////////////////////
void messageCb( const geometry_msgs::Vector3& toggle_msg)
{
////指定所要更改輸出的端子編號以及端子輸出的狀態。////
  digitalWrite(12, HIGH-digitalRead(12));        ////digitalWrite( LED_PIN, HIGH )//pinMode//引腳編號//腳位////
  delay(1000);                                   ////暫停程式執行//1 secord////
  digitalWrite(12, LOW );                        ////低電位////
}

///////////////////////////////////
////節點的接收//訊息格式//topic名稱////
///////////////////////////////////
ros::Subscriber<geometry_msgs::Vector3> sub("face", &messageCb );

///////////////
////設定函式////
///////////////
void setup()
{ 
  pinMode(12, OUTPUT);    ////OUTPUT模式////
  nh.initNode();          ////初始化節點////
  nh.subscribe(sub);      ////接收節點////
}

///////////////
////無限迴圈////
//////////////
void loop()
{  
////spin()在呼叫後不會再返回////
  nh.spinOnce();
  delay(1);
}
