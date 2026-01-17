This is a professional Interim Report structured specifically to meet the requirements of the 10 Academy Week 8 Challenge. You can copy this into a file named INTERIM_REPORT.md in your repository.

Interim Report: Telegram Medical Data Warehouse

Date: 17 Jan 2026
Status: Task 1 and Task 2 Completed

1. Project Overview

The objective of this project is to build an end-to-end data pipeline for Kara Solutions to analyze the Ethiopian medical business landscape using Telegram data. Currently, we have successfully implemented the extraction, loading, and transformation (ELT) layers.

2. Task 1: Data Lake Structure

Data is extracted from public Telegram channels (CheMed, Lobelia Cosmetics, Tikvah Pharma) using the Telethon library. The raw data is stored in a partitioned "Data Lake" to ensure scalability and easy tracking.

Directory Structure:
code
Text
download
content_copy
expand_less
data/
└── raw/
    ├── images/
    │   └── {channel_username}/
    │       └── {message_id}.jpg
    └── telegram_messages/
        └── YYYY-MM-DD/
            └── {channel_username}.json

JSON Metadata: Contains the raw API response including message text, timestamps, and engagement metrics (views/forwards).

Partitioning: Data is partitioned by date and channel, allowing for efficient incremental loading in the future.

3. Task 2: Data Warehouse & Star Schema

The raw data has been loaded into a PostgreSQL database (running in Docker) and transformed using dbt (Data Build Tool).

Star Schema Design

We implemented a dimensional model to optimize for analytical queries:

Staging Layer (stg_telegram_messages): Cleans raw data, casts data types (timestamps, integers), and handles missing values.

Dimension Tables:

dim_channels: Contains metadata about each channel, including the first/last post dates and average engagement.

Fact Tables:

fct_messages: The central table containing all message data, linked to dimensions via surrogate keys.

Diagram (Logical Layout):

fct_messages (Center)

message_id (PK)

channel_key (FK 
→
→
 dim_channels)

message_date

views, forwards

message_text

dim_channels (Side)

channel_key (PK)

channel_name

total_posts

4. Data Quality Summary

During the transformation phase, several data quality issues were identified and addressed:

Issue	Impact	Solution
Null Values	Views and forwards were null for some messages.	Used coalesce(views, 0) in dbt to ensure numerical consistency.
Data Types	Timestamps were stored as strings in JSON.	Casted to TIMESTAMP in the dbt staging layer for time-series analysis.
Messy Text	Empty or non-medical messages.	Implemented filters in staging to remove records with null message IDs or empty content.
Authentication Errors	Database port conflicts on local machine.	Migrated Docker container to port 5433 to bypass local Postgres services.
Automated Testing

We have implemented 11 data tests using dbt, including:

Uniqueness/Not Null: Enforced on all Primary Keys.

Relationships: Verified referential integrity between the Fact and Dimension tables.

Custom Business Rules: Created tests to ensure no future-dated messages exist and all view counts are non-negative.

