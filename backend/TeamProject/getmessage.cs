using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using CaseOnline.Azure.WebJobs.Extensions.Mqtt.Messaging;
using CaseOnline.Azure.WebJobs.Extensions.Mqtt;
using System.Text;
using TeamProject.mqtt;

namespace TeamProject
{
    public static class getmessage
    {
        [FunctionName("getmessage")]
        public static void Run(
            [MqttTrigger("/project/tiktem")] IMqttMessage message,
            ILogger log)
        {
            try
            {
                var bytestring = message.GetMessage();
                string jsonlist = Encoding.UTF8.GetString(bytestring);

                sendmqtt.test();

            }
            catch (Exception ex)
            {

                throw ex;
                //return new StatusCodeResult(500);
            }


        }
    }
}
