import sqlite3 as db
import time
import traceback
import sys
from db.scripts import DML,DQL

db_path = './db/dispur_wireless.db'

class BillModel():

    def __init__(self, sid=None, cid=None, pid=None, name=None, tarrif_call=None, tarrif_data=None, validity=None, rental=None, subs_date=None, last_billed=None, voice_usage=None, data_usage=None, call_cost=None, data_cost=None, total_cost=None, billing_cycle=None, payment_date=None, amount_due=None):
        self.sid = sid
        self.cid = cid
        self.pid = pid
        self.name = name
        self.tarrif_call = tarrif_call
        self.tarrif_data = tarrif_data
        self.validity = validity
        self.rental = rental
        self.subs_date = subs_date
        self.last_billed = last_billed
        self.voice_usage = voice_usage
        self.data_usage = data_usage
        self.call_cost = call_cost
        self.data_cost = data_cost
        self.total_cost = total_cost
        self.billing_cycle = billing_cycle
        self.payment_date = payment_date
        self.amount_due = amount_due

    
    #1) Select by sid
    @classmethod
    def find_by_sid(cls, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_bill_by_sid
        result = cursor.execute(query, (sid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                bill = BillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17])
            connection.close()
            return bill

    #2) Select by cid
    @classmethod
    def find_by_cid(cls, cid):
        bill_list = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_bill_by_cid
        result = cursor.execute(query, (cid,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                bill_list.append(BillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]))
            connection.close()
            return bill_list


    #3) Select all
    @classmethod
    def find_all(cls):
        bills = list()
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_all_users
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                bills.append(BillModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]))
            return bills
        connection.close()

    #4) Insert
    @classmethod
    def insert_into_table(cls, sid, cid, pid, name, tarrif_call, tarrif_data, validity, rental, subs_date, last_billed, voice_usage, data_usage, call_cost, data_cost, total_cost, billing_cycle, amount_due):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.insert_bill_by_sid
        try:
            result = cursor.execute(query, (sid, cid, pid, name, tarrif_call, tarrif_data, validity, rental, subs_date, last_billed, voice_usage, data_usage, call_cost, data_cost, total_cost, billing_cycle, amount_due))
            connection.commit()
            connection.close()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False

    #5) Update
    @classmethod
    def update_bill_sid(cls, cid, pid, name, tarrif_call, tarrif_data, validity, rental, subs_date, last_billed, voice_usage, data_usage, call_cost, data_cost, total_cost, billing_cycle, amount_due, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.update_bill_by_sid
        try:
            result = cursor.execute(query, (cid, pid, name, tarrif_call, tarrif_data, validity, rental, subs_date, last_billed, voice_usage, data_usage, call_cost, data_cost, total_cost, billing_cycle, amount_due, sid))
            connection.commit()
            connection.close()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False

    #6) Delete
    @classmethod
    def delete_bill_sid(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.delete_bill_by_sid
        try:
            result = cursor.execute(query, (sid,))
            connection.commit()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False
    
    #unused
    #9) select total bill by cid
    @classmethod
    def total_bill_cid(cls, cid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.total_bill_cost_for_cid
        result = cursor.execute(query, (cid,))
        cost = result.fetchall()
        if cost:
            connection.close()
            return cost
    
    #10) is_defaulter
    @classmethod
    def is_defaulter(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.is_defaulter
        result = cursor.execute(query, (sid,))
        bit = result.fetchall()
        if bit == 1:
            is_defaulter = True
        else:
            is_defaulter = False
        connection.close()
        return is_defaulter    

    #11) is_bill present
    @classmethod
    def is_bill_present(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.is_bill_present
        result = cursor.execute(query, (sid,))
        bit = result.fetchall()
        if bit == 1:
            result = True
        else:
            result = False
        connection.close()
        return result
    
    #12) get total due amount
    @classmethod
    def get_total_due(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DQL.select_due_amount_for_defaulter
        result = cursor.execute(query, (sid,))
        amount = result.fetchall()
        if amount:
            connection.close()
            return amount

    #13) Pay bill
    @classmethod
    def pay_bill(self, sid):
        connection = db.connect(db_path)
        cursor = connection.cursor()
        query = DML.pay_bill
        try:
            result = cursor.execute(query, (sid,))
            connection.commit()
            return True
        except db.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            connection.close()
            return False

    #13) jsonify the model
    def jsonify(self):
        return{
            'subID': self.sid,
            'customerID': self.cid,
            'planID': self.pid,
            'name': self.name,
            'callTarrif': self.tarrif_call,
            'dataTarrif': self.tarrif_data,
            'validity': self.validity,
            'rental': self.rental,
            'subsDate': self.subs_date,
            'lastBilled': self.last_billed,
            'voiceUsage': self.voice_usage,
            'dataUsage': self.data_usage,
            'callCost': self.call_cost,
            'dataCost': self.data_cost,
            'totalCost': self.total_cost,
            'billingCycle': self.billing_cycle,
            'paymentDate': self.payment_date,
            'amount_due': self.amount_due
        }
