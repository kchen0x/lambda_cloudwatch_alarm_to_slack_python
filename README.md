# lambda_cloudwatch_alarm_to_slack_python

An [AWS Lambda](http://aws.amazon.com/lambda/) function for better Slack notifications. 

This function was inspired by [assertible](https://github.com/assertible/lambda-cloudwatch-slack) and implemented with Python. 

It provides:

**Better default formatting for CloudWatch notifications**:


**Support for both AWS global and AWS China**

## How to use

Change the Slack webhook URL and channel name with your one and deploy the function to AWS Lambda. You should make sure the function has role with the access to your AWS SNS.
