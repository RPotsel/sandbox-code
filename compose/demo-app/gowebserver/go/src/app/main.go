package main

import (
    "os"
    "fmt"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    ws := os.Getenv("WORKSPACE")
    fmt.Fprintf(w, "Hello %s!\nYour HTTP request method is %s\n", ws, r.Method)
}

func main() {
    http.HandleFunc("/", helloHandler)
    http.ListenAndServe(":8080", nil)
}
