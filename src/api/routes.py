"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, DontationInfo
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/donation_info', methods=["POST"])
def handle_adding_domain_info():
      request_body = request.get_json()
      full_name = request_body('full_name')
      email = request_body('email')
      address = request_body('address')
      phone_number = request_body('phone_number')
      
    #   adding more code to scramble the credit card number 
      donation_info = DontationInfo.query.filter_by(email=email)
      if donation_info is not None:
          return jsonify({'message': 'User already exists'}), 400
      
      new_donation_info = DontationInfo(full_name=full_name, email=email, address=address, phone_number=phone_number)
      db.session.add(new_donation_info)
      db.session.commit()
      return jsonify(new_donation_info.serialize()), 201
  
@api.route('/donation_info', methods=["GET"])
# jwt required maybe depending on the relationship between user and donator 
def handle_get_all_domain_info():
    donation_info = DontationInfo.query.all()
    
    if donation_info is not None:
          return jsonify(donation_info), 200
      
    return jsonify({'message': 'User doesn`t exists'}), 400
    
# get each route
@api.route('/dontain_info/<int:id>', methods=["GET"])
# jwt required
def handle_get_each_donation_info(id):
    each_donation_info = DontationInfo.filter_by(id=id).first()
    
    return jsonify(each_donation_info.serialize())
    
