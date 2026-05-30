FROM golang:1.24 AS builder

WORKDIR /app
COPY . .

# tải package
RUN go mod tidy

# build từ thư mục cmd (vì main.go/runner.go nằm trong đó)
RUN CGO_ENABLED=0 GOOS=linux go build -o chall ./cmd

FROM alpine:latest
WORKDIR /app

COPY --from=builder /app/chall .

EXPOSE 3000
CMD ["./chall"]

