import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import boto3

ssm = boto3.client('ssm')

def lambda_handler(event,context):

    print(json.dumps(event))
    
    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(json.dumps(message))
    

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    
    json_values = {
        "fields": {
            "project":
                {
                    "key": "CIT"
                },
            "summary": alarm_name + " has new status" + new_state,
            "description": alarm_name + " has new status  " + new_state + " Reason : " + reason,
            "issuetype": {
                "name": "Bug"
            }    
        }
    }
 
    jiraurl_tmp = ssm.get_parameter(Name='jiraurl')
    jiraurl = jiraurl_tmp['Parameter']['Value']
    
    myAuthString_tmp = ssm.get_parameter(Name='myAuthString', WithDecryption=True)
    myAuthString = myAuthString_tmp['Parameter']['Value']
    
    print(jiraurl)
    print(myAuthString)
 
    req = Request(jiraurl, data=json.dumps(json_values).encode('utf-8'), 
                headers={'Authorization': myAuthString, 'Content-Type': 'application/json'})
    
    try:
        response = urlopen(req)
        response.read()
        
        print(".. JIRA issue created ...")
    except HTTPError as e:
        print('Request failed:')
    except URLError as e:
        print('Server Connection failed:')