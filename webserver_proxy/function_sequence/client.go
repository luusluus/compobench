package function_sequence

import (
	"bytes"
	"encoding/json"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
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

	service := lambda.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	input := &lambda.InvokeInput{
		FunctionName: aws.String("SequenceFunctionA"),
		Payload:      b.Bytes(),
	}

	result, err := service.Invoke(input)
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

	return int(*(result.StatusCode))

}
