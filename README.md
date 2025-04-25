# 🚀 Build with AI: Brand Monitoring Challenge

Welcome to the Brand Monitoring Challenge for our Build with AI workshop! In this exercise you’ll use the ADK (and optionally MCP) to build an end-to-end agent that:

1. **Ingests** mentions of a brand from multiple sources (Reddit, Twitter, News APIs, general web).
2. **Analyzes** what people are saying—sentiment, key topics, issue detection.
3. **Generates** a consolidated report highlighting the brand’s current public perception and areas of concern.

---

## 🛠 Workshop Tools & Prerequisites

- **Agent Development Kit (ADK)**
  Tool for defining your agent, tools, and function calls.

- **MCP (Model Context Protocol)** _(optional)_
  You’ll be given MCP credentials to connect. If your quota runs out, feel free to roll your own connectors or use plain function-calling.

- **Gemini**
  The LLM you’ll use for analysis and report generation.

- **Dependencies**
  Install all required packages from the provided `requirements.txt`:

  ```bash
  pip install -r requirements.txt
  ```

---

## 🚦 Challenge Statement

> **Given** the name of a brand (user input),
> **Build** an AI agent that:
> 1. Queries **at least three** data sources (e.g., Reddit, Twitter, News API, Web Scraper).
> 2. Performs **sentiment analysis**, **topic extraction**, and **issue detection** on the collected mentions.
> 3. Outputs a structured **Brand Monitoring Report** (see “Expected Output” below).

---

## 📥 Inputs

- `brand_name` (string)
  e.g. `"Acme Co."`

- *(Optional)* `start_date` / `end_date` to define the monitoring window.

---

## 📈 Expected Output

Your agent should return a **JSON** (or Markdown) report containing:

1. **Executive Summary**
   A 2–3 sentence overview of overall sentiment and top concerns.

2. **Sentiment Breakdown**
   Percentage of positive / neutral / negative mentions, **by source**.

3. **Top 5 Topics & Issues**
   Most frequently discussed themes (e.g., “shipping delays,” “customer support”).

4. **Trend Analysis**
   Simple time-series summary (mentions per day), highlighting peaks.

5. **Sample Mentions**
   2–3 representative quotes (with source name and link) for each sentiment category.

6. **Recommendations**
   Based on detected issues, suggest 2–3 actionable next steps.

---

## 🏗 Your Tasks

1. **Configure Connectors**
   - Use MCP with provided credentials, *or* implement your own via function calls/web scraping.

2. **Define Agent & Tools in ADK**
   - Declare functions for data ingestion, analysis, and report generation.

3. **Implement Analysis Pipeline**
   - Ingest raw mentions → clean/filter → call Gemini functions for sentiment & topics.

4. **Generate Report**
   - Aggregate results into the JSON/Markdown structure above.

5. **Demo Your Solution**
   - Run a live demo for **two** different brand names.

---

## 📝 Submission (Suggested)

- **GitHub Repo** containing:
  - `README.md`
  - Source code for your agent
  - `requirements.txt`
  - Example outputs for at least two brands


- **Evaluation Criteria** (for your reference):
  1. **Data Coverage**: ≥3 sources ingested.
  2. **Report Quality**: Clarity, completeness, structure.
  3. **Tooling**: Correct use of ADK functions (and MCP if used).
  4. **Code Quality**: Readable, modular, documented.

Good luck, and happy building! 🌟
