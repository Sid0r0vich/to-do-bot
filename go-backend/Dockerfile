FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o main main.go
FROM alpine:latest
RUN apk add --no-cache postgresql-client
WORKDIR /app
COPY --from=builder /app/main .
CMD ["./main"]