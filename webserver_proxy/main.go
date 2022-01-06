package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	as "webserver_proxy/async_sequence"
	fs "webserver_proxy/function_sequence"
	m "webserver_proxy/message"
)

func sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := fs.Invoke(message)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func async_sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)

	status_code := as.Invoke(message)

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
	http.HandleFunc("/async_sequence", async_sequence)

	fmt.Printf("Starting server at port 8000\n")
	http.ListenAndServe(":8000", nil)
}
