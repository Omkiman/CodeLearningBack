from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CodeBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.String(200), nullable=False)