package handlers

import (
	"database/sql"
	"go-backend/db"
	"go-backend/models"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

func AddTask(c *gin.Context) {
	var task models.Task
	if err := c.ShouldBindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var query string
	var err error

	if !task.NotifyAt.IsZero() {
		query = `INSERT INTO tasks (user_id, text, day, notify_at, has_notification)
				VALUES ($1, $2, $3, $4, $5) RETURNING id`
		err = db.DB.QueryRow(query, task.UserID, task.Text, task.Day,
			task.NotifyAt, true).Scan(&task.ID)
	} else {
		query = `INSERT INTO tasks (user_id, text, day) VALUES ($1, $2, $3) RETURNING id`
		err = db.DB.QueryRow(query, task.UserID, task.Text, task.Day).Scan(&task.ID)
	}

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, task)
}

func GetTasks(c *gin.Context) {
	userID, _ := strconv.Atoi(c.Query("user_id"))
	day, _ := strconv.Atoi(c.Query("day"))
	rows, err := db.DB.Query(
		`SELECT id, text, notify_at, has_notification FROM tasks 
		WHERE user_id=$1 AND day=$2`, userID, day)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	var tasks []models.Task
	for rows.Next() {
		var task models.Task
		var notifyAt sql.NullTime

		err := rows.Scan(&task.ID, &task.Text, &notifyAt, &task.HasNotification)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		task.UserID = userID
		task.Day = day

		if notifyAt.Valid {
			task.NotifyAt = notifyAt.Time
		}

		tasks = append(tasks, task)
	}

	c.JSON(http.StatusOK, tasks)
}

func GetPendingNotifications(c *gin.Context) {
	currentTime := time.Now()

	rows, err := db.DB.Query(`
		SELECT id, user_id, text, day, notify_at 
		FROM tasks 
		WHERE has_notification = true 
		AND notify_at <= $1 
		AND notify_at > $2`,
		currentTime.Add(time.Minute), currentTime.Add(-time.Minute))

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	var tasks []models.Task
	for rows.Next() {
		var task models.Task
		var notifyAt sql.NullTime

		err := rows.Scan(&task.ID, &task.UserID, &task.Text, &task.Day, &notifyAt)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		if notifyAt.Valid {
			task.NotifyAt = notifyAt.Time
			task.HasNotification = true
		}

		tasks = append(tasks, task)
	}

	c.JSON(http.StatusOK, tasks)
}

func MarkNotificationSent(c *gin.Context) {
	taskID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid task ID"})
		return
	}

	_, err = db.DB.Exec(`
		UPDATE tasks 
		SET has_notification = false 
		WHERE id = $1`, taskID)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": "success"})
}
