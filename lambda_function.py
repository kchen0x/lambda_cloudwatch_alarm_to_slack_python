#!/usr/bin/python3.7

import urllib3
import json
from datetime import datetime

http = urllib3.PoolManager()
url = 'https://hooks.slack.com/services/xxx'
channel_name = '#xxx'

def handle_cloudwatch(event, context):
    ts_string = event['Records'][0]['Sns']['Timestamp']
    ts_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    timestamp = datetime.strptime(ts_string, ts_format).timestamp()
    message = json.loads(event['Records'][0]['Sns']['Message'])
    region = event['Records'][0]['EventSubscriptionArn'].split(':')[3]
    subject = 'AWS CloudWatch Notification'
    alarmName = message['AlarmName']
    metricName = message['Trigger']['MetricName']
    oldState = message['OldStateValue']
    newState = message['NewStateValue']
    alarmDescription = message['AlarmDescription']
    alarmReason = message['NewStateReason']
    trigger = message['Trigger']
    color = 'warning'

    if (message['NewStateValue'] == 'ALARM'):
        color = 'danger'
    elif (message['NewStateValue'] == 'OK'):
        color = 'good'
    
    slack_message = {
        'channel': channel_name,
        'text': '*' + subject + '*',
        'attachments': [
        {
            'color': color,
            'fields': [
            { 'title': 'Alarm Name', 'value': alarmName, 'short': True },
            { 'title': 'Alarm Description', 'value': alarmDescription, 'short': False},
            {
                'title': 'Trigger',
                'value': trigger['Statistic'] + ' '
                + metricName + ' '
                + trigger['ComparisonOperator'] + ' '
                + str(trigger['Threshold']) + ' for '
                + str(trigger['EvaluationPeriods']) + ' period(s) of '
                + str(trigger['Period']) + ' seconds.',
                'short': False
            },
            { 'title': 'Old State', 'value': oldState, 'short': True },
            { 'title': 'Current State', 'value': newState, 'short': True },
            {
                'title': 'Link to Alarm',
                'value': 'https://' + region + '.console.aws.amazon.com/cloudwatch/home?region=' + region + '#s=Alarms&alarm=' + alarmName,
                'short': False
            }
            ],
            'ts':  timestamp
        }
        ]
    }
    
    return slack_message

def post_message(message):
    body = json.dumps(message).encode('utf-8')
    resp = http.request('POST', url, body=body)
    print({
        'status_code': resp.status, 
        'response': resp.data
    })

def lambda_handler(event, context):
    print('sns received:' + json.dumps(event))

    slack_message = None
    event_subscription_arn = event['Records'][0]['EventSubscriptionArn']
    event_sns_subject = event['Records'][0]['Sns']['Subject'] or 'no subject'
    event_sns_message_raw = event['Records'][0]['Sns']['Message']
    event_sns_message = None

    if (True):
        print('processing cloudwatch notification')
        slack_message = handle_cloudwatch(event, context)

    post_message(slack_message)
