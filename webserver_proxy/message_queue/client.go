package message_queue

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sns"
	"github.com/google/uuid"

	m "webserver_proxy/message"
)

func Invoke(payload m.Message) int {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("eu-central-1")},
	)
	if err != nil {
		log.Println(err.Error())
	}

	service := sns.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	result_key := fmt.Sprintf("result_%s.json", payload.WorkflowInstanceId)

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	message_attributes := make(map[string]*sns.MessageAttributeValue)

	message_attributes["caller"] = &sns.MessageAttributeValue{
		DataType:    aws.String("String"),
		StringValue: aws.String("Client"),
	}

	message_attributes["last_function"] = &sns.MessageAttributeValue{
		DataType:    aws.String("String"),
		StringValue: aws.String("MessageQueueFunctionC"),
	}

	publish_input := &sns.PublishInput{
		Message:           aws.String(b.String()),
		MessageAttributes: message_attributes,
		TopicArn:          aws.String("arn:aws:sns:eu-central-1:923301848785:MessageQueueTopic"),
	}

	service.Publish(publish_input)
	if err != nil {
		log.Println(err)
	}

	time.Sleep(6 * time.Second)

	s3_service := s3.New(sess)
	bucket_name := "message-queue-store"
	head_object_input := &s3.HeadObjectInput{
		Bucket: aws.String(bucket_name),
		Key:    aws.String(result_key),
	}
	if err := s3_service.WaitUntilObjectExists(head_object_input); err != nil {
		fmt.Println(err)
		return 404
	}
	delete_object_input := &s3.DeleteObjectInput{
		Bucket: aws.String(bucket_name),
		Key:    aws.String(result_key),
	}
	s3_service.DeleteObject(delete_object_input)

	return 200
}
