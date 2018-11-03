# Distributed architecture implementation using Amazon AWS

The project aims to implement the distributed architecture using the Amazon AWS

## Challenges
- Application should run locally on your machine
- User inputs a comma-separated list of numbers.
- Puts this list in the S3-bucket (and remembers the key/pointer to this object).
- Puts a message in the SQS-inbox with a key/pointer to the object in the S3-bucket, along with a process to be executed on these numbers.
- Waits until a response is generated in the SQS-outbox (should contain a pointer to a new, and processed, object in the S3-bucket along with the process executed).
- Reads the result from the S3-bucket
- Prints the results along with the original numbers and the the process that was done.
- Deletes the result-message from the SQS-outbox.

## To Do
- Bug Fixes
- implementation for second EC2

## Architecture

![alt text](https://raw.githubusercontent.com/mohitkr05/aws_sqs/master/architecture.png)


## Getting Started

- upload the server.py on EC2
- Configure the SQS queues
- Create a S3 bucket
- provide details in both server.py and client.py

### Working Logs
The concurrent operation can be verified using the generated logs:




Client
> $ python3 client.py
2018-11-03 13:15:51.779948 : Client.py started to run

Please enter comma seperated numbers
1,2,34,5,6,7,8,9
File Written

2018-11-03 13:16:07.003610 : Function Upload file to S3 called  

File Uploaded

2018-11-03 13:16:08.398641 : Function Upload file success : ['testfile.txt', '""']

2018-11-03 13:16:08.402093 : Function SQS Send message called

2018-11-03 13:16:09.493060 : Sqs message sent

2018-11-03 13:17:09.554386 : Function SQS read message called

2018-11-03 13:17:10.448567 : Function Retrieve S3 Object called  

2018-11-03 13:17:11.556362: Function Retrieve S3 Success  

2018-11-03 13:17:11.559597 : Function SQS delete message called

Message deleted

2018-11-03 13:17:12.398608 : The process is completed , downloaded file is hashed_file.txt

>$ cat downloaded_file.txt
1,2,34,5,6,7,8,9


>$ cat hashed_file.txt
The SHA256 hash of1 is: --> 6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b,The SHA256 hash of2 is: --> d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35,The SHA256 hash of34 is: --> 86e50149658661312a9e0b35558d84f6c6d3da797f552a9657fe0558ca40cdef,The SHA256 hash of5 is: --> ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d,The SHA256 hash of6 is: --> e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683,The SHA256 hash of7 is: --> 7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451,The SHA256 hash of8 is: --> 2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3,The SHA256 hash of9 is: --> 19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7,



Server
python3 server.py
2018-11-03 13:16:14.873204 :Server.py started to run                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
2018-11-03 13:16:14.873278 :Function SQS read message called                                                                                                                                                                                                                   
2018-11-03 13:16:16.928159 :Function Retrieve S3 Success                                                                                                                                                                                                                       
2018-11-03 13:16:16.931745 :Function SQS delete message called

Message deleted                                                                                                                                                                                                                                                                               
2018-11-03 13:16:17.779195 :Function Process Downloaded file called
2018-11-03 13:16:17.780137 :File written downloaded_file.txt
2018-11-03 13:16:17.780413 :Function Upload file to S3 called                                                                                                                                                                                                                    

File Uploaded
2018-11-03 13:16:19.031185: Function Upload file success : ['processed_file.txt', '""']
2018-11-03 13:16:19.032231: Function SQS Send message called
2018-11-03 13:16:20.133111: Sqs message sent
2018-11-03 13:17:20.191642: Function SQS read message called
