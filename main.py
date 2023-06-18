import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
import requests

load_dotenv()

app = Flask(__name__)

my_secret = os.environ['ERD_API_KEY'] or os.getenv("ERD_API_KEY")

def get_exchange_rate(from_currency, to_currency, amount, date=None):
  url = f"https://api.apilayer.com/currency_data/convert?from={from_currency}&to={to_currency}&amount={amount}"

  headers = {"apikey": my_secret}

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    result = response.json()
    return result["result"]
  else:
    raise Exception(f"Error: {response.status_code}, {response.text}")


@app.route('/convert', methods=['GET'])
def convert_currency():
  from_currency = request.args.get('from')
  to_currency = request.args.get('to')
  amount = request.args.get('amount')
  date = request.args.get('date', None)

  try:
    converted_amount = get_exchange_rate(from_currency, to_currency, amount,
                                         date)
    return jsonify({
      "from": from_currency,
      "to": to_currency,
      "amount": amount,
      "converted_amount": converted_amount
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
  app.run()
