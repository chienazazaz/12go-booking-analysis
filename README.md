# 12Go Booking Analysis

This repository contains the code and resources for analyzing booking data from the 12Go platform. The analysis focuses on extracting insights related to booking trends, customer behavior, channel performance, and operational metrics.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)

---

## Project Overview

The goal of this project is to perform exploratory data analysis (EDA) on booking data to uncover trends, identify issues, and propose actionable insights. The analysis includes:
- Booking and transaction characteristics
- Customer and channel insights

---

## Setup Instructions
```bash
poetry install
poetry shell
jupyter notebook
streamlit run dashboard/Home.py
```

## Key Files & Folder
- [initial_approach](initial_approach.ipynb): Notebook outlining the initial exploration and approach to the analysis.
- [EDA_P1](EDA_P1.ipynb): Contains the first part of the exploratory data analysis, focusing on booking trends and initial insights.
- [EDA_P2](EDA_P2.ipynb): Continuation of the EDA, diving deeper into customer behavior and channel performance.
- [Dashboard](dashboard): Streamlit child project