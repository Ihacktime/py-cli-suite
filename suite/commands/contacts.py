import click
import sqlite3
from typing import Optional
import os

class ContactManager:
    def __init__(self, db_path='contacts.db'):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Create a SQLite table for storing contacts if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    name TEXT PRIMARY KEY,
                    phone TEXT,
                    email TEXT
                )
            ''')
            conn.commit()

    def add_contact(self, name: str, phone: str, email: Optional[str] = None) -> bool:
        """Add a new contact to the contact book."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', 
                               (name, phone, email))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def list_contacts(self):
        """Get all contacts from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, phone, email FROM contacts ORDER BY name')
            return cursor.fetchall()

    def get_contact(self, name: str):
        """Get a specific contact by name."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, phone, email FROM contacts WHERE name = ?', (name,))
            return cursor.fetchone()

    def delete_contact(self, name: str) -> bool:
        """Delete a contact from the contact book."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
            conn.commit()
            return cursor.rowcount > 0

    def update_contact(self, name: str, phone: Optional[str] = None, email: Optional[str] = None) -> bool:
        """Update an existing contact's details."""
        # Get current contact details
        current = self.get_contact(name)
        if not current:
            return False
        
        # Use current values if new ones aren't provided
        new_phone = phone if phone is not None else current[1]
        new_email = email if email is not None else current[2]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE contacts SET phone = ?, email = ? WHERE name = ?', 
                           (new_phone, new_email, name))
            conn.commit()
            return cursor.rowcount > 0

@click.group()
def contacts():
    """Contact management tools."""
    pass

@contacts.command()
@click.argument('name')
@click.argument('phone')
@click.option('--email', '-e', help='Contact email address')
def add(name, phone, email):
    """Add a new contact."""
    manager = ContactManager()
    if manager.add_contact(name, phone, email):
        click.echo(click.style('Contact added successfully!', fg='green'))
    else:
        click.echo(click.style('Contact already exists!', fg='red'))

@contacts.command()
@click.argument('name')
def get(name):
    """Get a specific contact."""
    manager = ContactManager()
    contact = manager.get_contact(name)
    if contact:
        click.echo(click.style(f"Name: {contact[0]}", fg='yellow'))
        click.echo(click.style(f"Phone: {contact[1]}", fg='yellow'))
        click.echo(click.style(f"Email: {contact[2]}", fg='yellow'))
    else:
        click.echo(click.style('Contact not found!', fg='red'))

@contacts.command()
def list():
    """List all contacts."""
    manager = ContactManager()
    contacts = manager.list_contacts()
    if contacts:
        click.echo(click.style("\nContact List:", fg='cyan'))
        click.echo(click.style("=" * 50, fg='cyan'))
        for name, phone, email in contacts:
            click.echo(click.style(f"Name: {name}", fg='yellow'))
            click.echo(click.style(f"Phone: {phone}", fg='yellow'))
            click.echo(click.style(f"Email: {email}", fg='yellow'))
            click.echo(click.style("-" * 30, fg='cyan'))
    else:
        click.echo(click.style('No contacts found!', fg='red'))

@contacts.command()
@click.argument('name')
def delete(name):
    """Delete a contact."""
    manager = ContactManager()
    if manager.delete_contact(name):
        click.echo(click.style('Contact deleted successfully!', fg='green'))
    else:
        click.echo(click.style('Contact not found!', fg='red'))

@contacts.command()
@click.argument('name')
@click.option('--phone', '-p', help='New phone number')
@click.option('--email', '-e', help='New email address')
def update(name, phone, email):
    """Update a contact's details."""
    manager = ContactManager()
    if manager.update_contact(name, phone, email):
        click.echo(click.style('Contact updated successfully!', fg='green'))
    else:
        click.echo(click.style('Contact not found!', fg='red'))