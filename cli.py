import click
from img import process_images

@click.command()
@click.option('--input', '-i')
@click.option('--output', '-o')
def main(input, output):
    process_images(input, output)


if __name__ == "__main__":
    main()