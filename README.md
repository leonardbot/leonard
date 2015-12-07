# Leonard bot
Leonard bot is a virtual assistant, who will be can create notifications, notes, search in the internet and in the maps etc.
## Install and start
```
git clone https://github.com/sevazhidkov/leonard.git
cd leonard
pip install -r requirements.txt
```
After it, you need to set some environment variables that listed below.

You can start bot with running start.py script. Right now we don't support Python 2.x, bot tested on CPython 3.4.
```
python start.py
```
It will run bot with console adapter. You will see something like this:
```
Enter message:
Enter a comma-separated attachments(<type>_<path>):
```
Type your message in first line, second line leave empty. For example:
```
Enter message: !hello
Enter a comma-separated attachments(<type>_<path>):
BOT:  Hi!
```
You can test plugins for bot using console adapter. If you want to change adapter, set the ```adapter``` argument
of start script. For example:
```
python start.py --adapter telegram
```
Don't forget set adapter's environment variables that listed below.
## Plugins
| Name  | Description                | Example              |
|-------|----------------------------|----------------------|
| hello | Send hello message to user | Hello, bot<br>!hello |
|       |                            |                      |
|       |                            |                      |
## Environment variables
Variables sorted by priority: from high to low.

| Name                       | Description                                                 | Default value             |
|----------------------------|-------------------------------------------------------------|---------------------------|
| LEONARD\_MONGODB\_URI      | URI for connecting MongoDB                                  | mongodb://localhost:27017 |
| LEONARD\_REDIS\_HOST       | Host for Redis storage                                      | localhost                 |
| LEONARD\_REDIS\_PORT       | Port for Redis storage                                      | 6379                      |
| LEONARD\_REDIS\_DB         | Num of DB for Redis storage                                 | 0                         |
| LEONARD\_CONSOLE\_LANGUAGE | Letters of language that console adapter uses as default    | en                        |
| LEONARD\_TELEGRAM_TOKEN    | Token for connection to Telegram Bot API (telegram adapter) |                           |

## Contributing
* You can create new plugins or extend existing plugins. You can find examples of
plugins code in ```plugins/hello.py```. All hooks you can see in ```leonard/hooks.py```.
If you created new plugin don't forget to add it to ```installed_plugins.txt```.

* You can new adapters or improve existing adapters. You can see example adapter in
```adapters/console.py```. All adapters functions and classes are listed in ```leonard/adapter.py```.

* You can improve Leonard core. At the moment, the most important thing is more effective working with threads.

* You can translate Leonard to your language. Checkout ```messages``` folder and ```leonard/messages.py```.

## Contact
Send me a message in Telegram: [@sevazhidkov](https://telegram.me/sevazhidkov).

Or in Twitter: [@sevazhidkov](https://twitter.com/sevazhidkov).

Or E-mail: [seva@leonardbot.xyz](mailto:seva@leonardbot.xyz).

Also you can buy me [coffee](https://paypal.me/sevazhidkov/5USD), [pizza](https://paypal.me/sevazhidkov/10USD),
[new Macbook Pro](https://paypal.me/sevazhidkov/2408USD) or [whatever you want](https://paypal.me/sevazhidkov).