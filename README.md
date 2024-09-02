# Orix POC

## Setup & Installation

1. Create python virtual environment
   ```shell
   python3 -m venv venv
   ```
2. Activate python virtual environment
   ```shell
   source venv/bin/activate
   ```
3. Install python dependencies from `requirements.txt` file
   ```shell
   pip install -r requirements.txt
   ```


## How to run
   ```shell
   python3 app.py
   ```
   or
   ```shell
   uvicorn app:app --reload
   ```