from flask_sqlalchemy import SQLAlchemy
import arrow

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.Text)
    longname = db.Column(db.Text)
    rank = db.Column(db.Integer)
    when = db.Column(db.DateTime)

    @classmethod
    def get_all_groups(cls):
        return cls.query.order_by(Group.when.desc()).all()

    @classmethod
    def add_group(cls, groupid, longname, rank):
        group = Group()
        group.groupid = groupid
        group.longname = longname
        group.rank = rank
        group.when = arrow.utcnow().datetime
        db.session.add(group)
        db.session.commit()
        return

    @classmethod
    def get_group_by_group_id(cls, group_id):
        return cls.query.filter(Group.groupid == group_id).first()
