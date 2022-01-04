package function_sequence

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"

	"fmt"
)

func Invoke(payload []byte) int {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("eu-central-1")},
	)
	if err != nil {
		fmt.Println(err.Error())

	}

	service := lambda.New(sess)

	input := &lambda.InvokeInput{
		FunctionName: aws.String("SequenceFunctionA"),
		Payload:      payload,
	}

	result, err := service.Invoke(input)
	if err != nil {
		fmt.Println(err)
	}

	return int(*(result.StatusCode))

}
