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

<h3> 2. AWS System Manager Parameter Store:</h3>
<p>You need to store the JIRA API URL and the authentication token in Parameter Store securely. These will be used by our Lambda function to make a connection with JIRA programmatically. Run the below mention AWS CLI commands to create and store values in Parameter Store, make sure parameter names are same as below otherwise you have you change these names in Lambda function.</p>

<h4>aws ssm put-parameter --name "mysecurestring" --value "Enter Your Token Value Here" --type SecureString</h4><br>
<h4>aws ssm put-parameter --name "jiraurl" --value "https://[username].atlassian.net/rest/api/2/issue" --type String</h4>

<h3> 3. S3 bucket and Lambda function:</h3>
<p>You can download the lambda function from GitHub link in your local directory and zip it again or download the zipped to upload on your newly created bucket. Create a S3 bucket and upload your Lambda function using below AWS CLI commands. You need to change S3 bucket name CloudFormation template</p>

<h4>aws s3api create-bucket --bucket entreyours3bucketname --region us-east-1</h4><br>
<h4>aws s3 cp .\lambda.zip s3://enteryours3bucketname</h4>

<h3> 4. Creating Stack with CloudFormation:</h3> 
<p>We need to create the SNS, CloudWatch Alarm and EC2 instance, Security Group, Lambda function and IAM roles. CloudFormation template will create all these resources with configuration and their dependencies. You just need to change the S3 bucket name in CloudFormation template with you S3 bucket that you have created in previous step. Run below AWS CLI command to create CloudFormation Stack from the template</p>

<h4>aws cloudformation create-stack --stack-name myteststack --template-body file://jira_cloudwatch.yaml</h4>

You can verify all you resource while login into the AWS console. 

<h2>Testing our application</h2>
<p>Now you can SSH into the Linux EC2 instance from the AWS console and connect using a standalone client or the browser-based SSH connection. You need to run Linux stress utility to stress the CPU which will concurrently increase CPU usage. Stress is a Simple command-line utility used to conduct CPU memory and disk tests. So, run below commands to install some extra Linux packages for Linux Stress utility</p>

<h4>sudo amazon-linux-extras install epel</h4><br>
<h4>sudo yum install -y stress</h4>

<p>Now, you can run the below command to beat up the CPU for 5 mins; This will push EC2 CPU to 100% usage. You can then monitor the CloudWatch alarm as the CPU is being stressed. CloudWatch Alarm will be changed from ‘OK’ to ‘In Alarm’ state. </p>

<h4>stress --cpu 2 --timeout 300s<h4>

<p>You can also verify the Lambda CloudWatch to see if Lambda is being executed properly. Login into you JIRA dashboard and verify the ticket created by AWS CloudWatch Alarm / Lambda function.</p>

<h2>Cleanup Resources:</h2>
<p>You can run below AWS CLI command to delete all resources created by CloudFormation stack. Navigate to AWS console and empty S3 bucket and delete bucket.</p>

<h4>aws cloudformation delete-stack --stack-name myteststack</h>
