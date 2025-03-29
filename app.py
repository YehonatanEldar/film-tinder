import random

from flask import Flask, render_template

from pantry import Pantry


app = Flask(__name__)

pantry = Pantry()

def create_party():
    party_id = random.randint(100, 1000)
    
    pantry.put(
        basket_name=f'party_{party_id}', 
        data={
            'id': party_id,
            'streaming services': [],
            'participant data': {}
        }
    )

@app.route('/')
def home():
    # Button to start a party
    return render_template('index.html')

@app.route('/party/<id>')
def party(id):
    data = pantry.get(f'party_{id}')
    # QR code for joining
    # Host feature
    # Host can add or delete streaming services
    # Host can remove participants
    # Host can start party
    return render_template('party.html')

if __name__ == '__main__':
    app.run()