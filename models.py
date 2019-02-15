from pony import orm

db = orm.Database()


class Planning(db.Entity):
    title = orm.Required(str)
    password = orm.Required(str)
    stories = orm.Set('Story')


class Story(db.Entity):
    planning = orm.Required(Planning)
    name = orm.Required(str)
    estimates = orm.Set('Estimate')


class Estimate(db.Entity):
    story = orm.Required(Story)
    est_user = orm.Optional(str)
    estimate = orm.Optional(str)
    est_comment = orm.Optional(str)
