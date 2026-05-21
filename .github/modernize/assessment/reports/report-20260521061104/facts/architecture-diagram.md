# Architecture Diagram

This document summarizes the Photo Album application's runtime structure and the main component relationships that support photo upload, gallery browsing, image retrieval, and deletion.

## Application Architecture

```mermaid
flowchart TD
    subgraph Client["Client Layer"]
        Browser["Web Browser"]
    end

    subgraph App["Application Layer - Spring Boot 2.7"]
        Views["Thymeleaf Views"]
        UploadJs["Upload JavaScript"]
        HomeCtrl["HomeController"]
        DetailCtrl["DetailController"]
        FileCtrl["PhotoFileController"]
        PhotoSvc["PhotoServiceImpl"]
    end

    subgraph Data["Data Layer"]
        PhotoRepo["Spring Data JPA Repository"]
        OracleDB[("Oracle Database PHOTOS table")]
    end

    subgraph External["External Services"]
        BootstrapCdn["Bootstrap CDN"]
        OracleContainer["Oracle DB Container"]
    end

    Browser -->|"Loads gallery and detail pages"| Views
    Browser -->|"Drag and drop uploads"| UploadJs
    Views -->|"GET / and GET /detail/{id}"| HomeCtrl
    Views -->|"Photo detail navigation and delete"| DetailCtrl
    UploadJs -->|"POST /upload"| HomeCtrl
    Browser -->|"GET /photo/{id}"| FileCtrl
    HomeCtrl -->|"List and create photo records"| PhotoSvc
    DetailCtrl -->|"Lookup, navigate, delete"| PhotoSvc
    FileCtrl -->|"Load BLOB content"| PhotoSvc
    PhotoSvc -->|"CRUD and custom queries"| PhotoRepo
    PhotoRepo -->|"SQL and BLOB persistence"| OracleDB
    OracleContainer -->|"Hosts"| OracleDB
    Browser -->|"Fetches UI assets"| BootstrapCdn
```

### Technology Stack Summary

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Presentation | Thymeleaf templates, Bootstrap, vanilla JavaScript | Thymeleaf via Spring Boot 2.7.18, Bootstrap 5.3.0 | Renders gallery/detail pages and handles drag-and-drop uploads |
| Web | Spring Boot Web, Spring MVC | 2.7.18 | Handles HTTP requests and server-side page composition |
| Business Logic | PhotoServiceImpl | Application code | Validates uploads, extracts metadata, coordinates persistence |
| Data Access | Spring Data JPA, Hibernate | Spring Boot managed | Maps the Photo entity to Oracle and executes repository queries |
| Storage | Oracle Database Free/XE | Container image latest / XE-compatible JDBC URL | Stores photo metadata and image BLOB data |
| Delivery | Docker, Docker Compose | Dockerfile + compose | Runs the web app and Oracle database as containers |

### Data Storage & External Services

The application stores all photo metadata and binary image content in a single Oracle database table named `PHOTOS`. Beyond the database, the only notable external dependency at runtime is the Bootstrap CDN used by the server-rendered UI for styling and client-side bundle delivery.

### Key Architectural Decisions

- Uses a classic layered Spring MVC design where controllers delegate all business logic and persistence orchestration to a single `PhotoServiceImpl` service.
- Persists uploaded images as Oracle BLOB data instead of filesystem storage, which keeps the application stateless from a file-hosting perspective.
- Uses server-rendered Thymeleaf pages for navigation while enhancing uploads with client-side JavaScript for drag-and-drop and immediate gallery updates.

## Component Relationships

```mermaid
flowchart LR
    subgraph Presentation["Presentation"]
        IndexView["index.html"]
        DetailView["detail.html"]
        UploadClient["upload.js"]
        HomeControllerNode["HomeController"]
        DetailControllerNode["DetailController"]
        PhotoFileControllerNode["PhotoFileController"]
    end

    subgraph Business["Business Logic"]
        PhotoServiceNode["PhotoService"]
        PhotoServiceImplNode["PhotoServiceImpl"]
        UploadResultNode["UploadResult"]
    end

    subgraph DataAccess["Data Access"]
        PhotoRepoNode["PhotoRepository"]
        PhotoEntityNode["Photo Entity"]
    end

    subgraph Infra["Infrastructure"]
        SpringBootNode["Spring Boot Runtime"]
        TxNode["Transactional Boundary"]
        OracleNode["Oracle Database"]
    end

    IndexView -->|"submits uploads to"| UploadClient
    IndexView -->|"binds model data from"| HomeControllerNode
    DetailView -->|"binds model data from"| DetailControllerNode
    UploadClient -->|"calls"| HomeControllerNode
    HomeControllerNode -->|"delegates"| PhotoServiceNode
    DetailControllerNode -->|"delegates"| PhotoServiceNode
    PhotoFileControllerNode -->|"delegates"| PhotoServiceNode
    PhotoServiceNode -->|"implemented by"| PhotoServiceImplNode
    PhotoServiceImplNode -->|"returns"| UploadResultNode
    PhotoServiceImplNode -->|"queries and saves"| PhotoRepoNode
    PhotoRepoNode -->|"maps"| PhotoEntityNode
    PhotoRepoNode -->|"executes against"| OracleNode
    SpringBootNode -.->|"creates and wires"| Presentation
    TxNode -.->|"wraps service methods"| PhotoServiceImplNode
```

### Component Inventory

| Component | Layer | Type | Responsibility |
|---|---|---|---|
| `index.html` | Presentation | Thymeleaf template | Displays the gallery, upload area, and flash/error messages |
| `detail.html` | Presentation | Thymeleaf template | Shows a single photo, metadata, navigation, and delete action |
| `upload.js` | Presentation | Browser script | Validates dropped files, posts multipart uploads, and prepends new cards to the gallery |
| `HomeController` | Presentation | MVC controller | Handles gallery rendering and upload responses |
| `DetailController` | Presentation | MVC controller | Handles detail page rendering and delete operations |
| `PhotoFileController` | Presentation | MVC controller | Streams image bytes with cache-control headers |
| `PhotoServiceImpl` | Business Logic | Service | Applies upload rules, extracts image dimensions, and coordinates CRUD operations |
| `PhotoRepository` | Data Access | Spring Data repository | Executes Oracle-specific native SQL for ordered listing and navigation |
| `Photo` | Data Access | JPA entity | Represents persisted photo metadata and BLOB content |
