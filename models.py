from myproject import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(200), nullable = False)



if __name__ == '__main__':
    db.create_all()