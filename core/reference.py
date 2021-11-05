from pandas import DataFrame


class Reference:

    def __init__(self):
        pass

    def _calculate_tpo_count(self, tpo: DataFrame) -> DataFrame:
        '''
        Per ogni prezzo in Tpo conta la frequenza con la quale il prezzo è stato scambiato
        '''
        # tpo.to_csv("./data/csv/tpo.csv")
        price_count_list = []
        for col, _ in tpo.iteritems():
            price_count_list.append((col, tpo[col].count()))
        tpo_count = DataFrame(price_count_list, columns=['price', 'count'])
        tpo_count.index.name = 'index'
        return tpo_count
