

# DRF CSV Upload API

This Django REST Framework (DRF) project provides an API endpoint to upload a CSV file containing user data, validate it, and store valid entries in the database.

---

## Features

- Upload a `.csv` file via POST API
- Validates each row:
  - `name`: Must be a non-empty string
  - `email`: Must be a valid email (duplicates skipped)
  - `age`: Must be an integer between 0 and 120
- Saves only valid rows
- Returns:
  -  Total saved records
  -  Total rejected records
  -  Validation errors for each rejected row
- Bonus:
  - DRF serializer-based validation
  - Unit tests included

---

##  Sample Input File

File: `sample_users.csv`

```csv
name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,25
Invalid Email,invalid-email,40
Empty Name,,35
Too Young,kid@example.com,-1
Too Old,old@example.com,130
Duplicate,john@example.com,28


```
## Sample output json
 File: `sample_output.json`

 ```json

{
  "saved_records": 2,
  "rejected_records": 5,
  "validation_errors": [
    {
      "row": 3,
      "errors": {"email": ["Enter a valid email address."]}
    },
    {
      "row": 4,
      "errors": {"email": ["This field may not be blank."]}
    },
    {
      "row": 5,
      "errors": {"age": ["Ensure this value is greater than or equal to 0."]}
    },
    {
      "row": 6,
      "errors": {"age": ["Age must be between 0 and 120."]}
    },
    {
      "row": 7,
      "errors": {"email": ["Duplicate email."]}
    }
  ]
}
```

## How to Run Locally
1.Clone the repository and navigate to the folder
2. create and activate a virtual environment

```bash

python -m venv venv
source venv/bin/activate

 ```
3. install dependencies
```bash
pip install -r requirements.txt
```
4.Apply migrations
```bash
python manage.py migrate
```
5. Run the server
```bash
python manage.py runserver
```
## API endpoint

method : POST

URL: /api/upload-csv

description: upload CSV file(use ```file``` key in ```form data```)

## Run Unit tests
```bash
python manage.py test users
```
