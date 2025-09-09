package router

import (
	"go-backend/handlers"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	r := gin.Default()

	r.POST("/tasks", handlers.AddTask)
	r.GET("/tasks", handlers.GetTasks)

	r.GET("/notifications/pending", handlers.GetPendingNotifications)
	r.POST("/notifications/:id/mark-sent", handlers.MarkNotificationSent)

	return r
}
