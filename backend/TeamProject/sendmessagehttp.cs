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

namespace TeamProject
{

    public static class sendmessagehttp
    {
        
        [FunctionName("Sendmessage")]
        public static ActionResult Sendmessage(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "startgame")] HttpRequest req,
            [Mqtt(ConnectionString = "MqttConnection")] out IMqttMessage outMessage,
            ILogger logger)
        {
            try
            {
                string requestbody = new StreamReader(req.Body).ReadToEnd();

                outMessage = new MqttMessage("/project/tiktem", Encoding.ASCII.GetBytes(requestbody), MqttQualityOfServiceLevel.AtLeastOnce, false);
                return new StatusCodeResult(200);
            }
            catch (Exception ex)
            {
                outMessage = null;
                return new StatusCodeResult(500);
            }
        }
    }
}
