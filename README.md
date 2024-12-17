# Orix POC (New)


## Prerequisites
- Python 3.12
- UV Package Manager

## Setup & Installation
Run the following command to install dependencies:

```bash
uv sync --python 3.12
```

Create a `.env` file in the root directory, following the [reference template](./.env.example).


## How to run
```shell
uv run uvicorn app:app --reload
```
