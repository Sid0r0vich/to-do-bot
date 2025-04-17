package handlers

import (
	"go-backend/db"
	"go-backend/models"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func AddTask(c *gin.Context) {
	var task models.Task
	if err := c.ShouldBindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	query := `INSERT INTO tasks (user_id, text, day) VALUES ($1, $2, $3) RETURNING id`
	err := db.DB.QueryRow(query, task.UserID, task.Text, task.Day).Scan(&task.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, task)
}

func GetTasks(c *gin.Context) {
	userID, _ := strconv.Atoi(c.Query("user_id"))
	day, _ := strconv.Atoi(c.Query("day"))
	rows, err := db.DB.Query("SELECT id, text FROM tasks WHERE user_id=$1 AND day=$2", userID, day)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	var tasks []models.Task
	for rows.Next() {
		var task models.Task
		rows.Scan(&task.ID, &task.Text)
		tasks = append(tasks, task)
	}

	c.JSON(http.StatusOK, tasks)
}
