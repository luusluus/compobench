package async_sequence

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
	event_history_table := "EventHistoryTable"

	payload.WorkflowInstanceId = uuid.New().String()

	lambda_service := lambda.New(sess)

	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(payload)

	input := &lambda.InvokeInput{
		FunctionName:   aws.String("EventSourcingOrchestrator"),
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
		time.Sleep(8 * time.Second)

		retries := 1
		for {
			tables, _ := dynamodb_service.ListTables(&dynamodb.ListTablesInput{})
			for _, table_name := range tables.TableNames {
				if strings.Contains(*table_name, event_history_table) {
					event_history_table = *table_name
				}
			}

			filter := expression.Name("WorkflowInstanceId").Equal(expression.Value(payload.WorkflowInstanceId))
			filter_expression, _ := expression.NewBuilder().WithFilter(filter).Build()
			scan_input := &dynamodb.ScanInput{
				ExpressionAttributeNames:  filter_expression.Names(),
				ExpressionAttributeValues: filter_expression.Values(),
				FilterExpression:          filter_expression.Filter(),
				TableName:                 aws.String(event_history_table),
			}
			query_result, _ := dynamodb_service.Scan(scan_input)

			for _, item := range query_result.Items {
				event_type_id := *item["EventTypeId"].N
				if event_type_id == "6" {
					return 200
				}
			}

			time.Sleep(100 * time.Millisecond)
			retries += 1

			if retries > 100 {
				break
			}
		}
	}
	return 404
}