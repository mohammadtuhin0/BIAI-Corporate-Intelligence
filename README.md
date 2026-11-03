
# BIAI Corporate Intelligence

An AI-powered Corporate Sales CRM and Business Intelligence platform built for the **BIAI AI Internship Round 2 Challenge**.

The application helps businesses manage corporate leads, monitor sales pipelines, identify data quality issues, track follow-ups, and generate AI-powered business insights using Google Gemini.

## Project Overview

BIAI Corporate Intelligence transforms raw corporate lead data into actionable business intelligence through an integrated CRM dashboard.

It combines traditional data analytics, sales management, automated validation, and generative AI in one application.

## Key Features

### 1. Dashboard & Analytics
- Total leads and deal value overview.
- Sales stage distribution.
- Industry-wise lead analytics.
- Follow-up summaries.
- Overdue and upcoming follow-up tracking.

### 2. Lead Management
- Create new leads.
- View and search existing leads.
- Update lead information.
- Delete leads.
- Manage sales stages.

### 3. Sales Pipeline
- Monitor leads across sales stages.
- Filter leads by industry and stage.
- Analyze deal values.
- Visualize sales pipeline performance.

### 4. Data Quality Management
- Missing information detection.
- Email and phone validation.
- Duplicate company and contact detection.
- Invalid date sequence detection.
- Overdue follow-up identification.
- Data quality reports and CSV export.

### 5. AI Business Assistant
Powered by Google Gemini API.

- AI-generated business summaries.
- Follow-up recommendations.
- Important lead insights.
- Natural-language business queries.
- CRM-aware business analysis.

**Privacy consideration:** The AI service sends selected business fields to Gemini. Contact names, emails, phone numbers, and notes are excluded from the AI context.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing |
| Plotly | Data visualization |
| SQLite | Database |
| Google Gemini API | AI-powered business intelligence |
| Pytest | Automated testing |
| python-dotenv | Environment configuration |

## Project Architecture

```text
biai-corporate-intelligence/
│
├── app.py
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── lead_repository.py
│
├── services/
│   ├── data_loader.py
│   ├── import_service.py
│   ├── lead_service.py
│   ├── validation_service.py
│   ├── analytics_service.py
│   └── ai_service.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Sales_Pipeline.py
│   ├── 3_Lead_Management.py
│   ├── 4_Data_Quality.py
│   └── 5_AI_Assistant.py
│
├── tests/
│   ├── test_validation.py
│   ├── test_leads.py
│   ├── test_repository.py
│   ├── test_lead_service.py
│   ├── test_analytics.py
│   └── test_ai_service.py
│
├── scripts/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.11+
- Git
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/mohammadtuhin0/BIAI-Corporate-Intelligence.git

cd BIAI-Corporate-Intelligence
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash
DATABASE_PATH=data/biai_crm.db
```

Get your API key from Google AI Studio:

https://aistudio.google.com/apikey

Never commit your actual API key to GitHub.

### 5. Initialize the Database

```bash
python scripts/init_database.py
```

### 6. Import Corporate Leads

```bash
python scripts/import_leads.py
```

### 7. Run the Application

```bash
python -m streamlit run app.py
```

The application will be available at:

http://localhost:8501

## Running Tests

Run the complete automated test suite:

```bash
pytest -v
```

Current test coverage includes:

- Analytics services
- Lead management
- Database repository
- Data validation
- AI service behavior
- AI context privacy checks

Latest test result: **26 tests passed**.

## Dataset

The project uses 25 fictional corporate leads supplied in the official BIAI Round 2 challenge pack.

The dataset includes:

- Company information
- Industry
- Contact information
- Lead source
- Sales stage
- Deal value in BDT
- Contact and follow-up dates

## Security & Configuration

- API credentials are stored in environment variables.
- `.env` is excluded from Git.
- SQLite database files are excluded from Git.
- Sensitive contact information is excluded from the Gemini business context.

## Project Status

**Core application and AI integration implemented.**

Testing, deployment, and final presentation preparation are in progress.

## Author

**Mohammad Tuhin**

CSE Student | AI/ML & Data Science Enthusiast

GitHub: https://github.com/mohammadtuhin0
