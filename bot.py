from gensim.models.word2vec import Word2Vec
import pickle

class Bot:
    def __init__(self):
        self.model=Word2Vec.load('suggest_1_2_3')
        with open('Product_dict.pkl', 'rb') as f:
            self.prod_dict = pickle.load(f)
        with open('reverse.pkl', 'rb') as f:
            self.reverse = pickle.load(f)
        with open('for3.pkl', 'rb') as f:
            self.for3 = pickle.load(f)

    def find_similar(self, ids, n):
        ids=str(ids)
        temp=self.model.most_similar(ids, topn=n)
        return [self.prod_dict[i[0]] for i in temp]
    
    def find_compl(self, ids, n):
        temp=self.model.predict_output_word(ids.split(), topn=n)
        return [self.prod_dict[i[0]] for i in temp]

    def find_str(self, strk, n=3):
        strk_spl = strk.split()
        final = list()
        for i in strk_spl:
            if i in self.for3:
                temp = self.for3[i][0:n]
                final += temp
        if len(final) == 0:
            return 'Not find'
        return [self.prod_dict[i] for i in final]

    def find_in_subcategpry(self, ids):
        with open('last_dict.pkl', 'rb') as f:
            last_dict = pickle.load(f)
        final = list()
        ids = str(ids)
        temp = self.model.most_similar(ids, topn=100)
        id_sim = temp[::][0]
        for i in range(len(temp)):
            if (temp[i][1] > 0.5):
                final.append(temp[i])
        sub = last_dict[ids]
        answer = list()
        for i in final:
            if last_dict[i[1]] == sub:
                answer.append(self.prod_dict[i[0]])
        if len(answer) == 0:
            return 'No'
        return answer


