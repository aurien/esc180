"""
Skeleton: Michael Guerzhoy.  Last modified: Oct. 3, 2022
By: Sarah Zhao and Christine Lee
"""
from ftplib import all_errors

def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country1, last_country2
    global activated

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = 0, 0

    last_country1 = ""
    last_country2 = ""

    activated = True

    MONTHLY_INTEREST_RATE = 1.05

def date_same_or_later(day1, month1, day2, month2):
# This function returns True iff the date (day1, month1) is the same as the date (day2, month2), or occurs later than (day2, month2). Assume the dates given are valid dates in the year 2020.
    if month1 == month2:
        if day1 == day2 or day1 > day2:
            return True
        else:
            return False
    elif month1 > month2:
        return True
    else:
        return False

def all_three_different(c1, c2, c3):
    if c1 == "" or c2 == "" or c3 == "":
        return False
    return c1 != c2 and c1 != c3 and c2 != c3

def update_intst(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_month, last_update_day
    month_difference = month - last_update_month
    if month != last_update_month:  # thus only changes if the month changes
        cur_balance_owing_intst *= 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_recent = 0
        cur_balance_owing_intst *= 1.05**(month_difference-1)
    last_update_month = month
    last_update_day = day

def purchase(amount, day, month, country):
    global last_country2, last_country1, activated, cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month) and (not all_three_different(last_country2, last_country1, country) or last_country2 == "") and activated:
        update_intst(day, month)
        cur_balance_owing_recent += amount
        last_country2 = last_country1
        last_country1 = country
        last_update_month = month
        last_update_day = day
    if all_three_different(last_country2, last_country1, country):
        activated = False
    return "error"

def amount_owed(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month):
        update_intst(day, month)
        return cur_balance_owing_intst + cur_balance_owing_recent
    elif not date_same_or_later(day, month, last_update_day, last_update_month):
        return "error"

def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month):
        update_intst(day, month)
        if amount > cur_balance_owing_intst + cur_balance_owing_recent:
            return "error"
        elif amount > cur_balance_owing_intst:
            cur_balance_owing_recent = cur_balance_owing_recent - (amount - cur_balance_owing_intst)
            cur_balance_owing_intst = 0
        elif amount <= cur_balance_owing_intst:
            cur_balance_owing_intst -= amount
    return "error"

def check_cases(result, answer):
    '''Function is to test whether or not credit.py is valid.'''
    if result == answer:
        return "Passed"
    return "Failed"

if __name__ == "__main__":
    #Test for Disable Card
    initialize()
    purchase(100, 1, 1, "China")    #100
    purchase(100, 1, 1, "Chile")    #100
    purchase(100, 1, 1, "Canada")   
    print("Case 1", check_cases(amount_owed(1,1), 200))

    #Test pay more than balance
    initialize()
    purchase(100, 1, 1, "France")
    purchase(100, 4, 1, "Chile")
    pay_bill (400, 5, 1)
    print ("Case 2", check_cases(amount_owed(5,1), 200))

    #Test for paying back bill after disabled card
    initialize()
    purchase (100, 1, 1, "Algeria")
    purchase (100, 5, 3, "Peru")
    purchase (100, 2, 6, "Oman")
    pay_bill (100, 3, 6)
    print ("Case 3", check_cases(amount_owed(3, 6), 131.800625))
    
    #Test for dates failing, purchase()
    initialize()
    purchase (100, 1, 12, "Jamaica")    #go through
    purchase (200, 3, 5, "Egypt")      #fail -- date is too early, nothing should happen. card is not disabled.
    purchase (400, 12, 12, "Zambia")    #go through
    purchase (100, 11, 12, "Russia")    #disable card
    purchase (100, 14, 12, "Russia")    #disable card
    print ("Case 4", check_cases(amount_owed(14, 12), 500))

    #Test for dates failing, pay_bill()
    initialize()
    purchase(100, 13, 1, "Tuvalu")
    pay_bill(10, 5, 1)
    print("Case 5", check_cases(amount_owed(13, 1), 100))
    pay_bill(10, 14, 1)
    print("Case 6", check_cases(amount_owed(14, 1), 90))

    #Test for pay_bill() before purchase()
    initialize()
    pay_bill (200, 12, 1)
    print ("Case 7", check_cases(amount_owed(12, 1), 0))        
    purchase(100, 23, 1, "Indonesia")
    pay_bill(200, 3, 1) 
    purchase(200, 1, 5, "Armenia")
    purchase(100, 3, 6, "South Sudan")
    print("Case 8", check_cases(amount_owed(3, 6), 321.550625))

    
