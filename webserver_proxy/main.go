package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	async "webserver_proxy/async_function"
	m "webserver_proxy/message"
	sync "webserver_proxy/sync_function"
)

func sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := sync.Invoke(message, "SequenceFunctionA")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func compiled(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := sync.Invoke(message, "CompiledFunction")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func coordinator(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := sync.Invoke(message, "CoordinatorFunctionCoordinator")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := async.Invoke(message, "AsyncSequenceFunctionA", "async-sequence-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func routing_slip(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := async.Invoke(message, "RoutingSlipFunctionA", "routing-slip-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_coordinator(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := async.Invoke(message, "AsyncCoordinatorFunctionCoordinator", "async-coordinator-store")

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func parse_message(req *http.Request) m.Message {
	var m m.Message
	err := json.NewDecoder(req.Body).Decode(&m)
	if err != nil {
		fmt.Println(err)
	}
	return m
}

func main() {
	http.HandleFunc("/sequence", sequence)
	http.HandleFunc("/coordinator", coordinator)
	http.HandleFunc("/compiled", compiled)
	http.HandleFunc("/async_sequence", async_sequence)
	http.HandleFunc("/routing_slip", routing_slip)
	http.HandleFunc("/async_coordinator", async_coordinator)

	fmt.Printf("Starting server at port 8000\n")
	http.ListenAndServe(":8000", nil)
}
