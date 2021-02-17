<h1>Creating a ticket in JIRA from AWS CloudWatch Alarm with Lambda if CPU usage is high in EC2 instance</h1>
<p> We will create a simple application to automatically generate a ticket in JIRA using JIRA API through AWS Lambda function 
if the CloudWatch alarm has detected CPU usage > 40 in EC2. It will be a built-on serverless architecture and will be using the following AWS services EC2, 
CloudWatch Alarm, SNS (Simple Notification Service), AWS Lambda, System Manager Parameter Store and CloudFormation</p>
<br>
<p>You want to know more about AWS services, click https://docs.aws.amazon.com</p>

Building the application

Let’s build this application step by step. We will use the CloudFormation template to create and configure all necessary AWS resources like EC2, SNS topic, and Lambda function. We will not use AWS console instead we will run all commands through AWS CLI. 

<h3> 1. JIRA Bug & Issue Tracking System:</h3>
<p>JIRA is a powerful bug & issue tracker tool using by various companies to manage project workflows, track internal or external issues and manage test cases. 
Here, we will use the JIRA software cloud account for this application. In your JIRA cloud, We will create a JIRA project named “Cloud Infra Tickets (CIT)” 
since it will be used later in Lambda function, All EC2 CPU usage issues will be created under this project. 
Following JIRA REST API will be used to interact with JIRA programmatically. You need to generate an authentication token which will be provided along with the REST API call.</p>

<p>https://[username].atlassian.net/rest/api/2/issue</p>

([username] will be replaced with you JIRA username)
