# Select Queries Here

# 1) user table
select_user_by_id = "SELECT * FROM user WHERE uid=?"
select_all_users = "SELECT * FROM user"
login = "SELECT role_id FROM user WHERE uid=? AND pswd=?"
# 2) customer table
select_cust_by_id = "SELECT * FROM customer WHERE cid=?"
select_all_cust = "SELECT * FROM customer"


# 3) employee table
select_emp_by_id = "SELECT * FROM employee WHERE eid=?"
select_all_emp = "SELECT * FROM employee"


# 4) role table
select_role_by_id = "SELECT * FROM role WHERE rid=?"
select_all_role = "SELECT * FROM role"


# 5) subscription table
select_subs_by_id = "SELECT * FROM subscription WHERE sid=?"
select_all_subs = "SELECT * FROM subscription"


# 6) tarrif_plan table
select_plan_by_id = "SELECT * FROM tarrif_plan WHERE pid=?"
select_all_plan = "SELECT * FROM tarrif_plan"


# 7) usage table
select_usage_by_id = "SELECT * FROM usage WHERE sid=?"
select_all_usage="SELECT * FROM usage"

# 8) customer_bill table
select_bill_by_sid = "SELECT * FROM customer_bill WHERE sid=?"
select_bill_by_cid = """SELECT *
                         FROM customer_bill
                         WHERE sid IN (
                                 SELECT b.sid
                                 FROM customer_bill b
                                 WHERE 1 = IIF(b.payment_date IS NOT NULL, IIF(b.payment_date < b.last_billed, CAST(1 AS BIT), CAST(0 AS BIT)), IIF(b.billing_cycle > 1, CAST(1 AS BIT), CAST(0 AS BIT)))
                                 )"""
total_bill_cost_for_cid = "SELECT SUM(total_cost) FROM customer_bill WHERE cid=?"
is_defaulter = """SELECT IIF(b.payment_date IS NOT NULL, IIF(b.payment_date < b.last_billed, CAST(1 AS BIT), CAST(0 AS BIT)), IIF(b.billing_cycle > 1, CAST(1 AS BIT), CAST(0 AS BIT)))
                  FROM customer_bill b
                  WHERE b.sid = ?"""
is_bill_present = """SELECT CASE 
                     WHEN EXISTS (
                             SELECT *
                             FROM customer_bill
                             WHERE sid = ?
                             )
                         THEN CAST(1 AS BIT)
                     ELSE CAsT(0 AS BIT)
                     END"""
select_due_amount_for_defaulter = """SELECT (IFNULL(b.total_cost, 0) + IFNULL(b.amount_due, 0))
                                     FROM customer_bill b
                                     WHERE sid = ?"""

# 9) VIEW : [subscription_by_customer] usage details - for customer
select_all_subs_details = "SELECT * FROM [subscriptions_by_customer]"
select_subs_details_by_sid = "SELECT * FROM [subscriptions_by_customer] where sid=?"
select_subs_details_by_cid = "SELECT * FROM [subscriptions_by_customer] where cid=?"

# 10) VIEW: [bill_details_per_sub]subscription details  - for operator
select_all_usage_details = "SELECT * FROM [bill_details_per_sub]"
select_usage_details_by_sid_operator = "SELECT * FROM [bill_details_per_sub] where sid=?"
select_usage_details_by_sid_customer = """SELECT sid
                                                ,pid
                                                ,name
                                                ,subscribed_on
                                                ,last_billed
                                                ,voice_usage
                                                ,data_usage
                                                ,billing_cycle
                                        FROM [bill_details_per_sub]
                                        WHERE sid = ?"""
select_usage_details_by_cid_operator = "SELECT * FROM [bill_details_per_sub] where cid=?"
select_usage_details_by_cid_customer = """SELECT sid
                                                ,pid
                                                ,name
                                                ,subscribed_on
                                                ,last_billed
                                                ,voice_usage
                                                ,data_usage
                                                ,billing_cycle
                                        FROM [bill_details_per_sub]
                                        WHERE cid = ?"""

