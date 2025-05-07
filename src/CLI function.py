import argparse
from main import debugWifiStore, importCsv, wifiTable


def cli_main():
    parser = argparse.ArgumentParser(description="Wi-Fi Localization CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: locate scan
    subparsers.add_parser("locate-scan", help="Scan nearby APs and find location")

    # Subcommand: locate with count
    locate_parser = subparsers.add_parser("locate", help="Find location using specified AP count")
    locate_parser.add_argument("count", type=int, help="Number of APs to use")

    # Subcommand: count APs
    subparsers.add_parser("count", help="Count the number of APs in the database")

    # Subcommand: debugstore
    subparsers.add_parser("debugstore", help="Display the first few observations from the store")

    # Subcommand: import CSV
    import_parser = subparsers.add_parser("import", help="Import Wi-Fi data from a CSV file")
    import_parser.add_argument("file", type=str, help="Path to the CSV file")

    args = parser.parse_args()

    if args.command == "locate-scan":
        print("TODO: Implement Wi-Fi scanning")
    elif args.command == "locate":
        print(f"TODO: Locate using {args.count} APs")
    elif args.command == "count":
        print(f"Number of stored APs: {len(wifiTable.store)}")
    elif args.command == "debugstore":
        debugWifiStore()
    elif args.command == "import":
        importCsv(args.file)
        print("Data imported successfully!")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli_main()
