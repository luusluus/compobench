package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"

	fs "webserver_proxy/function_sequence"
)

type Message struct {
	Sleep    int      `json:"sleep"`
	Workflow []string `json:"workflow"`
}

func sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)
	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(message)
	status_code := fs.Invoke(b.Bytes())

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
}

func parse_message(req *http.Request) Message {
	var m Message
	err := json.NewDecoder(req.Body).Decode(&m)
	if err != nil {
		fmt.Println(err)
	}
	return m
}

func main() {
	http.HandleFunc("/sequence", sequence)

	fmt.Printf("Starting server at port 8000\n")
	http.ListenAndServe(":8000", nil)
}
