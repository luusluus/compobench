package client_side

import (
	"bytes"
	"encoding/json"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
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

	service := lambda.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)
	for _, function_name := range payload.Workflow {
		input := &lambda.InvokeInput{
			FunctionName: aws.String(function_name),
			Payload:      b.Bytes(),
		}
		response, err := service.Invoke(input)

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

		json.NewDecoder(bytes.NewReader(response.Payload)).Decode(&payload.Input)
		b = new(bytes.Buffer)
		json.NewEncoder(b).Encode(payload)
	}

	return 200
}
