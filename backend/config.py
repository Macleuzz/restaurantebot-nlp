from dotenv import load_dotenv
import os

load_dotenv()

LANGUAGE_ENDPOINT   = os.getenv("LANGUAGE_ENDPOINT")
LANGUAGE_KEY        = os.getenv("LANGUAGE_KEY")
LANGUAGE_PROJECT    = os.getenv("LANGUAGE_PROJECT")
LANGUAGE_DEPLOYMENT = os.getenv("LANGUAGE_DEPLOYMENT")

SQL_SERVER   = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER     = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

SENDGRID_KEY        = os.getenv("SENDGRID_KEY") 
EMAIL_RESTAURANTE   = os.getenv("EMAIL_RESTAURANTE")

MicrosoftAppId       = os.getenv("MicrosoftAppId", "")
MicrosoftAppPassword = os.getenv("MicrosoftAppPassword", "")