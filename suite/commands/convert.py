import click
from suite.utils.api import get_exchange_rate
from suite.utils.constants import CURRENCIES

def convert_currency(amount, exchange_rate):
    return amount * exchange_rate

@click.group()
def convert():
    """Conversion tools: currency, number-to-words, image."""
    pass

@convert.command()
@click.argument('amount', type=float)
@click.argument('base_currency')
@click.argument('target_currency')
def currency(amount, base_currency, target_currency):
    """Convert currency from base to target."""
    base_currency = base_currency.upper()
    target_currency = target_currency.upper()

    if base_currency not in CURRENCIES:
        click.echo(f"Error: Base currency {base_currency} is not supported.")
        return
    if target_currency not in CURRENCIES:
        click.echo(f"Error: Target currency {target_currency} is not supported.")
        return

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        click.echo("Error: Could not fetch exchange rate.")
        return

    converted_amount = convert_currency(amount, exchange_rate)
    click.echo(f"{amount} {base_currency} is {converted_amount:.2f} {target_currency}")

# Placeholder for number-to-words command
@convert.command()
@click.argument('number', type=int)
def number_to_words(number):
    """Convert a number to words."""
    click.echo(f"Number to words conversion for {number} will be implemented soon.")

# Placeholder for image conversion command
@convert.command()
@click.argument('input_path')
@click.argument('output_format')
def image(input_path, output_format):
    """Convert image format."""
    click.echo(f"Image conversion for {input_path} to {output_format} will be implemented soon.")