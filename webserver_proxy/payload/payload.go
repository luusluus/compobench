package message

type Payload struct {
	Sleep              int      `json:"sleep"`
	WorkflowInstanceId string   `json:"workflow_instance_id"`
	Workflow           []string `json:"workflow"`
	Composition        []string `json:"composition"`
	Input              string   `json:"input"`
}
