import os
import argparse
import bugsnag
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

bugsnag.configure(
  api_key=os.environ.get('LEONARD_BUGSNAG_KEY', ''),
  project_root=os.getcwd(),
  release_stage=os.environ.get('ENV', 'development')
)

try:
    bot.start()
except Exception as error:
    bugsnag.notify(error)
