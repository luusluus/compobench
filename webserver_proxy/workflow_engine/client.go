package workflow_engine

import (
	"bytes"
	"encoding/json"
	"log"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sfn"
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

	service := sfn.New(sess)

	payload.WorkflowInstanceId = uuid.New().String()

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	execution_input := &sfn.StartExecutionInput{
		StateMachineArn: aws.String("arn:aws:states:eu-central-1:923301848785:stateMachine:WorkflowStateMachine"),
		Input:           aws.String(b.String()),
	}
	output, err := service.StartExecution(execution_input)
	if err != nil {
		log.Println(err)
	}

	time.Sleep(6 * time.Second)

	describe_execution_input := &sfn.DescribeExecutionInput{
		ExecutionArn: output.ExecutionArn,
	}
	status_code := 500
	for {
		output, err := service.DescribeExecution(describe_execution_input)
		if err != nil {
			log.Println(err)
		}
		if *output.Status == "SUCCEEDED" {
			status_code = 200
			break
		} else if *output.Status == "RUNNING" {
			time.Sleep(100 * time.Millisecond)
		} else {
			status_code = 400
			break
		}
	}
	return status_code
}
