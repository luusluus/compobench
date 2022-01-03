package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strconv"
)

type Message struct {
	Sleep    int      `json:"sleep"`
	Workflow []string `json:"workflow"`
}

func sequence(w http.ResponseWriter, req *http.Request) {
	message := parse_message(req)
	cmd := exec.Command("python", "../compositions/function_sequence/client.py", strconv.Itoa(message.Sleep))
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println(err)
	}
	status_code := parse_python_response(out)
	fmt.Println(status_code)

	w.WriteHeader(status_code)
	w.Header().Set("Content-Type", "application/json")
	return
}

func parse_message(req *http.Request) Message {
	var m Message
	err := json.NewDecoder(req.Body).Decode(&m)
	if err != nil {
		fmt.Println(err)
	}
	return m
}

func parse_python_response(response []byte) int {
	out_string := string(response)
	// remove new line
	status_code, err := strconv.Atoi(out_string[:len(out_string)-1])
	if err != nil {
		fmt.Println(err)
	}
	return status_code
}

func main() {

	http.HandleFunc("/sequence", sequence)

	http.ListenAndServe(":8000", nil)
}
