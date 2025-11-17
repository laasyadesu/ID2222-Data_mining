from collections import Counter
from itertools import combinations

class Apriori:

    def __init__(self, s_threshold, c_threshold, data):
        self.s_threshold = s_threshold
        self.c_threshold = c_threshold
        self.data = data
        self.dataset = []
        self.frequent_itemsets = {} # To store all frequent itemsets and their support
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

    def generate_association_rules(self):  
        rules = []

        #itemset is the main big set
        
        for itemset, support_itemset in self.frequent_itemsets.items():
            if len(itemset) > 1:
                # all non-empty proper subsets of the itemset
                for i in range(1, len(itemset)):
                    for set_X in combinations(itemset, i):
                        set_X = frozenset(set_X)
                        set_Y = itemset - set_X

                        # Confidence(A->C) = Support(A U C) / Support(A)
                        # (A U C) is the original itemset
                        set_X_support = self.frequent_itemsets.get(set_X)
                        
                        if set_X_support:
                            confidence = support_itemset / set_X_support
                            if confidence >= self.c_threshold:
                                rule = (set_X, set_Y, confidence)
                                rules.append(rule)
                                print(f"Rule: {set_X} -> {set_Y}, confidence: {confidence:.2f}")
                                
        return rules



    def main(self):
        # Start with 1-itemsets (singleton), then increase size of itemset.
        curr_frq_singletons = self.gen_item_sets_singleton()
        singleton_sets = {frozenset([item]): self.support({item}) for item in curr_frq_singletons}
        self.frequent_itemsets.update(singleton_sets)
        
        curr_frq_sets = [set([item]) for item in curr_frq_singletons]
        k = 2

        while True:
            # Get candidate sets of size k
            candidate_sets = self.gen_candidate_sets(curr_frq_sets, k)
            if not candidate_sets:
                break
            
            # Remove candidates set of current size k to get frequent k-itemsets
            frequent_sets_k = self.gen_item_sets(candidate_sets)
            if not frequent_sets_k:
                break
            
            print(f"No. of frequent {k}-itemsets: {len(frequent_sets_k)}")
            
            self.frequent_itemsets.update(frequent_sets_k)           
            curr_frq_sets = list(frequent_sets_k.keys())
            k += 1
        
        # generate rules
        self.generate_association_rules()


if __name__ == "__main__":
    # Set the support and confidence thresholds as desired
    apriori = Apriori(s_threshold=0.3, c_threshold=0.6, data="T10I4D100K.dat")  
    apriori.main()

