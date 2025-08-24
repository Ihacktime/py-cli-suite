import click
import smtplib
import random
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@click.group()
def email():
    """Email tools: send daily quotes, etc."""
    pass

@email.command()
@click.option('--csv-file', default='recipients.csv', help='Path to CSV file with recipients')
@click.option('--quotes-file', default='quotes.txt', help='Path to text file with quotes (one per line)')
def send_quotes(csv_file, quotes_file):
    """Send daily inspirational quotes to recipients."""
    # Get credentials from environment variables
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        click.echo("Error: Email credentials not found. Set EMAIL_USER and EMAIL_PASSWORD environment variables.")
        return
    
    # Read quotes from file
    try:
        with open(quotes_file, 'r') as f:
            quotes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        click.echo(f"Error: Quotes file '{quotes_file}' not found.")
        return
    
    if not quotes:
        click.echo("Error: No quotes found in the quotes file.")
        return
    
    # Function to send emails
    def send_email(recipient_name, recipient_email, quote):
        subject = "Your Daily Inspirational Quote"
        body = f"Hello {recipient_name}, here is your daily inspirational quote:\n\n{quote}"

        # Setting up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Sending the email
        try:
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(sender_email, sender_password)
            text = message.as_string()
            session.sendmail(sender_email, recipient_email, text)
            session.quit()
            click.echo(f"✓ Mail sent to {recipient_name} ({recipient_email})")
            return True
        except Exception as e:
            click.echo(f"✗ Failed to send email to {recipient_name} ({recipient_email}). Error: {e}")
            return False

    # Read CSV and send emails
    try:
        with open(csv_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            success_count = 0
            total_count = 0
            
            for row in reader:
                total_count += 1
                recipient_name = row['name']
                recipient_email = row['email']
                quote_of_the_day = random.choice(quotes)
                
                if send_email(recipient_name, recipient_email, quote_of_the_day):
                    success_count += 1
            
            click.echo(f"\nSent {success_count} out of {total_count} emails successfully.")
            
    except FileNotFoundError:
        click.echo(f"Error: CSV file '{csv_file}' not found.")
    except KeyError:
        click.echo("Error: CSV file must have 'name' and 'email' columns.")