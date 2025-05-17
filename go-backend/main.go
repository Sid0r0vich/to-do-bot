package main

import (
	"log"
	"net/http"

	"go-backend/db"
	"go-backend/router"
)

func main() {
	log.Println("Trying to connect PostgreSQL...")
	connectionString := "WRITE TO ARINA TO GET IT"
	log.Println("Connection string:", connectionString)

	err := db.Init(connectionString)
	if err != nil {
		log.Fatalf("ERROR AAAA: %v", err)

	}

	r := router.SetupRouter()
	log.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
