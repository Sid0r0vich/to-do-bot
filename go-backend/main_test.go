package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

type Task struct {
	ID       int       `json:"id"`
	UserID   int       `json:"user_id"`
	Text     string    `json:"text"`
	Day      int       `json:"day"`
	NotifyAt time.Time `json:"notify_at"`
}

type MockDB struct {
	tasks []Task
}

func (db *MockDB) AddTask(task Task) int {
	task.ID = 1
	db.tasks = append(db.tasks, task)
	return task.ID
}

func (db *MockDB) GetTasks(userID, day int) []Task {
	return db.tasks
}

func SetupRouter(db *MockDB) *gin.Engine {
	r := gin.Default()

	r.POST("/tasks", func(c *gin.Context) {
		var task Task
		if err := c.BindJSON(&task); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid JSON"})
			return
		}
		db.AddTask(task)
		c.JSON(http.StatusOK, gin.H{"id": task.ID})
	})

	r.GET("/tasks", func(c *gin.Context) {
		c.JSON(http.StatusOK, db.GetTasks(0, 0))
	})

	return r
}

func TestAddAndGetTask(t *testing.T) {
	db := &MockDB{}
	r := SetupRouter(db)

	task := map[string]interface{}{
		"user_id":   1,
		"text":      "Test task",
		"day":       1,
		"notify_at": time.Now().Add(time.Hour).Format(time.RFC3339),
	}

	body, _ := json.Marshal(task)

	req := httptest.NewRequest(http.MethodPost, "/tasks", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	req = httptest.NewRequest(http.MethodGet, "/tasks", nil)
	w = httptest.NewRecorder()
	r.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var tasks []Task
	json.Unmarshal(w.Body.Bytes(), &tasks)
	assert.Equal(t, 1, len(tasks))
	assert.Equal(t, "Test task", tasks[0].Text)
}
