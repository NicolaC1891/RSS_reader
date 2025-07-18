import argparse


def read_cli_parameters() -> argparse.Namespace:
    """
    Reads CLI parameters
    :return: argparge.Namespace instance with CLI parameters stored in attributes
    """
    cli_reader = argparse.ArgumentParser(description="This is an RSS reader")
    cli_reader.add_argument("--source", type=str, help="RSS URL")  # remove --
    cli_reader.add_argument("--version", action="version", version="RSS Reader v.0.1")
    cli_reader.add_argument("--json", action="store_true", help="Print results as JSON in stdout")
    cli_reader.add_argument("--verbose", action="store_true", help="Output verbose status messages")
    cli_reader.add_argument("--limit", type=int, help="Limit new topics if this parameter is provided")
    cli_parameters.source = "https://auto.onliner.by/feed"
    cli_parameters.verbose = True
    cli_parameters.limit = 5
    cli_parameters.json = True
    return cli_reader.parse_args()


cli_parameters = read_cli_parameters()
