
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"

console = Console()
app = FastAPI(title="Evolv Token Scanner")


class TokenRequest(BaseModel):
    contract_address: str


def get_token_info(contract_address: str):
    url = f"{ETHERSCAN_BASE_URL}?module=token&action=tokeninfo&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("status") != "1":
        raise ValueError("Token not found or API error.")
    return data.get("result", [{}])[0]


def get_contract_source(contract_address: str):
    url = f"{ETHERSCAN_BASE_URL}?module=contract&action=getsourcecode&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("status") != "1":
        raise ValueError("Could not retrieve contract source code.")
    return data.get("result", [{}])[0]


def display_token_info(token_data):
    table = Table(title="Token Info", show_lines=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for key in ["TokenName", "Symbol", "TotalSupply", "Decimals"]:
        table.add_row(key, str(token_data.get(key, "N/A")))
    console.print(table)


def display_contract_analysis(source_data):
    table = Table(title="Contract Analysis", show_lines=True)
    table.add_column("Check", style="magenta")
    table.add_column("Result", style="yellow")

    owner_check = "Yes" if "owner" in source_data.get("SourceCode", "").lower() else "No"
    mint_check = "Yes" if "mint" in source_data.get("SourceCode", "").lower() else "No"

    table.add_row("Has Owner?", owner_check)
    table.add_row("Has Mint Function?", mint_check)
    console.print(table)


@app.post("/scan")
def scan_token(req: TokenRequest):
    try:
        token_data = get_token_info(req.contract_address)
        source_data = get_contract_source(req.contract_address)
        return {
            "token": {
                "name": token_data.get("TokenName"),
                "symbol": token_data.get("Symbol"),
                "total_supply": token_data.get("TotalSupply"),
                "decimals": token_data.get("Decimals"),
            },
            "analysis": {
                "has_owner": "owner" in source_data.get("SourceCode", "").lower(),
                "has_mint_function": "mint" in source_data.get("SourceCode", "").lower()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evolv Token Scanner")
    parser.add_argument("contract", help="Token contract address")
    args = parser.parse_args()

    try:
        console.print("[bold blue]Fetching token data...[/bold blue]")
        token_data = get_token_info(args.contract)
        display_token_info(token_data)

        console.print("[bold blue]Analyzing contract source...[/bold blue]")
        source_data = get_contract_source(args.contract)
        display_contract_analysis(source_data)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
