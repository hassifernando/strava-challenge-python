# Strava Challenge Python

  This project is a set of automated tests for integration with the Strava API, a platform for fitness activities. It performs tests on various API endpoints to ensure correct functionality and integration with the system.

The tests cover features such as user authentication, retrieval of athlete profile information, activity creation, and other related operations.

The goal of this project is to apply and enhance knowledge in Python, as well as utilize the advanced features of Pytest to comprehensively test the various API endpoints.
## Features
- User authentication and authorization
- Retrieval of athlete profile information
- Activity creation and management
- Security and confidentiality testing
- Verification of API response structure and formats
  
## Requirements

- Python: 3.11.4
- pipenv: version 2023.7.11

## Installation

Clone this repository to your local machine:

```shell
git clone https://github.com/hassifernando/strava-challenge-python.git
```
Navigate to the project directory:

```
cd strava-challenge-python
```
Install the necessary dependencies:

```
pipenv install
```

## Running the Tests os Testes

To run the automated tests, follow the steps below:


Navigate to the project directory:

```
cd strava-challenge-python
```

Execute the following command to run all tests:
```
pytest
```
If you prefer to run specific tests:
```
 pytest -k test_create_activity tests/test_activities.py
```

