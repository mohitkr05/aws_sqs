import boto3
import os
import botocore
import hashlib
import csv
import time
import datetime


# The code runs on EC2, continously reading a message from the input Queue
# Once a message is recieved in the input queue , the program will fetch the message
# Read the filename from the attributes, fetch the object from the s3 bucket,
# Process the object with computing hash on each input
# Upload the processed file to the S3
# Send the message to the output queue
#print(datetime.datetime.now())


'''
function = retrieve_S3_object
arguments = bucket_name
object_key = the object in s3
local_file = the file which is to be saved in the os
'''
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



def process_downloaded_file(downloaded_file):
    print(str(datetime.datetime.now()) + "Function Process Downloaded file called  \n")
    hashoutput = ''
    with open(downloaded_file) as f:
        for line in f.readlines():
            numbers = line.split(",")
            for n in numbers:
                k = str(n).encode('utf-8')
                hashoutput = hashoutput + "The SHA256 hash of" + str(n) + " is: --> " + str(hashlib.sha256(k).hexdigest()) + str(",")
    filek = open("processed_file.txt","w")
    filek.write(hashoutput)
    print(str(datetime.datetime.now()) + "File written" + downloaded_file + " \n")
    filek.close()


def upload_file_s3( bucket_name, file):
    print(str(datetime.datetime.now()) + "Function Upload file to S3 called  \n")
    object_info = []
    s3 = boto3.client('s3')
    s3.upload_file(file, bucket_name, file)
    print("File Uploaded \n")
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        if (key['Key'] == file):
            object_info.append(key['Key'])
            object_info.append(key['ETag'])
    print(str(datetime.datetime.now()) + "Function Upload file success : " + str(object_info) + " \n")
    return object_info



def sqs_send_message(object_info, queName):
    print(str(datetime.datetime.now()) + "Function SQS Send message called \n")
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
    print(str(datetime.datetime.now()) + "Sqs message sent \n")


def sqs_read_message(qUrl):
    print(str(datetime.datetime.now()) + "Function SQS read message called \n")
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
    print(str(datetime.datetime.now()) + "Function SQS delete message called \n")
    sqs = boto3.client('sqs')
    response = sqs.delete_message(
    QueueUrl=qUrl,
    ReceiptHandle=msg_rcpt
    )
    print("Message deleted \n")
    return (response)


'''
The main function for the server.
polls for the reading queue every 60 seconds
check for any message and correspondingly process the data
'''
def main():
    print(str(datetime.datetime.now()) + "Server.py started to run \n")
    input_queue = 'ccproject'
    input_queue_uri = 'https://queue.amazonaws.com/126429338143/ccproject'
    output_queue = 'ccproject2'
    output_queue_uri = 'https://queue.amazonaws.com/126429338143/ccproject2'
    s3_bucket_name = 'ccproject2018ht'
    while 1:
      message = sqs_read_message(input_queue_uri)
      print(message)
      for msg in message['Messages']:
          msg_body = msg['Body']
          msg_attr = msg['MessageAttributes']
          msg_rcpt = msg['ReceiptHandle']
      objectname = msg_attr['Key']['StringValue']
      retrieve_S3_object(s3_bucket_name, objectname, 'downloaded_file.txt')
      msg_del = sqs_delete_message(input_queue_uri,msg_rcpt)
      process_downloaded_file('downloaded_file.txt')
      object_info = upload_file_s3(s3_bucket_name,"processed_file.txt")
      sqs_send_message(object_info, output_queue)
      time.sleep(60)

if __name__== "__main__":
  main()
