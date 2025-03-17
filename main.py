from utils import Client, Search, argparse

def main():
    parser = argparse.ArgumentParser(description="go2web: A CLI tool for making HTTP requests and searching the web.")
    parser.add_argument("-u", "--url", type=str, help="Fetch content from a URL")
    parser.add_argument("-s", "--search", type=str, help="Search the web for a term")

    args = parser.parse_args()
    
    if args.url:
        print(Client.send_request(args.url))
    elif args.search:
        print(Search.search_term(args.search))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()