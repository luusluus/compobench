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
	"github.com/google/uuid"

	p "webserver_proxy/payload"
)

func Invoke(payload p.Payload) int {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("eu-central-1")},
	)
	if err != nil {
		log.Println(err.Error())
	}

	s3_service := s3.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	result_key := fmt.Sprintf("results/%s.json", payload.WorkflowInstanceId)
	bucket_name := "storage-based-store"

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	put_object_input := &s3.PutObjectInput{
		Body:   bytes.NewReader(b.Bytes()),
		Bucket: aws.String(bucket_name),
		Key:    aws.String(fmt.Sprintf("function_a/%s.json", payload.WorkflowInstanceId)),
	}
	s3_service.PutObject(put_object_input)
	if err != nil {
		log.Println(err)
	}

	time.Sleep(8 * time.Second)

	head_object_input := &s3.HeadObjectInput{
		Bucket: aws.String(bucket_name),
		Key:    aws.String(result_key),
	}
	if err := s3_service.WaitUntilObjectExists(head_object_input); err != nil {
		log.Println(err)
		return 404
	}

	for _, function := range payload.FullWorkflow {
		object_key := fmt.Sprintf("%s/%s.json", function, payload.WorkflowInstanceId)
		delete_object_input := &s3.DeleteObjectInput{
			Bucket: aws.String(bucket_name),
			Key:    aws.String(object_key),
		}
		s3_service.DeleteObject(delete_object_input)
	}

	delete_object_input := &s3.DeleteObjectInput{
		Bucket: aws.String(bucket_name),
		Key:    aws.String(result_key),
	}
	s3_service.DeleteObject(delete_object_input)

	return 200
}
