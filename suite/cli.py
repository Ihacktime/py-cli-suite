import click

@click.group()
def cli():
    """A suite of useful CLI tools."""
    pass

# Import and register commands
from suite.commands.convert import convert
from suite.commands.email import email
from suite.commands.web import web
from suite.commands.media import media
from suite.commands.contacts import contacts

cli.add_command(convert, name='convert')
cli.add_command(email, name='email')
cli.add_command(web, name='web')
cli.add_command(media, name='media')
cli.add_command(contacts, name='contacts')

if __name__ == '__main__':
    cli()