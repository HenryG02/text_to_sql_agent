# text_to_sql_agent

## 1. Context
In my free time (when I was younger), I liked to train and speedsolve Rubik's Cube and similar puzzles. I even participated in official World Cube Association (WCA) competitions. However, I've "retired" myself from the competitive scene, since my last participation in official competitions was in 2017.

Nonetheless, I'm trying to regain the habit and participate in a competition in 2026. Connecting this hobby with my professional and academic interests and ocupations, in this project, a **Text-to-SQL agent** will be developed with the goal of helping me by answering questions about my performance and giving me valuable hidden insights, such as which weekday I tend to perform better, for example.

## 2. Tech Stack
For this project, the programming language used is Python. In the pyproject.toml file, all project dependecies are listed, with uv being used as dependency manager. We'll use Agno for LLM/agent orchestration and Supabase to store our data remotely on a PostgreSQL database. For the UI, the streamlit library will be used.

## 3. Repository Structure
**data**: folder containing raw .txt files with solve times and metadata exported from an Android speedcubing timer app, called Twisty Timer.

**notebooks**: folder containing Jupyter notebooks for data exploration and explanation of some theoretical/statistical concepts that will be useful when analyzing the data.

**scripts**: folder containing standalone Python scripts that support the solution.

**src**: folder containing the source code of the solution.

**pyproject.toml**: project configuration and dependencies file

**.env.example**: a mock .env file with the necessary environment variables for the project
