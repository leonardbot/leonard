import argparse
from leonard import Leonard

parser = argparse.ArgumentParser(description='Start bot')
parser.add_argument('--config-prefix', type=str, default='LEONARD_',
                    help='a str from which starting all config variables')
parser.add_argument('--adapter', type=str, default='console',
                    help='a str with name of adapter from adapters folder'
                         'or PyPi')
args = parser.parse_args()

bot = Leonard({'config-prefix': args.config_prefix,
               'adapter': args.adapter})

bot.start()
