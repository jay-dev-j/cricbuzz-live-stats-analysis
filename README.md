# 🏏 Cricbuzz Live Stats Analysis

A **data-driven cricket analytics web application** built using **Python, Streamlit, and MySQL**, designed to analyze live matches, player performance, and team statistics.

---

## 🚀 Features

* 🔴 Live Match Analysis
* 👤 Player Search & Statistics
* 📊 Team Performance Insights
* 🏆 Match Result Analysis
* 💾 Session State for better user experience
* 🗄️ 25+ SQL Queries for data analysis
* 🔄 Full CRUD Operations (Create, Read, Update, Delete)

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** MySQL
* **Libraries:** pandas, streamlit, mysql-connector

---

## 📂 Project Structure

```
Cricbuzz-Live-Stats/
│
├── app.py                 # Main Streamlit app (navigation)
├── home.py                # Home page UI
├── live_matches.py        # Live match analysis
├── player_stats.py        # Player statistics module
├── sql_queries.py         # 25+ SQL queries
├── crud_operations.py     # CRUD functionalities
├── Data_Fetching.ipynb    # Data collection & preprocessing
└── README.md
```

---

## 🔍 How It Works

* Cricket data is stored and managed using **MySQL**
* SQL queries are used to:

  * Analyze match results
  * Calculate team wins
  * Fetch player statistics
* The **Streamlit interface** allows:

  * Navigating between pages
  * Searching players
  * Viewing live match insights
* `st.session_state` is used to preserve user inputs across interactions

---

## 🗄️ Database & SQL Highlights

* Implemented **25+ SQL queries**
* Used operations like:

  * `GROUP BY` for aggregation
  * `COUNT()` for statistics
  * Filtering match results
* Includes full **CRUD operations**:

  * Insert new data
  * Fetch records
  * Update existing entries
  * Delete records

---

## 📸 Key Functionalities

* 🔍 Search and analyze player performance
* 🔴 View live or recent match details
* 📊 Compare team statistics
* 🧮 Generate insights using SQL queries

---

## 💡 Key Concepts Used

* Python Modules & Functions
* SQL Query Optimization
* Streamlit UI Development
* Session State Handling
* Data Analysis using Pandas

---

## 🎯 Future Improvements

* 🌐 Real-time API integration (Cricbuzz / RSS feeds)
* 📈 Advanced data visualizations (charts & dashboards)
* 🧠 Machine Learning for match prediction
* 📱 Responsive/mobile-friendly UI

---

## 🙋‍♂️ Author

**Jayadev J**
B.Tech Computer Science Engineering (Fresher)
Interested in **Data Analytics & Machine Learning**


---

## 📌 Note

This project is developed for **learning and academic purposes**.
