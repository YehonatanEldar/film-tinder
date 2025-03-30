import os
import random

import qrcode
from flask import Flask, redirect, render_template, request, url_for
from PIL import Image

from pantry import Pantry

app = Flask(__name__)

pantry = Pantry()
print('Deleting existing baskets...')
pantry.delete_all_baskets()
print('Baskets deleted successfully!')

def create_party():
    party_id = random.randint(1000, 10000)
    
    pantry.new_basket(
        basket_name=f'party_{party_id}', 
        data={
            'id': party_id,
            'streaming services': [],
            'participant data': {}
        }
    )

    return party_id

def generate_qr_code(data, filename="qrcode.png", box_size=10, border=4, fill_color="black", back_color="white"):
    """
    Generate a QR code from the given data
    
    Parameters:
    data (str): The data to encode in the QR code
    filename (str): Output filename for the QR code image
    box_size (int): Size of each box in the QR code
    border (int): Border size around the QR code
    fill_color (str): Color of the QR code data
    back_color (str): Background color
    
    Returns:
    str: Path to the saved QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    img.save(filename)
    
    return os.path.abspath(filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/party/<id>')
def party(id):
    data = pantry.get(f'party_{id}')
    
    if not data:
        return f"No data found for party ID {id}", 404
    
    isHost = request.args.get("isHost")
    
    url_root = request.url_root
    join_url = f'{url_root}join_party/{id}'
    image_filename = f'qrcode_{id}.png'
    generate_qr_code(join_url, filename=os.path.join('qr_codes', image_filename))
    
    return render_template('party.html', image_filename=image_filename, join_url=join_url, id=id, isHost=isHost, data=data)

@app.route('/create_party')
def create_party_page():
    id = create_party()
    return redirect(url_for('party', id=id) + '?isHost=True')

@app.route('/join_party/<id>')
def join_party_page(id):
    return redirect(url_for('party', id=id) + '?isHost=False')

if __name__ == '__main__':
    app.run()
