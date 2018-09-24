class PairGenerator():
    def __init__(this,list_of_people) :
        this.list_of_people = list_of_people

    def can_add(this, list, pair):
        for e in list:
            if pair[0] in e or pair[1] in e:
                return False
        return True

    def generate_pairs(this):
        all_possible_pairs = []
        all_possible_pairs_lists = []
        for j in range(len(this.list_of_people) - 1):
            one_possiblity_pairing = []
            for i in range(j + 1, len(this.list_of_people)):
                one_possiblity_pairing.append((this.list_of_people[j], this.list_of_people[i]))
            all_possible_pairs_lists.append(one_possiblity_pairing)
        for pair_list in all_possible_pairs_lists:
            for pair in pair_list:
                all_possible_pairs.append(pair)
        return all_possible_pairs[::-1]

    def generate_all_combinations(this):
        all_combinations = []
        pairs = this.generate_pairs()
        for i in range(0, len(pairs)):
            combinations_with_current_pair = []
            remaining_pairs = [e for e in pairs]
            while len(combinations_with_current_pair) != len(this.list_of_people) / 2:
                combination = [pairs[i]]
                j = i + 1
                while(j < len(remaining_pairs)):
                    current_pair = remaining_pairs[j]
                    if this.can_add(combination, current_pair):
                        combination.append(current_pair)
                        remaining_pairs.remove(current_pair)
                        j -= 1
                    j += 1
                print(combination)
                combinations_with_current_pair.append(combination)
            all_combinations.append(combinations_with_current_pair)
        return all_combinations

pairGenerator = PairGenerator(["A", "B", "C", "D", "E", "F"])
all_combinations = pairGenerator.generate_all_combinations()
# for combination in all_combinations:
#     print(combination)
