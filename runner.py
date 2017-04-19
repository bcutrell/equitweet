from equitweet.seeder import SeedStocks, SeedTweets

import argparse
import json

def main(args, db_config):
    cmd = args.command

    if cmd == 'seed_stocks':
        SeedStocks(db_config).run()
    elif cmd == 'seed_tweets':
        SeedTweets(db_config).run()
    elif cmd == 'seed_prices':
        pass


if __name__ == '__main__':
    with open('database.json', 'r') as f:
        db_config = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['seed_stocks', 'seed_prices', 'seed_tweets'])
    args = parser.parse_args()

    main(args, db_config)

