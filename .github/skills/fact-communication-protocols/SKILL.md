---
name: fact-communication-protocols
description: Identify inter-service communication protocols (HTTP/REST, gRPC, Message Queue, TCP)
---

# Communication Protocols Analysis

## Purpose
Detect communication protocols used for inter-service communication, API exposure, and external integrations.

## Target Files/Locations
- **/pom.xml, **/build.gradle, **/*.csproj, **/package.json (dependencies)
- **/*.proto (gRPC definitions)
- **/application.{properties,yml} (message queue configs)
- **/*.java, **/*.cs, **/*.js (HTTP clients, gRPC stubs)

## Example Patterns
- **HTTP/REST**: RestTemplate, HttpClient, axios, fetch, @RestController
- **gRPC**: grpc-*, *.proto files, gRPC stubs
- **Message Queues**: RabbitMQ, Kafka, Redis Pub/Sub, AWS SQS
- **TCP/UDP**: Socket, ServerSocket, TcpClient
- **WebSocket**: ws://, WebSocket, SignalR

## Analysis Steps

### 1. Check for HTTP/REST
```
Use Grep: "@RestController|@RequestMapping|HttpClient|RestTemplate|axios|fetch"
Files: **/*.{java,cs,js,py}
Context: -B 2 -A 2

Check Spring: @RestController, @GetMapping
Check .NET: HttpClient, [ApiController]
Check Node: express, axios
```

### 2. Check for gRPC
```
Use Glob: **/*.proto
Count proto files

Use Grep: "grpc|GrpcClient|GrpcChannel"
Files: **/*.{java,cs,go,py}
Dependencies: grpc-netty, Grpc.Net.Client, @grpc/grpc-js
```

### 3. Check for Message Queues
```
Use Grep: "RabbitTemplate|KafkaTemplate|@JmsListener|IMessageQueue"
Files: **/*.{java,cs}

Dependencies:
- spring-boot-starter-amqp (RabbitMQ)
- spring-kafka (Kafka)
- MassTransit, NServiceBus (.NET)

Config:
- spring.rabbitmq.*, spring.kafka.*
```

### 4. Check for WebSocket
```
Use Grep: "WebSocket|ws://|wss://|SignalR|@ServerEndpoint"
Files: **/*.{java,cs,js}
```

### 5. Check for TCP/UDP
```
Use Grep: "ServerSocket|Socket|TcpListener|UdpClient"
Files: **/*.{java,cs,go}
```

## Confidence Determination

### High Confidence
- ✅ Multiple protocol indicators found
- ✅ Dependencies + code usage confirmed
- **Example**: "HTTP/REST via Spring MVC, gRPC for internal services (5 .proto files), Kafka for async messaging"

### Medium Confidence
- ⚠️ Dependencies present but usage unclear
- **Example**: "HTTP REST API likely, gRPC dependency but no .proto files found"

### Low Confidence
- ⚠️ Protocol inferred from framework
- **Example**: "Likely HTTP-based (web framework) but protocol not explicit"

### Not Applicable
- ❌ Standalone application with no communication
- **Example**: "CLI tool with no network communication"

## Output Format

```json
{
  "input_name": "Communication Protocols",
  "analysis_method": "LLM",
  "status": "success|not_applicable",
  "result": {
    "finding": "{Protocols summary}",
    "confidence": "high|medium|low",
    "evidence": [
      "{HTTP/REST endpoints}",
      "{gRPC proto files}",
      "{Message queue configs}",
      "{Dependencies}"
    ],
    "values": [
      "{Protocol: HTTP/REST, gRPC, Kafka, RabbitMQ, etc.}",
      "{Framework: Spring MVC, ASP.NET Core, Express}",
      "{Port numbers}",
      "{Count: N endpoints, M proto files}"
    ]
  },
  "execution_time_seconds": {elapsed},
  "timestamp": "{ISO 8601}"
}
```
