from lib.seeder import SeedStocks
from lib.seeder import SeedTweets, SeedPrices

import argparse


def main(args):
    cmd = args.command

    if cmd == 'seed_stocks':
        SeedStocks().run()
    elif cmd == 'tweetalyze':
        SeedTweets().run()
    elif cmd == 'seed_prices':
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['seed_stocks', 'seed_prices', 'tweetalyze'])
    args = parser.parse_args()

    main(args)
