"""Credit Card Simulator
Author: Vanessa Lu.  Last modified: Oct. 12, 2022
"""

def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    global MONTHLY_INTEREST_RATE

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = 0, 0

    last_country = None
    last_country2 = None

    card_disabled = False

    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    '''Check if day1 and month1 is later than or is the same date as day2 and month2
        Return True iff (day1, month1) is the same as (day2, month2) or is later than (day2, month2)
        Assumptions: day1, month1, day2, and month2 are valid dates in 2020'''
    if month1 < month2:   #if month1 is smaller than month2, immediatly return false as it occurs before month2
        return False
    elif month1 > month2: #if month1 is larger than month2, immediately return true as it occurs after month2
        return True
    else:                 #if the months are the same, check if day1 is the same as or after day2
        if (day1 == day2 or day1 > day2): #if day1 is either the same or after day2, return true
            return True
        else:             #if day1 is neither, return false as it therefore occurs before the date (day2, month2)
            return False

def all_three_different(c1, c2, c3):
    '''Check if c1, c2, and c3 are all different strings
        Return True iff the values of the three strings c1, c2, and c3 are different from each other
        Assumptions: strings c1, c2, and c3 are valid country names'''
    if (c1 != c2 and c2 != c3 and c1 != c3 and c3 != None):
        return True
    else:
        return False

def purchase(amount, day, month, country):
    '''Simulate a purchase (amount), on the date (day, month), in a country (country)
        Return the string "error" and possibly disable the card
        Assumptions: amount > 0 and country != null (e.g. valid country name)'''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled

    if card_disabled:   #if fraud is detected, return string "error" immediately, purchase does not go through
        return "error"
    if not all_three_different(country, last_country, last_country2): #if no fraud detected
        if date_same_or_later(day, month, last_update_day, last_update_month):
        #if the date is valid (i.e. same as or after last recorded date)
            if month > last_update_month: #iff one or more months have passed since last recorded date, then:
                update_balances(month)    #applies interest accordingly and switches to a new current month balance
            cur_balance_owing_recent += amount #adds amount to current month (non-interest) balance
            update_date(day, month)       #updates last recorded date to current date
            update_country(country)       #updates last two consecutive countries to compare for fraud
        else:
            update_country(country)       #regardless of whether the date is valid or not, last two consecutive countries
                                          #are still updated to compare for fraud
            return "error"
    else:
        update_country(country)           #if fraud is detected, only update the country list
        card_disabled = True              #disable the card
        return "error"

def amount_owed(day, month):
    '''Return the amount owed as of the date (day, month) or return the string "error" if the date is invalid'''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month):
        if month > last_update_month:     #if one or more months have passed since last recorded date:
            update_balances(month)        #update balances with interest
        update_date(day, month)           #update the last recorded date to current date
        return cur_balance_owing_intst + cur_balance_owing_recent   #return the total of both balances
    else:
        return "error"

def pay_bill(amount, day, month):
    '''Simulate the payment of the amount owed on the credit card. The payment first goes to pay the interest-owing
        balance, then to pay the non-interest-owing balance.
        Returns the string "error" if the date is invalid
        Assumptions: amount > 0'''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month):
        tot_bal = amount_owed(day, month)   #calculate total balance owed
        if amount >= tot_bal:
            cur_balance_owing_intst = 0.0   #since amount paid is greater than or eqaual to total balance, set both
            cur_balance_owing_recent = 0.0  #balances to 0 as all owed balance has been paid
            amount = 0.0
        else:
            if amount < cur_balance_owing_intst:
                cur_balance_owing_intst -= amount   #subtract amount from interest-owing balance only
                amount = 0.0
            else:                                   #if amount is greater than interest-owing balance,
                temp = cur_balance_owing_intst
                cur_balance_owing_intst = 0.0       #pay off all interest-owing balance and
                amount -= temp                      #subtract previous int-owing balance from amount paid
                cur_balance_owing_recent -= amount  #subtract the remaining amount from non-int balance
                amount = 0.0
        update_date(day, month)       #updates last recorded date to current date
    else:
        return "error"

def update_balances(new_month):
    '''Updates both the interest-owing and non-interest owing balances and applies interest to any int-owing balance'''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month

    #calculate the number of months that have passed since last recorded date
    month_gap = new_month - last_update_month

    #if only one month has passed since last recorded date, interest is only applied to cur_balance_owing_intst, then
    #cur_balance_owing_recent is switched over (added to) cur_balance_owing_intst
    if (new_month - last_update_month == 1):
        #apply one month's interest to the balance owing interest
        cur_balance_owing_intst *= (1 + MONTHLY_INTEREST_RATE)
        #add the former non-interest owing balance to the interest-owing balance
        cur_balance_owing_intst += cur_balance_owing_recent
        #reset current month's balance to 0
        cur_balance_owing_recent = 0
    else:
        #apply interest to the balance owing interest according to above time period
        cur_balance_owing_intst *= pow((1 + MONTHLY_INTEREST_RATE), month_gap) #multipl
        #apply one month less of interest to the former non-interest balance
        cur_balance_owing_recent *= pow((1 + MONTHLY_INTEREST_RATE), month_gap - 1)
        #add the former non-interest owing balance to the interest-owing balance
        cur_balance_owing_intst += cur_balance_owing_recent
        #reset current month's balance to 0
        cur_balance_owing_recent = 0

def update_date(day, month):
    '''Updates last recorded date (last_update_day, last_update_month) to current date (day, month)'''
    global last_update_day, last_update_month
    last_update_day = day
    last_update_month = month

def update_country(country):
    '''Updates last two consecutive countries to include the country country'''
    global last_country, last_country2
    last_country2 = last_country
    last_country = country

# Initialize all global variables outside the main block.
initialize()