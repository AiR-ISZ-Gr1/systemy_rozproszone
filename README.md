# Systemy Rozproszone (Distributed Systems)

This project provides ...

## Table of Contents
  
  - [Installation](#installation)
  - [Usage](#usage)
  - [About](#about)
  - [Features](#features)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AiR-ISZ-Gr1/systemy_rozproszone.git
    ```

2. Setup infrastructure on W:

    If on UNIX based system run:
    ```bash
    bash start_compose.sh
    ```
    2. If the port `XXXX` for setting up database is busy try:
    `#TODO`
   
    If on Windows open Docker Desktop as admin and Windows PowerShell as admin and run:
    ```bash
    ./start.bat
    ```

5. Wait till container `databases-startup` goes down.

6. Everything is set up.


## Usage

1. Open `localhost:8501`
2. Log-in to test client `TestU` or test admin `TestA`.


## About

Lorem Ipsum


## Features

- **Text**: Lorem ipsum.
- **Text**: Lorem ipsum.

# Systemy Rozproszone



### RUN ALL DOCKERS CONTAINERS
```bash
. start_compose.sh
```



### FRONTEND 

#### DOCKER BUILD
```bash
cd app/frontend
docker build --tag streamlit_frontend .
```
#### RUN FRONTEND
```bash
docker compose -f app/frontend/docker-compose.yml up
```

### RUN LOGIN AND REGISTER
```bash
docker compose -f app/login_register/docker-compose.yml up
```

### RUN DATABASES & CRUD API
```bash
docker compose -f app/databases/docker-compose.yml up
```

<video width="640" height="480" controls>
  <source src="demo.webm" type="video/webm">
</video>



