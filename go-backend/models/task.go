package models

type Task struct {
    ID       int    `json:"id"`
    UserID   int    `json:"user_id"`
    Text     string `json:"text"`
    Day      int    `json:"day"`
}
