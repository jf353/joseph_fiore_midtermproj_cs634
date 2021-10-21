import csv

# Get User input
print("What dataset would you like to use the apriori algorithm for?")
print("\t1. Amazon")
print("\t2. Best Buy")
print("\t3. K-Mart")
print("\t4. Nike")
print("\t5. Generic")

dataset_num = input("Please enter the number of the dataset you want: ")
while not dataset_num.isnumeric() or int(dataset_num) < 1 or int(dataset_num) > 5:
    if not dataset_num.isnumeric():
        print("Input must be an integer")
    else:
        print("Input must be the number for one of the following datasets:")
        print("\t1. Amazon")
        print("\t2. Best Buy")
        print("\t3. K-Mart")
        print("\t4. Nike")
        print("\t5. Generic")
    dataset_num = input("Please enter a number corresponding to one of the listed datasets: ")

trans_file = ''

if dataset_num == '1':
    trans_file = 'amazon_ex_trans.csv'
elif dataset_num == '2':
    trans_file = 'bestbuy_ex_trans.csv'
elif dataset_num == '3':
    trans_file = 'kmart_ex_trans.csv'
elif dataset_num == '4':
    trans_file = 'nike_ex_trans.csv'
else:
    trans_file = 'generic_ex_trans.csv'

print('')
support_s = input("Please enter your desired support (between 0.0 and 1.0): ")
while True:
    try:
        if float(support_s) < 0 or float(support_s) > 1:
            print("Input must be between 0.0 and 1.0")
        else:
            break
    except ValueError:
        print("Input must be a number")
    support_s = input("Please enter your desired support (between 0.0 and 1.0): ")

support = float(support_s)

print('')
confidence_s = input("Please enter your desired confidence (between 0.0 and 1.0): ")
while True:
    try:
        if float(confidence_s) < 0 or float(confidence_s) > 1:
            print("Input must be between 0.0 and 1.0")
        else:
            break
    except ValueError:
        print("Input must be a number")
    confidence_s = input("Please enter your desired confidence (between 0.0 and 1.0): ")

confidence = float(confidence_s)

# DO APRIORI

# Get 1-Itemsets with support
supported_k_itemsets = {}
counts = {}
transaction_num = 0
with open(trans_file, newline='', encoding='utf-8-sig') as csvfile:
    transreader = csv.reader(csvfile, dialect='excel')
    for transaction in transreader:
        items = transaction[1].split(',')
        for item in items:
            if tuple([item.strip()]) in counts.keys():
                counts[tuple([item.strip()])] += 1
            else:
                counts[tuple([item.strip()])] = 1
        transaction_num += 1

supported_k_itemsets[1] = {}
for entry in counts.keys():
    if counts[entry] / transaction_num >= support:
        supported_k_itemsets[1][entry] = counts[entry]

# Get k-Itemsets with support where k >= support
current_k = 2
while True:
    supported_k_itemsets[current_k] = {}
    counts.clear()
    possible_k_sets = set()
    for i in range(0,len(supported_k_itemsets[current_k - 1].keys())-1):
        for j in range(i+1,len(supported_k_itemsets[current_k - 1].keys())):
            itemset_a = list(supported_k_itemsets[current_k - 1].keys())[i]
            itemset_b = list(supported_k_itemsets[current_k - 1].keys())[j]
            possible_new_itemset = list(set(itemset_a) | set(itemset_b))
            if len(possible_new_itemset) == current_k:
                possible_new_itemset.sort()
                possible_k_sets.add(tuple(possible_new_itemset))

    with open(trans_file, newline='', encoding='utf-8-sig') as csvfile:
        transreader = csv.reader(csvfile, dialect='excel')
        for transaction in transreader:
            items = [x.strip() for x in transaction[1].split(',')]
            for possible_set in possible_k_sets:
                if set(possible_set).issubset(items):
                    if possible_set in counts.keys():
                        counts[possible_set] += 1
                    else:
                        counts[possible_set] = 1

    for entry in counts.keys():
        if counts[entry] / transaction_num >= support:
            supported_k_itemsets[current_k][entry] = counts[entry]

    if len(supported_k_itemsets[current_k].keys()) == 0:
        break
    current_k += 1

#Get a list of all the supported itemsets for ease of use, also print them
print("Itemsets With Required Support")
print("------------------------------------------")
supported_itemsets = []
for k in supported_k_itemsets.keys():
    for itemset in supported_k_itemsets[k].keys():
        supported_itemsets.append(itemset)
        print(str(set(itemset)) + "\t\t{supp:.2f}%".format(supp = (supported_k_itemsets[k][itemset] / transaction_num) * 100))
print("------------------------------------------", end ="\n\n")

#Find all associations with confidence
associations = {}
for itemset in supported_itemsets:
    for itemset_b in supported_itemsets:
        if itemset == itemset_b:
            continue
        second_set = tuple(set(itemset) | set(itemset_b))
        count_of_one = supported_k_itemsets[len(itemset)][itemset]
        count_of_two = 0
        if len(second_set) in supported_k_itemsets.keys() and second_set in supported_k_itemsets[len(second_set)].keys():
            count_of_two = supported_k_itemsets[len(second_set)][second_set]
        else:
            with open(trans_file, newline='', encoding='utf-8-sig') as csvfile:
                transreader = csv.reader(csvfile, dialect='excel')
                for transaction in transreader:
                    items = [x.strip() for x in transaction[1].split(',')]
                    if set(second_set).issubset(items):
                        count_of_two += 1
        if count_of_two / count_of_one >= confidence:
            associations[tuple([itemset, itemset_b])] = count_of_two / count_of_one 

#Print all associations with enough Confidence
print("Associations With Required Confidence")
print("------------------------------------------")
for association in associations.keys():
    a = list(association)
    print(str(set(a[0])) + "->" + str(set(a[1])) + "\t\t{conf:.2f}%".format(conf = associations[association] * 100))
print("------------------------------------------", end ="\n\n")
