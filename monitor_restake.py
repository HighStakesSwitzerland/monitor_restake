from json import loads
from subprocess import check_output
from discord import SyncWebhook, Embed
from datetime import datetime, timedelta

webhook_url = 'https://discord.com/api/webhooks/xxxxx'
recipients = ''


class MonitorRestake:

    def __init__(self):
        super().__init__()

    def run(self):

        try:

            data = check_output(["journalctl", "--output", "json", "-u", "restake", "--since",
                                 datetime.strftime(datetime.today()-timedelta(hours=2), '%Y-%m-%d %H:%M:00')]).decode('utf-8')
            data = [loads(i)['MESSAGE'] for i in (data[:-1].split('\n'))]

            networks = {}
            network = "Cosmos" #a placeholder for now
            for i in data:
                if isinstance(i, list):
                    i = ''.join(chr(c) for c in i)
                if "Loaded" in i:
                    network = i.split('Loaded ')[1].replace(" ", "_")
                if network in networks:
                    networks[network] += i + ' '
                else:
                    networks[network] = i + ' '

            for i in networks:
                if not 'Autostake finished' in networks[i]:
                    if "Could not connect" in networks[i]:
                        error = "Check server configuration"
                        color = 16711935
                    elif "balance is too low" in networks[i] or "insufficient funds" in networks[i]:
                        error = "Wallet has a low balance or gas configuration is wrong"
                        color = 16711680
                    else:
                        error = "Undefined error, please check logs"
                        color = 16753920

                    self.discord_message(i, error, color)

        except Exception as e:
            self.discord_message("error", str(e), 0)

    def discord_message(self, network, error, color):
        
        webhook = SyncWebhook.from_url(webhook_url)
        embed = Embed(title=network.upper(), description=error, color=color)
        webhook.send(recipients, embed=embed)


MonitorRestake().run()
