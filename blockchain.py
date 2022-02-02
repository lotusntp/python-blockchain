
import datetime
import json
import hashlib
from urllib import response
from flask import Flask , jsonify

from attr import has
class Blockchain:
    def __init__(self):
        # save group block
        self.chain = [] # list save block
        # genesis block
        self.create_block(nonce=1,previous_hash="0")
        

    
    # method create blockchain system
    def create_block(self,nonce,previous_hash):
        # เก็บส่วนประกอบของ block แต่ละ block
        block = {
            "index": len(self.chain)+1,
            "timestamp":  str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash" : previous_hash
        }
        self.chain.append(block)
        return block

    # ให้บริการเกี่ยวกับ Block ล่าสุดที่อยู่ใน blockchain
    def get_previous_block(self):
        return self.chain[-1]

    def hash(self,block):
        # เรียงข้อมูลใน block  แปลง python object (dict) => json object
        encode_block = json.dumps(block,sort_keys=True).encode()
        # sha-256
        return hashlib.sha256(encode_block).hexdigest()

    def proof_of_work(self,previous_nonce):
        # อยากได้ค่า nonce ที่ส่งผมให้ได้ target hash => 0000
        new_nonce = 1 #ค่า nonce ที่ต้องการ
        check_proof = False # ตัวแปรเช็คค่า nonce ให้ได้ตาม traget ที่กำหนด

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_nonce+=1
        return new_nonce

    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"] # nonce block ก่อนห้นา
            nonce = block["nonce"] # nonce ของ block ที่ตรวจสอบ
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block=block
            block_index+=1

        return True
# web server
app = Flask(__name__)
# use blockchain
blockchain = Blockchain()
# routing
@app.route('/')
def hello():
    return "<p>Hello Blockchian</p>"

@app.route('/get_chain',methods=["GET"])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/mining',methods=["GET"])
def mining_bloc():
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block['nonce']

    nonce = blockchain.proof_of_work(previous_nonce)
    #hash block ก่อนหน้า
    previous_hash = blockchain.hash(previous_block)
    #update new block
    block = blockchain.create_block(nonce,previous_hash)

    response = {
        "message": "Mining block suscessc",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response),200

@app.route('/is_valid',methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "block is valid"}
    else:
        response = {"message": "Have Problem , Blockchain Is Not Valid"}

    return jsonify(response),200
#run server
if __name__ == "__main__":
    app.run()




