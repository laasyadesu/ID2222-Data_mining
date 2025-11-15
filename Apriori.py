from collections import Counter
from itertools import combinations

class Apriori:

    def __init__(self, s_threshold, data):
        self.s_threshold = s_threshold
        self.data = data
        self.dataset = []
        self.handle_data(data)
    
    def handle_data(self, data):
        with open(data, "r") as dataFile:
            lines = dataFile.readlines()
        # Process the lines into a dataset
        for line in lines:
            line = line.strip()
            if not line:
                continue
            self.dataset.append(set(line.split()))
        print(self.dataset[0:5])
    
    def support(self, itemset):
        count = 0
        for transaction in self.dataset:
            if itemset.issubset(transaction):
                count += 1
        return count / len(self.dataset)
        

    def gen_item_sets_singleton(self):
        # Flatten the list of transactions to count item frequencies
        flat_items = [item for transaction in self.dataset for item in transaction]
        # Count the occurrences of individual items
        count = Counter(flat_items)
        # Filter by the support threshold
        frq_singleton = {item:i for item, i in count.items() if self.support({item}) >= self.s_threshold}
        return frq_singleton
    
    def gen_item_sets(self, candidate_sets):
        frequent_sets = {}
        for candidate in candidate_sets:
            itemset = set(candidate)
            sup = self.support(itemset)
            if sup >= self.s_threshold:
                frequent_sets[frozenset(itemset)] = sup
        return frequent_sets

    def gen_candidate_sets(self, prev_frequent_sets, k):
        candidate_sets = []
        for i in range(len(prev_frequent_sets)):
            for j in range(i+1, len(prev_frequent_sets)):
                candidate = prev_frequent_sets[i].union(prev_frequent_sets[j])
                if self.support(candidate) >= self.s_threshold and len(candidate) == k:
                    candidate_sets.append(candidate)
        return list({frozenset(c) for c in candidate_sets})
                    
        #return list (combinations(prev_frequent_sets, k))

    def main(self):
        curr_frq = self.gen_item_sets_singleton()
        print(curr_frq)
        curr_frq_sets = [set([item]) for item in curr_frq]

        k = 2

        while True:
            frq_sets=self.gen_candidate_sets(curr_frq_sets, k)
            print(frq_sets)
            frequent_sets = self.gen_item_sets(frq_sets)
            if  len(frequent_sets) == 0:
                break
            print(f'final itemsets {frequent_sets}')
            curr_frq_sets = list(frequent_sets.keys())
            k+=1

if __name__ == "__main__":
    apriori = Apriori(0.4, "data.dat")  # Set the support threshold as desired
    apriori.main()

