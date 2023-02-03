import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .models import create_tables, Users, Favourites
from config import userdb, password_db, base_name

DSM = f'postgresql://{userdb}:{password_db}@localhost:5432/{base_name}'
engine = sqlalchemy.create_engine(DSM)
Session = sessionmaker(bind=engine)
session = Session()


def add_parthers_data(user_id, partners, view):  # +
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = Users(users=user_id, partners=partners, view=view)
    session.add(user)
    session.commit()

    print(user.id)
    session.close()


# def add_favourite_data(user_id, partners):  # +
#     create_tables(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     favourites = Favourites(users=user_id, partners=partners)
#     session.add(favourites)
#     session.commit()
#
#     session.close()


def open_partners_data(user_id):
    create_tables(engine)
    last_search = []
    for id in session.query(Users).filter(Users.users == user_id).all():
        result = vars(id)

        # last_search.append(result['users'])
        last_search.append(result['partners'])
        last_search.append(result['view'])
        # last_search = (user_id, last_search)
        # print(last_search)

    # last_search = []
    return last_search  # , user_id


def append_users_base(user_id, user_search):
    # i = user_id
    for i in user_search:
        print(i)
        add_parthers_data(user_id, i, view=False)
