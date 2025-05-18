package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"go-backend/db"
	"go-backend/router"
)

func main() {
	port := 8080
	connectionString := os.Getenv("DB_CONNECTION_STRING")

	log.Println("Trying to connect PostgreSQL...")
	log.Println("Connection string:", connectionString)

	err := db.Init(connectionString)
	if err != nil {
		log.Fatalf("ERROR AAAA: %v", err)
	}

	r := router.SetupRouter()
	log.Printf("Server running on http://localhost:%d\n", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), r))
}
