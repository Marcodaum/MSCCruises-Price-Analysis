from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import scraper
import scraper.scraper
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cruises(db.Model):
    __tablename__ = 'cruises'

    scrape_date = db.Column(db.DateTime, primary_key=True)
    id = db.Column(db.String(16), primary_key=True)

    ship_name = db.Column(db.String(30), unique=False, nullable=False)
    cruise_duration = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    price_per_night = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"Cruise : {self.id}, Price: {self.scrape_date}, Ship: {self.ship_name}, Duration: {self.cruise_duration} days, Price: {self.price} €"
            
    def to_dict(self):
        return {
            'scrape_date': self.scrape_date.isoformat(),
            'id': self.id,
            'ship_name': self.ship_name,
            'cruise_duration': self.cruise_duration,
            'price': self.price,
            'price_per_night': self.price_per_night
        }


def scrape():
    with app.app_context():
        cruises = scraper.scraper.scrape()
        print("Scraping completed. Now storing into database...")
        current_time = datetime.now()



        for cruise in cruises:
            existing_cruise = Cruises.query.filter(
                Cruises.id == cruise.cruise_id
            ).order_by(Cruises.scrape_date.desc()).first()
            if not existing_cruise or existing_cruise.price != int(cruise.price):
                new_cruise = Cruises(
                    scrape_date = current_time,
                    id=cruise.cruise_id,
                    ship_name=cruise.ship_name,
                    cruise_duration=cruise.duration,
                    price=cruise.price,
                    price_per_night=cruise.price_per_night,
                )
                db.session.add(new_cruise)
                print("Cruise added: " + new_cruise.ship_name + " " + str(new_cruise.price) + " €")
            else:
                print("Cruise not added as price did not change")
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape, trigger='cron', hour='14,13')
scheduler.start()

with app.app_context():
    db.create_all()
    #with db.engine.connect() as connection:
    #    connection.execute(text('DROP TABLE cruises'))

@app.route('/cruises', methods=['GET'])
def get_cruises():
    if request.method == 'GET':
        order_by = request.args.get("orderBy")
        no = request.args.get("no")
        # history = int(request.args.get("history", 1))
        query = Cruises.query

        if order_by == "pricePerNight":
            query = query.order_by(Cruises.price_per_night)
        elif order_by == "price":
            query = query.order_by(Cruises.price)
        elif order_by == "duration":
            query = query.order_by(Cruises.cruise_duration)


        if no:
            query = query.limit(no)

        cruises = query.all()
        cruise_list = [cruise.to_dict() for cruise in cruises]
        return jsonify(data=cruise_list)
    
@app.route('/admin/scrape', methods=['POST'])
def manual_scrape():
    scrape()
    return "Scrape triggered successfully!", 200