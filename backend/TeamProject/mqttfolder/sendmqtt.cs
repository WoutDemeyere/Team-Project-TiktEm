using Microsoft.AspNetCore.Mvc;
using MQTTnet.Diagnostics;
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace TeamProject.mqtt
{
    public class sendmqtt
    {
        public static void test()
        {
            MqttClient client;
            IPAddress brokeradres = IPAddress.Parse("13.81.105.139");
            client = new MqttClient(brokeradres);
            string clientId = Guid.NewGuid().ToString();
            client.Connect(clientId);
            client.Publish("/project/tiktem1", Encoding.UTF8.GetBytes("verified"), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        }
    }
}
