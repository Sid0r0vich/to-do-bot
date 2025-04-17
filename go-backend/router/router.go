package router

import (
    "github.com/gin-gonic/gin"
    "go-backend/handlers"
)

func SetupRouter() *gin.Engine {
    r := gin.Default()

    r.POST("/tasks", handlers.AddTask)
    r.GET("/tasks", handlers.GetTasks)

    return r
}
