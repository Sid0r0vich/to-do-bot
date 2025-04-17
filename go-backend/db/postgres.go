package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

var DB *sql.DB

func Init(connectionString string) error {
	var err error
	DB, err = sql.Open("postgres", connectionString)
	if err != nil {
		return fmt.Errorf("failed to connect to database: %w", err)
	}

	if err = DB.Ping(); err != nil {
		return fmt.Errorf("cannot reach database: %w", err)
	}

	log.Println("Postgres connected")
	return nil
}
