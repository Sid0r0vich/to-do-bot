package models

import "time"

type Task struct {
	ID              int       `json:"id"`
	UserID          int       `json:"user_id"`
	Text            string    `json:"text"`
	Day             int       `json:"day"`
	NotifyAt        time.Time `json:"notify_at,omitempty"`
	HasNotification bool      `json:"has_notification"`
}
