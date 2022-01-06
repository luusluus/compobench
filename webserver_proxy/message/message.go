package message

type Message struct {
	Sleep              int      `json:"sleep"`
	Workflow           []string `json:"workflow"`
	WorkflowInstanceId string   `json:"workflow_instance_id"`
}
