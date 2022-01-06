package async_sequence

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/google/uuid"

	m "webserver_proxy/message"
)

func Invoke(payload m.Message, function_name string, bucket_name string) int {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("eu-central-1")},
	)
	if err != nil {
		log.Println(err.Error())
	}

	lambda_service := lambda.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	result_key := fmt.Sprintf("result_%s.json", payload.WorkflowInstanceId)

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	input := &lambda.InvokeInput{
		FunctionName:   aws.String(function_name),
		Payload:        b.Bytes(),
		InvocationType: aws.String("Event"),
	}

	result, err := lambda_service.Invoke(input)
	if err != nil {
		if aerr, ok := err.(awserr.Error); ok {
			switch aerr.Code() {
			case lambda.ErrCodeTooManyRequestsException:
				return 429
			default:
				return 500
			}
		}
	}
	status_code := int(*(result.StatusCode))
	if status_code == 202 {
		time.Sleep(6 * time.Second)

		s3_service := s3.New(sess)
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
	}
	return 200
}
