import requests
import time
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich import print
import json

console = Console()

class Major:
    def __init__(self):
        self.base_url = "https://major.glados.app/api"
        self.endpoints = {
            "auth": f"{self.base_url}/auth/tg/",
            "user_info": f"{self.base_url}/users/",
            "streak": f"{self.base_url}/user-visits/streak/",
            "visit": f"{self.base_url}/user-visits/visit/",
            "roulette": f"{self.base_url}/roulette/",
            "hold_coins": f"{self.base_url}/bonuses/coins/",
            "tasks": f"{self.base_url}/tasks/",
            "swipe_coin": f"{self.base_url}/swipe_coin/",
        }
        self.total_balance = 0

        console.print(Panel("Telegram Channel : t.me/ugdairdrop\nTelegram Group : t.me/ngopiUGD", 
                            title="[bold green]Welcome to MAJOR BOT[/bold green]", title_align="left"))

    def headers(self, token=None):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://major.glados.app/reward",
            "Referer": "https://major.glados.app/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def log(self, msg, style):
        console.print(msg, style=style)

    def wait_with_countdown(self, seconds):
        with Progress() as progress:
            task = progress.add_task("[cyan]Waiting...", total=seconds)
            for _ in range(seconds):
                progress.update(task, advance=1)
                time.sleep(1)
    
    def api_request(self, method, url, data=None, token=None):
        try:
            response = requests.request(method, url, headers=self.headers(token), json=data)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if response.status_code == 400:
                # Specific handling for 400 errors
                if "roulette" in url:
                    self.log("[yellow]Roulette action might have already been claimed.[/yellow]", style="yellow")
                elif "bonuses/coins" in url:
                    self.log("[yellow]Coins bonus might have already been claimed.[/yellow]", style="yellow")
                elif "swipe_coin" in url:
                    self.log("[yellow]Swipe coin action might have already been completed.[/yellow]", style="yellow")
                else:
                    self.log(f"[red]Bad request for {url}: {str(e)}[/red]", style="bold red")
            else:
                self.log(f"[red]Error in API request: {str(e)}[/red]", style="bold red")
            return None
        except requests.RequestException as e:
            self.log(f"[red]Error in API request: {str(e)}[/red]", style="bold red")
            return None

    def authenticate(self, init_data):
        result = self.api_request("POST", self.endpoints["auth"], {"init_data": init_data})
        if not result:
            self.log("[red]Error during authentication[/red]", style="bold red")
        return result

    def get_user_info(self, user_id, token):
        result = self.api_request("GET", f"{self.endpoints['user_info']}{user_id}/", token=token)
        if result:
            self.total_balance += result.get('rating', 0)
        return result

    def get_streak(self, token):
        return self.api_request("GET", self.endpoints["streak"], token=token)

    def post_visit(self, token):
        return self.api_request("POST", self.endpoints["visit"], {}, token=token)

    def spin_roulette(self, token):
        result = self.api_request("POST", self.endpoints["roulette"], {}, token=token)
        if result and result.get('rating_award', 0) > 0:
            self.total_balance += result['rating_award']
        return result

    def hold_coins(self, token):
        coins = random.randint(900, 950)
        return self.api_request("POST", self.endpoints["hold_coins"], {"coins": coins}, token=token)

    def swipe_coin(self, token):
        get_result = self.api_request("GET", self.endpoints["swipe_coin"], token=token)
        if get_result and get_result.get('success'):
            coins = random.randint(1000, 1300)
            return self.api_request("POST", self.endpoints["swipe_coin"], {"coins": coins}, token=token)
        return None

    def get_daily_tasks(self, token):
        return self.api_request("GET", f"{self.endpoints['tasks']}?is_daily=false", token=token)

    def complete_task(self, token, task):
        return self.api_request("POST", self.endpoints["tasks"], {"task_id": task['id']}, token=token)

    def format_blocked_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def process_account(self, init_data, account_index):
        auth_result = self.authenticate(init_data)
        if not auth_result or not auth_result.get('access_token') or not auth_result.get('user'):
            self.log(f"[red]Unable to authenticate account {account_index + 1}. Auth result: {json.dumps(auth_result)}[/red]", style="bold red")
            return

        access_token = auth_result['access_token']
        user = auth_result['user']
        if not user.get('id') or not user.get('first_name'):
            self.log(f"[red]Invalid user data for account {account_index + 1}. User data: {json.dumps(user)}[/red]", style="bold red")
            return

        user_id = user['id']
        first_name = user['first_name']

        console.print(Panel(f"[cyan]Account {account_index + 1} | {first_name}[/cyan]", title="Account Info", title_align="left"))

        try:
            user_info = self.get_user_info(user_id, access_token)
            if not user_info:
                raise Exception("Failed to get user info")

            streak_info = self.get_streak(access_token)
            visit_result = self.post_visit(access_token)
            roulette_result = self.spin_roulette(access_token)
            hold_coins_result = self.hold_coins(access_token)
            swipe_coin_result = self.swipe_coin(access_token)

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Task", style="dim")
            table.add_column("Status", justify="right")

            table.add_row("Stars", str(user_info.get('rating', 0)))
            table.add_row("Streak", f"{streak_info['streak'] if streak_info else 'N/A'} days")

            if visit_result and visit_result.get('is_increased'):
                table.add_row("Check-in", f"Success (Day {visit_result['streak']})")
            elif visit_result:
                table.add_row("Check-in", f"Already done (Day {visit_result['streak']})")
            else:
                table.add_row("Check-in", "Failed", style="red")

            if roulette_result and roulette_result.get('rating_award', 0) > 0:
                table.add_row("Roulette", f"+{roulette_result['rating_award']} stars")
            elif roulette_result and roulette_result.get('detail', {}).get('blocked_until'):
                table.add_row("Roulette", f"Blocked until {self.format_blocked_time(roulette_result['detail']['blocked_until'])}", style="yellow")
            else:
                table.add_row("Roulette", "Already Claimed", style="yellow")

            if hold_coins_result and hold_coins_result.get('success'):
                table.add_row("Hold Coins", "Success")
            elif hold_coins_result and hold_coins_result.get('detail', {}).get('blocked_until'):
                table.add_row("Hold Coins", f"Blocked until {self.format_blocked_time(hold_coins_result['detail']['blocked_until'])}", style="yellow")
            else:
                table.add_row("Hold Coins", "Already Claimed", style="yellow")

            if swipe_coin_result and swipe_coin_result.get('success'):
                table.add_row("Swipe Coin", "Success")
            elif swipe_coin_result and swipe_coin_result.get('detail', {}).get('blocked_until'):
                table.add_row("Swipe Coin", f"Blocked until {self.format_blocked_time(swipe_coin_result['detail']['blocked_until'])}", style="yellow")
            else:
                table.add_row("Swipe Coin", "Already Claimed", style="yellow")

            console.print(table)
            self.log(f"[cyan]Updated Stars: {user_info.get('rating', 0)}[/cyan]", style="cyan")

        except Exception as e:
            self.log(f"[red]Error processing account {account_index + 1}: {str(e)}[/red]", style="bold red")

    def main(self):
        try:
            with open("token.txt", "r") as file:
                accounts = file.readlines()

            while True:
                for index, line in enumerate(accounts):
                    line = line.strip()
                    if line:
                        self.process_account(line, index)
                    self.wait_with_countdown(10)  # Wait between accounts
                self.wait_with_countdown(3600)  # Wait for 1 hour before repeating
        except FileNotFoundError:
            self.log("[red]token.txt file not found[/red]", style="bold red")

if __name__ == "__main__":
    major = Major()
    major.main()
