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

	err = setupDatabase()
	if err != nil {
		return fmt.Errorf("failed to setup database: %w", err)
	}

	return nil
}

func setupDatabase() error {
	var exists bool
	err := DB.QueryRow("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tasks')").Scan(&exists)
	if err != nil {
		return err
	}

	if !exists {
		_, err = DB.Exec(`
			CREATE TABLE tasks (
				id SERIAL PRIMARY KEY,
				user_id INTEGER NOT NULL,
				text TEXT NOT NULL,
				day INTEGER NOT NULL,
				notify_at TIMESTAMP,
				has_notification BOOLEAN DEFAULT FALSE
			)
		`)
	} else {
		var columnExists bool
		err = DB.QueryRow("SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'tasks' AND column_name = 'notify_at')").Scan(&columnExists)
		if err != nil {
			return err
		}

		if !columnExists {
			_, err = DB.Exec(`
				ALTER TABLE tasks 
				ADD COLUMN notify_at TIMESTAMP,
				ADD COLUMN has_notification BOOLEAN DEFAULT FALSE
			`)
			if err != nil {
				return err
			}
		}
	}

	return err
}
