package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	async "webserver_proxy/async_function"
	bb "webserver_proxy/blackboard"
	cs "webserver_proxy/client_side"
	es "webserver_proxy/event_sourcing"
	mq "webserver_proxy/message_queue"
	p "webserver_proxy/payload"
	sb "webserver_proxy/storage"
	sync "webserver_proxy/sync_function"
	sfn "webserver_proxy/workflow_engine"
)

func client_side(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := cs.Invoke(payload)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func sequence(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := sync.Invoke(payload, "SequenceFunctionA")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func compiled(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := sync.Invoke(payload, "CompiledFunction")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func coordinator(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := sync.Invoke(payload, "CoordinatorFunctionCoordinator")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_sequence(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := async.Invoke(payload, "AsyncSequenceFunctionA", "async-sequence-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func routing_slip(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := async.Invoke(payload, "RoutingSlipFunctionA", "routing-slip-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_coordinator(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := async.Invoke(payload, "AsyncCoordinatorFunctionCoordinator", "async-coordinator-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func event_sourcing(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := es.Invoke(payload)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func blackboard(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := bb.Invoke(payload)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func message_queue(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := mq.Invoke(payload)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func storage_based(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := sb.Invoke(payload)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func workflow_engine(w http.ResponseWriter, req *http.Request) {
	payload := parse_payload(req)

	status_code := sfn.Invoke(payload)

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
	http.HandleFunc("/client_side", client_side)
	http.HandleFunc("/sequence", sequence)
	http.HandleFunc("/coordinator", coordinator)
	http.HandleFunc("/compiled", compiled)
	http.HandleFunc("/async_sequence", async_sequence)
	http.HandleFunc("/routing_slip", routing_slip)
	http.HandleFunc("/async_coordinator", async_coordinator)
	http.HandleFunc("/event_sourcing", event_sourcing)
	http.HandleFunc("/blackboard", blackboard)
	http.HandleFunc("/message_queue", message_queue)
	http.HandleFunc("/storage", storage_based)
	http.HandleFunc("/workflow_engine", workflow_engine)

	fmt.Printf("Starting server at port 8000\n")
	http.ListenAndServe(":8000", nil)
}
