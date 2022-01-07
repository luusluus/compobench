package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	async "webserver_proxy/async_function"
	mq "webserver_proxy/message_queue"
	p "webserver_proxy/payload"
	sync "webserver_proxy/sync_function"
	sfn "webserver_proxy/workflow_engine"
)

func sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := sync.Invoke(message, "SequenceFunctionA")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func compiled(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := sync.Invoke(message, "CompiledFunction")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func coordinator(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := sync.Invoke(message, "CoordinatorFunctionCoordinator")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := async.Invoke(message, "AsyncSequenceFunctionA", "async-sequence-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func routing_slip(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := async.Invoke(message, "RoutingSlipFunctionA", "routing-slip-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_coordinator(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := async.Invoke(message, "AsyncCoordinatorFunctionCoordinator", "async-coordinator-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func message_queue(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := mq.Invoke(message)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func workflow_engine(w http.ResponseWriter, req *http.Request) {
	message := parse_payload(req)

	status_code := sfn.Invoke(message)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func parse_payload(req *http.Request) p.Payload {
	var p p.Payload
	err := json.NewDecoder(req.Body).Decode(&p)
	if err != nil {
		fmt.Println(err)
	}
	return p
}

func main() {
	http.HandleFunc("/sequence", sequence)
	http.HandleFunc("/coordinator", coordinator)
	http.HandleFunc("/compiled", compiled)
	http.HandleFunc("/async_sequence", async_sequence)
	http.HandleFunc("/routing_slip", routing_slip)
	http.HandleFunc("/async_coordinator", async_coordinator)
	http.HandleFunc("/message_queue", message_queue)
	http.HandleFunc("/workflow_engine", workflow_engine)

	fmt.Printf("Starting server at port 8000\n")
	http.ListenAndServe(":8000", nil)
}
