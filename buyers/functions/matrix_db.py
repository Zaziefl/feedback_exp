import sys
print (sys.path)



# from numpy import random
# import sqlite3 as sl
# import os
#
# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
# from sqlalchemy.orm import relationship, Session, sessionmaker
# from sqlalchemy import create_engine, select
# from sqlalchemy.ext.declarative import declarative_base
#
#
# Base = declarative_base()
#
#
# class SamplingMatrix(Base):
#     __tablename__ = "matrix"
#
#     id = Column(Integer, primary_key=True)
#     inuse = Column(Boolean)
#     players = Column(Integer)
#     played = Column(Integer)
#     condition = Column(Integer)
#     values = Column(Integer)
#     for i in range(16):
#         exec('pr%s = Column(Integer)' % i)
#         exec('neur%s = Column(Integer)' % i)
#         exec('nr%s = Column(Integer)' % i)
#     del i
#
#     def __repr__(self):
#         return f"Matrix(id={self.id!r}, inuse={self.inuse!r}, \
#                players={self.players!r}, played={self.played!r}, \
#                condition={self.condition!r}, values={self.values!r})"
#     pass
#
#
# class MatrixParticipant(Base):
#     __tablename__ = "matrix_participant"
#     id = Column(Integer, primary_key=True)
#     matrix_id = Column(Integer, ForeignKey("matrix.id"), nullable=False)
#     participant_id = Column(Integer, nullable=False)
#     item_id = Column(Integer)
#
#     def __repr__(self):
#         return f"MatrixParticipant(id={self.id!r}, inuse={self.matrix_id!r}), \
#                participant_id={self.participant_id!r})"
#
# # run to initialize matrix
# # file_path = os.path.abspath(os.getcwd()) + "\matrices.db"
# # engine = create_engine('sqlite:///' + file_path, echo=True)
# # Base.metadata.create_all(engine)
#
# class MatrixManager:
#     Base = declarative_base()
#
#     def __init__(self):
#         self.Base = declarative_base()
#         file_path = os.path.abspath(os.getcwd()) + "/matrices.db"
#         self.engine = create_engine('sqlite:///' + file_path, echo=True)
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()
#
#     def reset(self):
#         self.session.query(MatrixParticipant).delete(synchronize_session='fetch')
#         self.session.commit()
#         self.session.query(SamplingMatrix).delete()
#         self.session.commit()
#         for i in range(12):
#             self.add_matrix(12)
#         self.session.commit()
#         pass
#
#
#     def add_matrix(self, players):
#         values = 0
#         for condition in range(4):
#             for i in range(15):
#                 val = random.binomial(1, .8)  # Specify probability
#                 values += pow(val, i) * val
#             self.session.add(SamplingMatrix(inuse=False, players=players, played=0, condition=condition, values=values,
#                                        pr0=0, pr1=0, pr2=0, pr3=0, pr4=0, pr5=0, pr6=0, pr7=0, pr8=0, pr9=0, pr10=0,
#                                        pr11=0, pr12=0, pr13=0, pr14=0, pr15=0, neur0=0, neur1=0, neur2=0, neur3=0,
#                                        neur4=0, neur5=0, neur6=0, neur7=0, neur8=0, neur9=0, neur10=0, neur11=0,
#                                        neur12=0, neur13=0, neur14=0, neur15=0, nr0=0, nr1=0, nr2=0, nr3=0, nr4=0, nr5=0,
#                                        nr6=0, nr7=0, nr8=0, nr9=0, nr10=0, nr11=0, nr12=0, nr13=0, nr14=0, nr15=0))
#         self.session.commit()
#         pass
#
#     def sample_matrix(self, condition, participant):
#         Session = sessionmaker(bind=self.engine)
#         session = Session()
#         matrices_played = session.query(MatrixParticipant.matrix_id).filter_by(participant_id=participant).all()
#         matrices_played_list = [r[0] for r in matrices_played]
#         list_possmatrix = session.query(SamplingMatrix).filter_by(condition=condition).\
#             filter(SamplingMatrix.id.notin_(matrices_played_list)).all()
#         if len(list_possmatrix) == 1:
#             sampled_matrix = list_possmatrix[0]
#         else:
#             sampled_matrix = list_possmatrix[random.randint(0, len(list_possmatrix) - 1)]
#         sampled_matrix.inuse = True
#         session.commit()
#         print("Matrix " + str(sampled_matrix.id) + " given to participant " + str(participant) + ".")
#         return sampled_matrix
#
#     def return_matrix(self, participant, matrix, item, rating, publish):
#         Session = sessionmaker(bind=self.engine)
#         session = Session()
#         return_matrix = session.query(SamplingMatrix).filter_by(id=matrix).all()[0]
#         return_matrix.players -= 1
#         return_matrix.played += 1
#         return_matrix.inuse = 0
#         if publish:
#             if rating == 1:
#                 exec("return_matrix.pr%s += %d" % (item, 1))
#             else:
#                 if rating == 0:
#                     exec("return_matrix.neur%s += %d" % (item, 1))
#                 else:
#                     exec("return_matrix.nr%s += %d" % (item, 1))
#         session.add(MatrixParticipant(matrix_id=matrix, participant_id=participant, item_id=item))
#         session.commit()
#         pass
#
#     def calculate_owner_payoff(self, participant):
#         Session = sessionmaker(bind=self.engine)
#         session = Session()
#         chosen_matrices = session.query(MatrixParticipant).filter(MatrixParticipant.participant_id != participant).all()
#         payoff = 0
#         for i in range(5):
#             if len(chosen_matrices) == 0:
#                 payoff += .1
#             else:
#                 if len(chosen_matrices) == 1:
#                     random_number = 1
#                 else:
#                     random_number = random.randint(0, len(chosen_matrices)-1)
#                 if (random.randint(0, 1) == 1 and chosen_matrices[random_number].item_id > 7) or (random.randint(0, 1)== 0 and chosen_matrices[random_number].item_id < 8):
#                     payoff += .1
#         session.commit()
#         return payoff
#
#
# pass
#
# # Run to test script
# # mm = MatrixManager()
# # mm.reset()
# # sm = mm.sample_matrix(0,0)