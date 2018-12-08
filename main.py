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

    SUM = {'CZK': 0, 'EUR': 0}
    SUMSMS = {'CZK': 0, 'EUR': 0}
    CREDITSUM = {'CZK': 0, 'EUR': 0}

    if len(file):
        lines = pandas.read_csv(file, usecols=['currency', 'phone_operator', 'amount'])
        for i in range(0, len(lines)):
            operator = lines.iloc[i].phone_operator
            currency = lines.iloc[i].currency
            price = lines.iloc[i].amount
            if currency == 'CZK':
                real_price = SMS[currency][operator][price]
                SUMSMS[currency] += price
                SUM[currency] += real_price
                CREDITSUM[currency] += price*0.7

    print('Celkova cena z SMS pro kontrolu (porovnat se sumou z MySQL): ' + str(SUMSMS['CZK']))
    print('Realna cena z SMS: ' + str(SUM['CZK']))
    print('Realna cena po odecteni 5% poplatku: ' + str(SUM['CZK']*0.95))
    print('Suma kreditu pro kontrolu (porovnat se sumou z MySQL): ' + str(CREDITSUM['CZK']))


if __name__ == "__main__":
    main(sys.argv[1:])
