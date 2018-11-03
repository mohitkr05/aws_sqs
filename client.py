#main.py
#The application will ask for numbers to encrypt them using an encrytion algorithm
import boto3
import os
import botocore
import hashlib
import csv
import time
import datetime
#from boto.sqs.message import Message

def retrieve_S3_object(bucket_name,object_key, local_file):
    print(str(datetime.datetime.now()) + "Function Retrieve S3 Object called  \n")
    print(datetime.datetime.now())
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).download_file(object_key,local_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    print(str(datetime.datetime.now()) + ": Function Retrieve S3 Success  \n")



# Function to get comma seperated numbers from the user and writes a file
def getnumbers():
    final_number = []
    numbers = input("Please enter comma seperated numbers \n")
    filek = open("testfile.txt","w")
    filek.write(numbers)
    print("File Written \n")
    filek.close()


def upload_file_s3( bucket_name, file):
    print(str(datetime.datetime.now()) + " : Function Upload file to S3 called  \n")
    object_info = []
    s3 = boto3.client('s3')
    s3.upload_file(file, bucket_name, file)
    print("File Uploaded \n")
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        if (key['Key'] == file):
            object_info.append(key['Key'])
            object_info.append(key['ETag'])
    print(str(datetime.datetime.now()) + " : Function Upload file success : " + str(object_info) + " \n")
    return object_info



def sqs_send_message(object_info, queName):
    print(str(datetime.datetime.now()) + " : Function SQS Send message called \n")
    sqs = boto3.client('sqs')
    response = sqs.get_queue_url(QueueName=queName)
    qUrl = response['QueueUrl']
    sqs.send_message(
    QueueUrl=qUrl,
    MessageBody='test_message', MessageAttributes={
    'Key': {
    'StringValue': object_info[0],
    'DataType': 'String'
    },
    'ETag':{
    'StringValue': object_info[1],
    'DataType': 'String'
    }
    })
    print(str(datetime.datetime.now()) + " : Sqs message sent \n")


def sqs_read_message(qUrl):
    print(str(datetime.datetime.now()) + " : Function SQS read message called \n")
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
    QueueUrl=qUrl,
    AttributeNames=[
        'All',
    ],
    MessageAttributeNames=[
        'All',
    ],
    MaxNumberOfMessages=1,
    VisibilityTimeout=20,
    WaitTimeSeconds=20,
    ReceiveRequestAttemptId='string'
    )
    return (response)


def sqs_delete_message(qUrl , msg_rcpt):
    print(str(datetime.datetime.now()) + " : Function SQS delete message called \n")
    sqs = boto3.client('sqs')
    response = sqs.delete_message(
    QueueUrl=qUrl,
    ReceiptHandle=msg_rcpt
    )
    print("Message deleted \n")
    return (response)



def main():
    print(str(datetime.datetime.now()) + " : Client.py started to run \n")
    input_queue = 'ccproject'
    input_queue_uri = 'https://queue.amazonaws.com/126429338143/ccproject'
    output_queue = 'ccproject2'
    output_queue_uri = 'https://queue.amazonaws.com/126429338143/ccproject2'
    s3_bucket_name = 'ccproject2018ht'
    getnumbers()
    object_info = upload_file_s3("ccproject2018ht","testfile.txt")
    sqs_send_message(object_info , input_queue)
    time.sleep(60)
    message = sqs_read_message(output_queue_uri)
    print(message)
    for msg in message['Messages']:
        msg_body = msg['Body']
        msg_attr = msg['MessageAttributes']
        msg_rcpt = msg['ReceiptHandle']
    objectname = msg_attr['Key']['StringValue']
    retrieve_S3_object(s3_bucket_name, objectname, 'hashed_file.txt')
    msg_del = sqs_delete_message(output_queue_uri,msg_rcpt)
    print(str(datetime.datetime.now()) + " : The process is completed , downloaded file is hashed_file.txt")


if __name__== "__main__":
  main()
