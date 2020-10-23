from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    phone_number = request.args.get('phones')
    if not phone_number:
      return render_template('index.j2')
    phone_number = phone_number.replace("+", "%2B")
    phone_number = phone_number.replace(" ", "%20")
    resp = requests.get(f'https://phonenumbervalidation.apifex.com/api/v1/validate?phonenumber={phone_number}')
    if not resp :
      return render_template('index.j2', not_valid="This is not a valid number. Please try again")
    resp_json = resp.json()
    country_name = resp_json['country_name_for_number']
    number_type = resp_json['number_type']
    formatt = resp_json['format_number_international']
    to_call = formatt.replace(" ", "")
    whats_msg = f'https://api.whatsapp.com/send?phone={to_call}'
    phone_call = "tel:" + to_call
    if resp_json['is_valid_number']:
      valid_number = 'Yes'
    else:
        valid_number = 'No'
    if resp_json['is_possible_number']:
      possible_number = 'Yes'
    else:
      possible_number = 'No'
    return render_template(
      'index.j2',
      type_number=number_type,
      country=country_name,
      format=formatt,
      valid=valid_number,
      possible=possible_number,
      tel=phone_call,
      whatsapp=whats_msg
      )

if __name__ == '__main__':
    app.run(debug=True)