1.In the terminal, create and activate a virtual environment using uv. This ensures your project dependencies don't conflict with the system Python.

uv venv
source .venv/bin/activate

2.Install the required packages into your virtual environment in the terminal.

uv pip install -r requirements.txt


3. Use the following command in the terminal to create the .env file

3.1. Set the variables in your terminal first
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SA_NAME=lab2-cr-service

3.2. Create the .env file using those variables
cat <<EOF > .env
PROJECT_ID=$PROJECT_ID
PROJECT_NUMBER=$PROJECT_NUMBER
SA_NAME=$SA_NAME
SERVICE_ACCOUNT=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
MODEL="gemini-2.5-flash"
EOF


