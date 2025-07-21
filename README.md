<h1 align="center">
  <img src="https://via.placeholder.com/120x120/4f46e5/ffffff?text=🔮" alt="QueryGPT" width="120" height="120">
  <br>
  🔮 QueryGPT: Complete Developer's Guide
  <br>
  <sub>Natural Language to SQL with AI - Deep Dive Implementation</sub>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-19+-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Claude_AI-FF6B6B?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude AI">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <strong>🎯 A complete walkthrough of building an AI-powered database query interface from scratch</strong>
</p>

---

## 📖 Table of Contents

- [🏗️ **System Architecture Deep Dive**](#️-system-architecture-deep-dive)
- [🔄 **Data Flow Walkthrough**](#-data-flow-walkthrough)
- [🧩 **Component Architecture**](#-component-architecture)
- [📝 **Code Implementation Guide**](#-code-implementation-guide)
- [🚀 **Quick Start**](#-quick-start)
- [🎨 **Frontend Implementation**](#-frontend-implementation)
- [⚡ **Backend Implementation**](#-backend-implementation)
- [🤖 **AI Integration**](#-ai-integration)
- [💾 **Database Layer**](#-database-layer)
- [🐳 **Deployment Architecture**](#-deployment-architecture)
- [🔧 **Configuration Management**](#-configuration-management)
- [🛠️ **Development Workflow**](#️-development-workflow)

---

## 🏗️ System Architecture Deep Dive

### 🎯 **High-Level System Overview**

QueryGPT transforms natural language questions into SQL queries using a sophisticated multi-layer architecture:

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

### 🔄 **Request Processing Flow**

Here's exactly what happens when a user asks a question:

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

---

## 🧩 Component Architecture

### 📁 **Project Structure Walkthrough**

```
my-claude-project/
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

## 📝 Code Implementation Guide

### 🎯 **Core Architecture Pattern: Orchestrator Pattern**

QueryGPT uses the **Orchestrator Pattern** where `QueryGPT` class coordinates between different specialized components:

```python
# query_gpt.py - The main orchestrator
class QueryGPT:
    def __init__(self, database_url: str = None, anthropic_api_key: str = None):
        # Initialize specialized components
        self.db_inspector = DatabaseInspector(database_url)      # Database operations
        self.summarizer = SchemaSummarizer()                     # Schema formatting  
        self.refiner = ClaudeRefiner(anthropic_api_key)          # AI integration
```

**Why this pattern?** 
- **Separation of Concerns**: Each component handles one responsibility
- **Testability**: Components can be unit tested independently
- **Scalability**: Easy to swap implementations (e.g., different AI models)
- **Maintainability**: Changes in one component don't affect others

---

## 🎨 Frontend Implementation

### 🔧 **React Architecture: Component Composition**

The frontend uses a **single-page application (SPA)** pattern with state management through React hooks:

```typescript
// frontend/src/App.tsx - Main application component
interface QueryResult {
  sql_query: string;
  results: Array<Record<string, any>>;
  explanation: string;
  success: boolean;
  error?: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  result?: QueryResult;
}

function App() {
  // State management for chat interface
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [history, setHistory] = useState<QueryResult[]>([]);
  
  // ... component logic
}
```

### 🎨 **CSS Architecture: Design System Approach**

The styling uses **CSS Custom Properties** for consistent theming:

```css
/* frontend/src/App.css - Design system variables */
:root {
  --bg-primary: #212121;        /* Main background */
  --bg-secondary: #2a2a2a;      /* Card backgrounds */
  --bg-tertiary: #303030;       /* Hover states */
  --text-primary: #ffffff;      /* Main text */
  --text-secondary: #d1d5db;    /* Secondary text */
  --accent-color: #10a37f;      /* Brand color */
  --border-color: #444444;      /* Borders and dividers */
}
```

**Benefits of this approach:**
- **Consistent theming** across all components
- **Easy theme switching** (light/dark mode)
- **Maintainable** color scheme updates
- **Scalable** design system

### 📱 **Responsive Design Pattern**

The interface adapts to different screen sizes using CSS Grid and Flexbox:

```css
.examples-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2 columns on desktop */
  gap: 0.75rem;
}

@media (max-width: 768px) {
  .examples-container {
    grid-template-columns: 1fr;  /* 1 column on mobile */
  }
}
```

---

## ⚡ Backend Implementation

### 🚀 **FastAPI Architecture: Async API Design**

The backend uses **FastAPI's async capabilities** for high-performance request handling:

```python
# api.py - FastAPI application setup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="QueryGPT API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]
    explanation: str
    success: bool
    error: Optional[str] = None
```

### 🔄 **Request Processing Logic**

Here's the complete request processing flow in the API:

```python
@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        question = request.question.strip()
        
        # Step 1: Determine if input is SQL or natural language
        if query_gpt.is_sql_query(question):
            sql_query = question  # Use SQL directly
        else:
            # Step 2: Convert natural language to SQL using Claude
            sql_query = query_gpt.refiner.convert_natural_language_to_sql(
                question, query_gpt.schema_summary
            )
        
        # Step 3: Execute query and get explanation
        results, explanation = query_gpt.execute_and_explain_query(
            sql_query, query_gpt.schema_summary
        )
        
        # Step 4: Return structured response
        return QueryResponse(
            sql_query=sql_query,
            results=results,
            explanation=explanation,
            success=True
        )
    except Exception as e:
        return QueryResponse(
            sql_query="",
            results=[],
            explanation=f"Internal server error: {str(e)}",
            success=False,
            error=str(e)
        )
```

---

## 🤖 AI Integration

### 🧠 **Claude AI Integration Architecture**

The `ClaudeRefiner` class abstracts all AI interactions:

```python
# claude_refiner.py - AI integration layer
import anthropic

class ClaudeRefiner:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def convert_natural_language_to_sql(self, natural_query: str, schema_context: str) -> str:
        """Convert natural language to SQL with contextual awareness"""
        prompt = f"""
Given this database schema context:
{schema_context}

Convert this natural language query to SQL:
"{natural_query}"

Important guidelines:
1. Generate a valid PostgreSQL query
2. Use proper table and column names from the schema
3. For aggregations, use GROUP BY appropriately
4. Include appropriate JOINs if needed
5. Order results logically

Return ONLY the SQL query, no explanations.
        """
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
```

### 🎯 **Prompt Engineering Strategy**

The prompts are carefully engineered for optimal results:

1. **Context-Aware**: Include database schema in every prompt
2. **Specific Instructions**: Clear guidelines for SQL generation
3. **Error Prevention**: Instructions to avoid common SQL mistakes
4. **Consistent Output**: Structured response format requirements

---

## 💾 Database Layer

### 🔍 **Database Inspector: Schema Analysis**

The `DatabaseInspector` provides database connectivity and schema introspection:

```python
# database_inspector.py - Database operations
import psycopg
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class TableInfo:
    name: str
    columns: List[Tuple[str, str]]  # (column_name, data_type)

class DatabaseInspector:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv('DATABASE_URL')
    
    def get_full_schema(self) -> List[TableInfo]:
        """Get complete schema information for all tables"""
        table_names = self.get_table_names()
        tables = []
        
        for table_name in table_names:
            columns = self.get_table_schema(table_name)
            tables.append(TableInfo(name=table_name, columns=columns))
        
        return tables
    
    def execute_query(self, query: str) -> List[Dict]:
        """Execute SQL query and return results as dictionaries"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
```

### 📋 **Schema Summarizer: Human-Readable Descriptions**

The `SchemaSummarizer` converts technical database schemas into readable descriptions:

```python
# schema_summarizer.py - Schema formatting
class SchemaSummarizer:
    @staticmethod
    def format_data_type(data_type: str) -> str:
        """Convert PostgreSQL data types to human-readable format"""
        type_mapping = {
            'integer': 'whole number',
            'numeric': 'decimal number',
            'character varying': 'text',
            'timestamp': 'date and time',
            'boolean': 'true/false',
            'date': 'date'
        }
        return type_mapping.get(data_type.lower(), data_type)
    
    @staticmethod
    def summarize_schema(tables: List[TableInfo]) -> str:
        """Generate human-friendly summary of the entire schema"""
        summary = f"Database contains {len(tables)} tables:\n\n"
        
        for table in tables:
            summary += f"**{table.name}** table:\n"
            for column_name, data_type in table.columns:
                readable_type = SchemaSummarizer.format_data_type(data_type)
                summary += f"  - {column_name}: {readable_type}\n"
            summary += "\n"
        
        return summary.strip()
```

### 📊 **Sample Database Schema**

The application comes with a cloud cost analysis schema:

```sql
-- init.sql - Database initialization
CREATE TABLE IF NOT EXISTS demo_table (
    id SERIAL PRIMARY KEY,
    account_id TEXT,              -- Cloud account identifier
    cloud_provider TEXT,          -- AWS, Azure, GCP
    environment TEXT,             -- prod, dev, staging
    subtag TEXT,                  -- Additional categorization
    usage_date DATE,              -- Cost date
    total_cost NUMERIC(15,8),     -- Cost amount with precision
    tag TEXT,                     -- Resource tags
    cost_category TEXT,           -- Cost classification
    cloudprovider_category TEXT,  -- Provider-specific category
    cost_center TEXT,             -- Business unit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_demo_table_date ON demo_table(usage_date);
CREATE INDEX IF NOT EXISTS idx_demo_table_provider ON demo_table(cloud_provider);
CREATE INDEX IF NOT EXISTS idx_demo_table_environment ON demo_table(environment);
```

---

## 🐳 Deployment Architecture

### 📦 **Docker Compose Orchestration**

The application uses a **multi-container architecture** for production deployment:

```yaml
# docker-compose.yml - Container orchestration
version: '3.8'

services:
  # Backend API service
  backend:
    build: .
    container_name: querygpt-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - db

  # Frontend web service  
  frontend:
    build: ./frontend
    container_name: querygpt-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s

  # PostgreSQL database
  db:
    image: postgres:15
    container_name: querygpt-db
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-querygpt}
      - POSTGRES_USER=${POSTGRES_USER:-querygpt}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-querygpt}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-querygpt}"]
      interval: 30s
```

### 🚀 **Automated Deployment Script**

The `deploy.sh` script provides **one-command deployment**:

```bash
#!/bin/bash
# deploy.sh - Production deployment automation

set -e  # Exit on any error

echo "🚀 Starting QueryGPT deployment..."

# Step 1: Validate environment
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

# Step 2: Check dependencies
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker not installed"
    exit 1
fi

# Step 3: Build and start services
echo "🔨 Building Docker containers..."
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

# Step 4: Health checks
echo "🔍 Checking service health..."
sleep 30

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    exit 1
fi

echo "🎉 QueryGPT is now running!"
echo "🌐 Frontend: http://localhost"
echo "🔗 Backend API: http://localhost:8000"
```

---

## 🚀 Quick Start

### 🎯 **One-Command Setup**

```bash
# Clone the repository
git clone <your-repository-url>
cd my-claude-project

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# ANTHROPIC_API_KEY=your_key_here

# Deploy everything
./deploy.sh
```

### 🌐 **Access Your Application**

<div align="center">

[![Frontend](https://img.shields.io/badge/🌐_Frontend-http://localhost-4CAF50?style=for-the-badge)](http://localhost)
[![API](https://img.shields.io/badge/⚡_API-http://localhost:8000-FF9800?style=for-the-badge)](http://localhost:8000)
[![Docs](https://img.shields.io/badge/📚_API_Docs-http://localhost:8000/docs-2196F3?style=for-the-badge)](http://localhost:8000/docs)

</div>

---

## 🔧 Configuration Management

### ⚙️ **Environment Variables**

Create a `.env` file for configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://querygpt:querygpt@db:5432/querygpt
POSTGRES_DB=querygpt
POSTGRES_USER=querygpt  
POSTGRES_PASSWORD=secure_password_here

# AI Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### 🔒 **Security Configuration**

```python
# Built-in security measures
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],            # Limit HTTP methods
    allow_headers=["*"],
)

# Input validation
class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)  # Length limits
```

---

## 🛠️ Development Workflow

### 🔄 **Local Development Setup**

#### Backend Development
```bash
# 1. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
export ANTHROPIC_API_KEY="your-key-here"

# 4. Run development server
python api.py
```

#### Frontend Development
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node.js dependencies
npm install

# 3. Start development server (with hot reload)
npm start

# 4. Open browser to http://localhost:3000
```

### 🧪 **Testing Strategy**

```bash
# Backend testing
python -m pytest tests/ -v

# Frontend testing  
cd frontend
npm test

# Integration testing
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 📊 Performance Optimization

### ⚡ **Database Query Optimization**

```sql
-- Optimized indexes for common queries
CREATE INDEX CONCURRENTLY idx_demo_table_provider_date 
ON demo_table(cloud_provider, usage_date);

CREATE INDEX CONCURRENTLY idx_demo_table_cost_center_date 
ON demo_table(cost_center, usage_date) 
WHERE total_cost > 0;
```

### 🎯 **Frontend Performance**

```typescript
// React optimization with useMemo and useCallback
const expensiveCalculation = useMemo(() => {
  return processLargeResultSet(results);
}, [results]);

const handleSubmit = useCallback(async (e: React.FormEvent) => {
  // Optimized submit handler
}, [question, loading]);
```

### 🤖 **AI Response Caching**

```python
# Cache frequently used schema summaries
@lru_cache(maxsize=100)
def get_cached_schema_summary(schema_hash: str) -> str:
    return self.refiner.refine_schema_summary(schema_content)
```

---

## 🔍 Troubleshooting Guide

### 🐛 **Common Issues & Solutions**

<div align="center">

```mermaid
flowchart TD
    START[Application Issue] --> CHECK_LOGS{Check Logs}
    
    CHECK_LOGS -->|Backend Error| BACKEND[Backend Issues]
    CHECK_LOGS -->|Frontend Error| FRONTEND[Frontend Issues]  
    CHECK_LOGS -->|Database Error| DATABASE[Database Issues]
    
    BACKEND --> API_KEY{API Key Valid?}
    API_KEY -->|No| FIX_API[Update ANTHROPIC_API_KEY]
    API_KEY -->|Yes| DB_CONN{DB Connected?}
    DB_CONN -->|No| FIX_DB[Check DATABASE_URL]
    DB_CONN -->|Yes| RESTART[Restart Backend]
    
    FRONTEND --> CORS{CORS Error?}
    CORS -->|Yes| FIX_CORS[Check Backend URL in Frontend]
    CORS -->|No| BUILD[npm run build]
    
    DATABASE --> PORT{Port Conflict?}
    PORT -->|Yes| CHANGE_PORT[Modify docker-compose.yml ports]
    PORT -->|No| RESET_DB[docker-compose down -v]
    
    FIX_API --> RESTART_FULL[docker-compose restart]
    FIX_DB --> RESTART_FULL
    FIX_CORS --> RESTART_FULL
    BUILD --> RESTART_FULL
    CHANGE_PORT --> RESTART_FULL
    RESET_DB --> RESTART_FULL
    RESTART --> RESTART_FULL
    
    RESTART_FULL --> TEST[Test Application]
    TEST --> SUCCESS[✅ Working!]
```

</div>

### 📋 **Debug Commands**

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend  
docker-compose logs -f db

# Database debugging
docker-compose exec db psql -U querygpt -d querygpt -c "\dt"

# Backend health check
curl -X GET http://localhost:8000/health

# Test API endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "SELECT COUNT(*) FROM demo_table"}'
```

---

## 🎯 Advanced Usage Examples

### 💰 **Cloud Cost Analysis Queries**

Try these natural language queries to explore the cost data:

<table>
<tr>
<td width="50%">

**📊 Basic Analytics**
```
"How many records are in the database?"
"What cloud providers do we use?"  
"Show me all unique environments"
"What's the date range of our data?"
```

</td>
<td width="50%">

**💸 Cost Analysis**
```
"Total cost by cloud provider this month"
"Which environment costs the most?"
"Show AWS costs grouped by category"
"Top 10 most expensive cost centers"
```

</td>
</tr>
<tr>
<td>

**📈 Time-based Analysis** 
```
"Daily costs for the last 30 days"
"Month-over-month cost comparison"
"Costs trending up or down?"
"Highest cost days this quarter"
```

</td>
<td>

**🔍 Detailed Breakdowns**
```
"AWS costs by service category"
"Production vs development costs"
"Cost per account by provider"
"Resource tags with highest costs"
```

</td>
</tr>
</table>

### 🔍 **Generated SQL Examples**

<details>
<summary><strong>💡 See SQL translations</strong></summary>

| Natural Language | Generated SQL |
|------------------|---------------|
| "Total cost by provider" | `SELECT cloud_provider, SUM(total_cost) as total FROM demo_table GROUP BY cloud_provider ORDER BY total DESC;` |
| "Monthly cost trends" | `SELECT DATE_TRUNC('month', usage_date) as month, SUM(total_cost) FROM demo_table GROUP BY month ORDER BY month;` |
| "AWS production costs" | `SELECT SUM(total_cost) FROM demo_table WHERE cloud_provider = 'AWS' AND environment = 'prod';` |
| "Top cost centers" | `SELECT cost_center, SUM(total_cost) as total FROM demo_table GROUP BY cost_center ORDER BY total DESC LIMIT 10;` |

</details>

---

## 🤝 Contributing

### 📋 **Development Guidelines**

```bash
# 1. Fork and clone
git clone https://github.com/your-username/querygpt.git
cd querygpt

# 2. Create feature branch
git checkout -b feature/amazing-new-feature

# 3. Make changes following these principles:
#    - Write self-documenting code
#    - Add type hints for Python
#    - Use TypeScript for React components
#    - Follow existing code patterns
#    - Add tests for new functionality

# 4. Test your changes
npm test                    # Frontend tests
python -m pytest          # Backend tests  
./deploy.sh               # Integration test

# 5. Submit pull request
git push origin feature/amazing-new-feature
```

### 🏗️ **Architecture Principles**

- **Single Responsibility**: Each class/function has one job
- **Dependency Injection**: Components receive dependencies  
- **Interface Segregation**: Small, focused interfaces
- **Error Handling**: Graceful error recovery
- **Security First**: Input validation and sanitization

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🌟 **Built with ❤️ for developers who love clean architecture**

<p>
  <a href="https://github.com/your-username/querygpt/stargazers">
    <img src="https://img.shields.io/github/stars/your-username/querygpt?style=social" alt="GitHub stars">
  </a>
  <a href="https://github.com/your-username/querygpt/network/members">  
    <img src="https://img.shields.io/github/forks/your-username/querygpt?style=social" alt="GitHub forks">
  </a>
  <a href="https://github.com/your-username/querygpt/watchers">
    <img src="https://img.shields.io/github/watchers/your-username/querygpt?style=social" alt="GitHub watchers">
  </a>
</p>

**[⭐ Star this repository](https://github.com/your-username/querygpt) if you found this walkthrough helpful!**

---

*🚀 Built with [Claude AI](https://claude.ai) • [FastAPI](https://fastapi.tiangolo.com) • [React](https://reactjs.org) • [PostgreSQL](https://postgresql.org) • [Docker](https://docker.com)*

</div>