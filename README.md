<h1 align="center">
  <img src="https://via.placeholder.com/120x120/4f46e5/ffffff?text=🔮" alt="QueryGPT" width="120" height="120">
  <br>
  🔮 QueryGPT
  <br>
  <sub>Natural Language to SQL Query Interface</sub>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-19+-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="BigQuery">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Claude_AI-FF6B6B?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude AI">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <strong>🎯 Convert natural language questions into SQL queries using AI</strong>
</p>

---

## 📖 Table of Contents

- [✨ **Features**](#-features)
- [🚀 **Quick Start**](#-quick-start)
- [🏗️ **Architecture**](#️-architecture)
- [🔧 **Configuration**](#-configuration)
- [💻 **Development**](#-development)
- [🐳 **Deployment**](#-deployment)
- [📊 **Usage Examples**](#-usage-examples)
- [🔍 **Troubleshooting**](#-troubleshooting)
- [🤝 **Contributing**](#-contributing)

---

## ✨ Features

- **Natural Language to SQL**: Ask questions in plain English and get SQL queries
- **Multi-Database Support**: Works with BigQuery and PostgreSQL
- **AI-Powered**: Uses Claude AI for intelligent query generation and result explanation
- **Interactive Chat Interface**: User-friendly web interface with conversation history
- **Real-time Results**: Execute queries and see results instantly
- **Schema-Aware**: Understands your database structure for accurate queries
- **Docker Ready**: Easy deployment with Docker Compose

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Anthropic API key for Claude AI
- Database credentials (BigQuery service account or PostgreSQL connection)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/joshuathomas06/QueryGPT.git
   cd QueryGPT
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```bash
   # For BigQuery
   USE_BIGQUERY=true
   BIGQUERY_SERVICE_ACCOUNT_PATH=./bigquery-service-account.json
   BIGQUERY_PROJECT_ID=your-project-id
   
   # For PostgreSQL (if not using BigQuery)
   DATABASE_URL=postgresql://user:password@localhost:5432/database
   
   # AI Configuration
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

3. **Deploy with Docker**
   ```bash
   ./deploy.sh
   ```

4. **Access the application**
   - Frontend: http://localhost
   - API Documentation: http://localhost:8000/docs

---

## 🏗️ Architecture

QueryGPT uses a multi-layer architecture to transform natural language into SQL queries:

<div align="center">

```mermaid
graph TB
    subgraph "🌐 Presentation Layer"
        UI[React TypeScript Frontend<br/>Modern Chat Interface<br/>📱 Port 80]
    end
    
    subgraph "🔧 Application Layer"
        API[FastAPI REST API<br/>Query Processing<br/>⚡ Port 8000]
        ORCH[QueryGPT Orchestrator<br/>Business Logic]
    end
    
    subgraph "🤖 AI Processing Layer"
        CLAUDE[Claude AI API<br/>Natural Language Processing]
        REFINER[ClaudeRefiner<br/>Query Generation & Explanation]
    end
    
    subgraph "📊 Data Processing Layer"  
        INSPECTOR[DatabaseInspector<br/>Schema Analysis & Query Execution]
        SUMMARIZER[SchemaSummarizer<br/>Human-Readable Schema Descriptions]
    end
    
    subgraph "💾 Data Storage Layer"
        DB[(PostgreSQL Database<br/>Cost Analysis Data<br/>🗃️ Port 5432)]
    end
    
    subgraph "🐳 Infrastructure Layer"
        DOCKER[Docker Compose<br/>Container Orchestration]
        NGINX[Nginx Reverse Proxy<br/>Production Serving]
    end
    
    UI -->|HTTP Requests<br/>JSON Payloads| API
    API -->|Orchestrate| ORCH
    ORCH -->|Schema Analysis| INSPECTOR
    ORCH -->|AI Processing| REFINER
    REFINER -->|API Calls| CLAUDE
    INSPECTOR -->|SQL Queries| DB
    SUMMARIZER -->|Schema Formatting| INSPECTOR
    
    DOCKER -->|Container Management| UI
    DOCKER -->|Container Management| API
    DOCKER -->|Container Management| DB
    NGINX -->|Load Balancing| UI
```

</div>

### Request Processing Flow

<div align="center">

```mermaid
sequenceDiagram
    participant User
    participant Frontend as React Frontend
    participant API as FastAPI Backend
    participant QueryGPT as QueryGPT Orchestrator
    participant ClaudeAI as Claude AI
    participant DB as PostgreSQL
    
    User->>Frontend: "What is the total cost by cloud provider?"
    Frontend->>API: POST /query {"question": "..."}
    
    API->>QueryGPT: Process natural language query
    QueryGPT->>DB: Analyze schema if needed
    DB-->>QueryGPT: Schema metadata
    
    QueryGPT->>ClaudeAI: Convert to SQL with schema context
    ClaudeAI-->>QueryGPT: Generated SQL query
    
    QueryGPT->>DB: Execute SQL query
    DB-->>QueryGPT: Query results
    
    QueryGPT->>ClaudeAI: Explain results in human terms
    ClaudeAI-->>QueryGPT: Natural language explanation
    
    QueryGPT-->>API: Complete response object
    API-->>Frontend: JSON response with SQL, results, explanation
    Frontend-->>User: Formatted results with copy buttons
```

</div>

### Project Structure

```
QueryGPT/
├── 🎨 frontend/                     # React TypeScript Application
│   ├── 📂 src/
│   │   ├── App.tsx                  # Main chat interface component
│   │   ├── App.css                  # Dark theme styling with CSS variables
│   │   └── index.tsx               # React application entry point
│   ├── 🐳 Dockerfile               # Frontend containerization
│   ├── ⚙️ nginx.conf               # Production web server config
│   └── 📦 package.json             # Node.js dependencies
├── ⚡ api.py                        # FastAPI REST API server
├── 🧠 query_gpt.py                 # Main orchestrator class
├── 🔍 database_inspector.py        # PostgreSQL connection & schema analysis
├── 📋 schema_summarizer.py         # Human-readable schema descriptions
├── 🤖 claude_refiner.py            # Claude AI integration layer
├── 🐳 docker-compose.yml           # Multi-container orchestration
├── 🚀 deploy.sh                    # Automated deployment script
├── 📊 init.sql                     # Database schema initialization
├── 📋 requirements.txt             # Python package dependencies
└── ⚙️ .env.example                 # Environment configuration template
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# BigQuery Configuration (recommended for production)
USE_BIGQUERY=true
BIGQUERY_SERVICE_ACCOUNT_PATH=./bigquery-service-account.json
BIGQUERY_PROJECT_ID=your-project-id

# PostgreSQL Configuration (alternative to BigQuery)
DATABASE_URL=postgresql://user:password@localhost:5432/database
POSTGRES_DB=querygpt
POSTGRES_USER=querygpt  
POSTGRES_PASSWORD=secure_password_here

# AI Configuration (required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Security Best Practices

1. **Never commit credentials to git**
   - Use `.gitignore` to exclude `.env` and service account files
   - Rotate any accidentally exposed credentials immediately

2. **Use environment variables**
   - Store all sensitive configuration in `.env`
   - Never hardcode API keys or passwords

3. **Limit database permissions**
   - Grant only necessary permissions to service accounts
   - Use read-only access where possible

---

## 💻 Development

### Local Development Setup

**Backend Development**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies  
pip install -r requirements.txt

# Run development server
python api.py
```

**Frontend Development**

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

---

## 🐳 Deployment

### Docker Deployment

1. **Ensure Docker is installed**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Configure environment**
   - Copy `.env.example` to `.env`
   - Add your API keys and database credentials

3. **Run deployment script**
   ```bash
   ./deploy.sh
   ```

### Manual Deployment

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 📊 Usage Examples

### Natural Language Queries

QueryGPT understands various types of questions:

**Basic Queries**
- "How many records are in the database?"
- "What tables are available?"
- "Show me the schema"

**Data Analysis**
- "What's the total cost by cloud provider?"
- "Show monthly spending trends"
- "Which environment has the highest costs?"
- "Top 10 most expensive cost centers"

**Complex Queries**
- "Compare AWS costs between production and development last month"
- "Show me daily costs for GCP in the staging environment"
- "What percentage of total costs is from Azure?"

### Direct SQL Support

You can also write SQL queries directly:
```sql
SELECT cloud_provider, SUM(total_cost) 
FROM demo_table 
GROUP BY cloud_provider 
ORDER BY SUM(total_cost) DESC;
```

---

## 🔍 Troubleshooting

### Common Issues

**1. Container won't start**
```bash
# Check logs
docker-compose logs backend

# Verify .env file exists
ls -la .env
```

**2. Database connection errors**
- Check DATABASE_URL format
- Verify PostgreSQL is running: `docker-compose ps db`
- For BigQuery, ensure service account JSON is valid

**3. API key errors**
- Verify ANTHROPIC_API_KEY is set correctly
- Check for extra spaces or quotes in .env

**4. Frontend can't connect to backend**
- Ensure backend is running on port 8000
- Check CORS settings in api.py

### Debug Commands

```bash
# View all logs
docker-compose logs -f

# Test backend health
curl http://localhost:8000/health

# Test query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many records are there?"}'

# Restart services
docker-compose restart

# Full reset
docker-compose down -v
docker-compose up -d
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write clear, self-documenting code
- Add type hints for Python code
- Follow existing code patterns
- Test your changes thoroughly
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License.

---



</div>
