from trello import TrelloClient
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuração do Trello
client = TrelloClient(
    api_key='YOUR_API_KEY',
    api_secret='YOUR_API_SECRET',
    token='YOUR_TOKEN',
    token_secret='YOUR_TOKEN_SECRET'
)
board_id = 'YOUR_BOARD_ID'
list_name = 'YOUR_LIST_NAME'

# Configuração do Google Sheets
creds = service_account.Credentials.from_service_account_file(
    'PATH_TO_YOUR_SERVICE_ACCOUNT_FILE.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
sheet_id = 'YOUR_SHEET_ID'
sheet_range = 'Sheet1!A1'

# Obter a lista do Trello
board = client.get_board(board_id)
trello_list = board.get_list(list_name)

# Obter as informações do card
card = trello_list.list_cards()[0]  # obtém o primeiro card na lista
card_name = card.name
card_desc = card.desc

# Atualizar a planilha do Google Sheets
values = [[card_name, card_desc]]
body = {'values': values}
result = service.spreadsheets().values().update(
    spreadsheetId=sheet_id,
    range=sheet_range,
    valueInputOption='RAW',
    body=body
).execute()

print(f"{result.get('updatedCells')} células atualizadas.")
