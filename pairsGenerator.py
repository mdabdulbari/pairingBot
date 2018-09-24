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
                combinations_with_current_pair.append(combination)
            all_combinations.append(combinations_with_current_pair)
        valid_combinations = []
        for list1 in all_combinations:
            for list2 in list1:
                if(len(list2) == len(this.list_of_people) / 2):
                    valid_combinations.append(list2)
        return valid_combinations

    def can_add_list(this, first_list, second_list):
        for first_pair in first_list:
            for second_pair in second_list:
                if first_pair == second_pair:
                    return False
        return True

    def can_add_to_big_list(this, big_list, second_list):
        for a_list in big_list:
            if this.can_add_list(a_list, second_list) == False:
                return False
        return True

    def final_combinations(this):
        final_combinations = []
        all_combinations = this.generate_all_combinations()
        for i in range(0, len(all_combinations)):
            temporory_combinations = [all_combinations[i]]
            for j in range(i + 1, len(all_combinations)):
                current_combination = all_combinations[j]
                if(this.can_add_to_big_list(temporory_combinations, current_combination)):
                    temporory_combinations.append(current_combination)
            if(len(temporory_combinations) == len(this.list_of_people) - 1):
                final_combinations.append(temporory_combinations)
        return final_combinations

pairGenerator = PairGenerator(["A", "B", "C", "D", "E", "F"])
final_combinations = pairGenerator.final_combinations()
print(final_combinations)

        