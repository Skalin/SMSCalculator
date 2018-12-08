import sys
import getopt
import pandas
from sms_prices import SMS


def main(argv):

    file = ''
    charge = 5  # charge for withdrawal in percents

    try:
        opts, args = getopt.getopt(argv, "f:", ["file="])
    except getopt.GetoptError:
        print('Unrecognized params')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--f"):
            file = arg
        if opt in ("-c", "--c"):
            charge = arg

    sum = {'CZK': 0, 'EUR': 0}
    sum_sms = {'CZK': 0, 'EUR': 0}

    currency_course = {'CZK': 1, 'EUR': 25}
    credit_course = {'CZK': 0.7, 'EUR': 0.647}
    charge_percents = 1 - (charge/100)

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

        for currency in currency_course:
            if sum_sms[currency]:
                print('======================================================================================')
                print('MENA: '+currency)
                print('======================================================================================')
                print('Celkova cena z SMS pro kontrolu (porovnat se sumou z MySQL): ' + str(sum_sms[currency]))
                print('Realna cena z SMS: ' + str(sum[currency] * currency_course[currency]))
                print('Realna cena po odecteni 5% poplatku: ' + str(sum[currency] * currency_course[currency] * charge_percents))
                print('Suma kreditu pro kontrolu (porovnat se sumou z MySQL): ' + str(sum_sms[currency] * credit_course[currency]))
                print('======================================================================================')

    else:
        print('File not specified')
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
