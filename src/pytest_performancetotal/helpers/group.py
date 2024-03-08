from itertools import groupby
from operator import itemgetter

class Group:
    def group_by(self, dict_list, attributes):
    # It's necessary to sort the list by the attributes beforehand
        dict_list.sort(key=itemgetter(*attributes))
    
     # groupby() groups the sorted dictionaries by the attributes
        grouped_data = {key: list(group) for key, group in groupby(dict_list, key=itemgetter(*attributes))}
        return grouped_data

# Example usage:
# Group by 'type' and 'color'
# grouped_items = group_by(items, ['type', 'color'])
