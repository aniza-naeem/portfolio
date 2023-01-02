This is a repository that I have created to showcase skills, share projects and track my progress in Data Analytics / Data Science related topics.

## Projects
### gmail account analysis

A fun project to analyze your personal Gmail account. This is my final project as part of my Data Analysis course at ReDI school of Copenhagen. Project is written in Python and does the following.

How many emails did I send during a given timeframe?​

At what times of the day do I send and receive emails with Gmail?​

The busiest day of the week in terms of emails?​

What is the average number of emails per day?​

What is the average number of emails per hour?​

What are the most active emailing days?​

What am I mostly emailing about?​

[Project code](../../tree/main/projects/gmail-analysis)

**Technologies/Libraries:** Jupyter notebook, numpy, pandas, matplotlib, mailbox, wordbank 

**Skills:** Data Analysis-> Descriptive Analysis, Data Visualization using Python

### cpu cost
This is an ETL pipeline written in python. pipleline runs every day at a specific time to get the cost data. Due to record limit in the source API, Pagination is implemented to get the complete data. I fetch the data using APIs from the source, do some math on it, and store the tranformed data in azure data lake for further analysis and reporting in Power BI. Decouple library is used to seperate the settings from code. This helps to manage settings for different environments independent of code.

[Project code](../../tree/main/projects/finops)

**Technologies/Libraries:** Visual studio, Azure data lake, Python Libraries (requests, json, csv, pandas, decouple)

**Skills**  Json data manipulation, CSV data manipulation, FinOps
