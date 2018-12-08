import sys, getopt
import pandas
from sms_prices import SMS


def main(argv):

    file = ''
    try:
        opts, args = getopt.getopt(argv, "f:", ["file="])
    except getopt.GetoptError:
        print('Unrecognized params')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--f"):
            file = arg

    sum = {'CZK': 0, 'EUR': 0}
    sum_sms = {'CZK': 0, 'EUR': 0}
    credit_sum = {'CZK': 0, 'EUR': 0}

    currency_course = {'CZK': 1, 'EUR': 25}

    if len(file):
        lines = pandas.read_csv(file, usecols=['currency', 'phone_operator', 'amount'])
        for i in range(0, len(lines)):
            operator = lines.iloc[i].phone_operator
            currency = lines.iloc[i].currency
            price = lines.iloc[i].amount
            if currency == 'CZK':
                real_price = SMS[currency][operator][price]
                sum_sms[currency] += price
                sum[currency] += real_price
                credit_sum[currency] += price*0.7

    for currency in currency_course:
        print('======================================================================================')
        print('MENA: '+currency)
        print('======================================================================================')
        print('Celkova cena z SMS pro kontrolu (porovnat se sumou z MySQL): ' + str(sum_sms[currency]))
        print('Realna cena z SMS: ' + str(sum[currency] * currency_course[currency]))
        print('Realna cena po odecteni 5% poplatku: ' + str(sum[currency] * currency_course[currency] * 0.95))
        print('Suma kreditu pro kontrolu (porovnat se sumou z MySQL): ' + str(credit_sum[currency]))
        print('======================================================================================')


if __name__ == "__main__":
    main(sys.argv[1:])
