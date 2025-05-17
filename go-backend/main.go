package main

import (
	"fmt"
	"log"
	"net/http"

	"go-backend/db"
	"go-backend/router"
)

func main() {
	port := 8080
	// os.Setenv("DB_CONNECTION_STRING", "user=postgres password=secret dbname=tasksdb sslmode=disable")

	log.Println("Trying to connect PostgreSQL...")
	connectionString := "user=postgres password=secret dbname=tasksdb host=db port=5432 sslmode=disable"
	log.Println("Connection string:", connectionString)

	err := db.Init(connectionString)
	if err != nil {
		log.Fatalf("ERROR AAAA: %v", err)
	}

	r := router.SetupRouter()
	log.Printf("Server running on http://localhost:%d\n", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf("0.0.0.0:%d", port), r))
}
