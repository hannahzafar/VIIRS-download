#!/usr/bin/env python
"""
Script to download VIIRS data using earthaccess with .netrc authentication.
"""

import argparse
import datetime
import os

import earthaccess


def validate_date(date_string):
    """
    Validate date string format.

    Args:
        date_string: str
            Date string to validate

    Returns:
        str: Validated date string

    Raises:
        argparse.ArgumentTypeError : If date format is invalid
    """
    try:
        datetime.date.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {date_string}. Use YYYY-MM-DD"
        )


def parse_arguments():
    """
    Parse command line arguments for target file(s).

    Returns:
    argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Arguments specifying target VIIRS data files"
    )

    parser.add_argument(
        "-p",
        "--product",
        type=str,
        required=True,
        help="VIIRS product short name (e.g., VNP64A1, VNP46A2)",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        required=True,
        help="VIIRS product version (e.g., 001, 002)",
    )

    parser.add_argument(
        "-gs",
        "--granule-string",
        type=str,
        required=False,
        help="VIIRS product wildcard string (fix for 16-day running average products)",
    )

    parser.add_argument(
        "-s",
        "--start-date",
        type=validate_date,
        required=True,
        help="Start date in YYYY-MM-DD format",
    )

    parser.add_argument(
        "-e",
        "--end-date",
        type=validate_date,
        required=True,
        help="End date in YYYY-MM-DD format",
    )

    return parser.parse_args()


def setup_earthdata_auth():
    """
    Authenticate with NASA Earthdata using standard .netrc file with the host urs.earthdata.nasa.gov.
    Returns: authentication
    """
    try:
        # earthaccess will automatically use .netrc if available
        auth = earthaccess.login(strategy="netrc")
        print("Successfully authenticated Earthdata login")
        return auth
    except Exception:
        print("Check .netrc login credentials for urs.earthdata.nasa.gov")
        return None


def main():
    # Parse input args
    args = parse_arguments()
    # print(args.product, args.version, args.granule_string, args.start_date, args.end_date, sep="\n")

    # Authenticate with earthaccess
    setup_earthdata_auth()

    # Query results
    print("Querying results...")
    # Include granule_string only if optional param is set
    if args.granule_string is not None:
        results = earthaccess.search_data(
            short_name=args.product,
            version=args.version,
            granule_name=args.granule_string,
            cloud_hosted=True,
            temporal=(args.start_date, args.end_date),
        )
    else:
        results = earthaccess.search_data(
            short_name=args.product,
            version=args.version,
            cloud_hosted=True,
            temporal=(args.start_date, args.end_date),
        )

    # print(len(results))
    # print(results[0])
    if len(results) < 1:
        print("No matching results found. Check input arguments")
        return

    # Download results
    download_folder = (
        f"{args.product}_V{args.version}_{args.start_date}_{args.end_date}"
    )

    # Make sure to not overwrite existing
    try:
        os.makedirs(download_folder, exist_ok=False)
    except FileExistsError as e:
        print(e)
        return

    # print(download_folder)
    files = earthaccess.download(results, download_folder)
    print(f"{len(files)} files downloaded to {download_folder}")


if __name__ == "__main__":
    main()
