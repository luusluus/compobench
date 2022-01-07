package blackboard

import (
	"bytes"
	"encoding/json"
	"log"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/expression"
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
	dynamodb_service := dynamodb.New(sess)
	execution_table := "BlackboardWorkflowExecutionTable"

	payload.WorkflowInstanceId = uuid.New().String()

	lambda_service := lambda.New(sess)

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	input := &lambda.InvokeInput{
		FunctionName:   aws.String("BlackboardFunctionController"),
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

	log.Println(payload.WorkflowInstanceId)
	status_code := int(*(result.StatusCode))
	if status_code == 202 {
		time.Sleep(8 * time.Second)

		tables, _ := dynamodb_service.ListTables(&dynamodb.ListTablesInput{})
		for _, table_name := range tables.TableNames {
			if strings.Contains(*table_name, execution_table) {
				execution_table = *table_name
			}
		}

		filter := expression.Name("WorkflowInstanceId").Equal(expression.Value(payload.WorkflowInstanceId))
		filter_expression, _ := expression.NewBuilder().WithFilter(filter).Build()
		scan_input := &dynamodb.ScanInput{
			ExpressionAttributeNames:  filter_expression.Names(),
			ExpressionAttributeValues: filter_expression.Values(),
			FilterExpression:          filter_expression.Filter(),
			TableName:                 aws.String(execution_table),
		}

		retries := 1
		for {
			query_result, _ := dynamodb_service.Scan(scan_input)
			for _, item := range query_result.Items {
				event_type_id := *item["StepId"].N
				if event_type_id == "3" {
					log.Println(*item["WorkflowInstanceId"].S)
					return 200
				}
			}

			time.Sleep(100 * time.Millisecond)
			retries += 1

			if retries > 50 {
				break
			}
		}
	}
	return 404
}
