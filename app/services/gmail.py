from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pathlib import Path
from email.mime.text import MIMEText
import base64

SCOPES = [
	"https://www.googleapis.com/auth/gmail.readonly",
	"https://www.googleapis.com/auth/gmail.send"
	]

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CRED_FILE = BASE_DIR / "gmail_credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

def get_gmail_service():
	"""Authenticate and return Gmail API Client."""
	creds = None

	if TOKEN_FILE.exists():
		creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
	
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
			creds = flow.run_local_server(port=0)
	
	with open(TOKEN_FILE, 'w') as token:
		token.write(creds.to_json())
	
	return build("gmail", "v1", credentials=creds)


def fetch_latest_unread_email():
	"""Get newest unreaded email."""
	service = get_gmail_service()

	# list of unreaded mails
	result = service.users().messages().list(
		userId="me",
		q="is:unread",
		maxResults=1
	).execute()

	messages = result.get("messages", [])
	if not messages:
		return None

	# load mail via id
	msg = service.users().messages().get(
		userId="me",
		id=messages[0]["id"],
		format="full"
	).execute()

	# read header
	headers = msg["payload"]["headers"]
	subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
	sender = next((h["value"] for h in headers if h["name"] == "From"), "")
	message_id = next((h["value"] for h in headers if h["name"] == "Message-ID"), "")

	# extract mail body
	body = ""
	parts = msg["payload"].get("parts", [])
	for part in parts:
		if part["mimeType"] == "text/plain":
			body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
			break
	
	return {
		"subject": subject,
		"sender": sender,
		"body": body,
		"thread_id": msg["threadId"],
		"message_id": message_id
	}

def send_mail(to:str, subject:str, body:str, thread_id:str, message_id:str, quoted_text:str|None=None) -> str:
	"""Sends reply email in the context of an existing thread."""
	print("SEND_MAIL FUNCTION CALLED")
	service = get_gmail_service()

	full_body = body
	if quoted_text:
		full_body += f"\n\n--- Original Message ---\n{quoted_text}"
	message = MIMEText(full_body)
	message["to"] = to
	message["subject"] = subject
	message["In-Reply-To"] = message_id
	message["References"] = message_id

	raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

	service.users().messages().send(
		userId="me",
		body={"raw": raw, "threadId": thread_id}
	).execute()

	return f"E-Mail send to {to}"