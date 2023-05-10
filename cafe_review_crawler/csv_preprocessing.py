import argparse
import ast
import pandas as pd
import glob
import datetime
import re
import numpy as np
from emoji import core

#from hanspell import spell_checker

class review__preprocessing():
    def __init__(self):
        parser = argparse.ArgumentParser('review_data preprocessing', add_help=False)
        parser.add_argument('--review-size', default=100, type=int)
        parser.add_argument('--review-length', default=700, type=int)
        parser.add_argument('--data-path', default='./data')
        parser.add_argument('--result-path', default='concat_data.csv')
        parser.add_argument('--sentence_size', default=8, type=int)
        
        self.args = parser.parse_args()


    def set_list_size(self, x, size):
        if len(x) > size:
            return x[:size]
        else:
            return x

    def review_preprocessing(self, x, sentence_size, review_length):
        new_reviews = []

        for sentence in x:
            
            # 전처리
            sentence = re.sub('\n',' ',sentence)
            sentence = re.sub('\u200b','',sentence)
            sentence = re.sub('\xa0','',sentence)
            sentence = re.sub('([a-zA-Z])','',sentence)
            sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)
            sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',sentence)
            sentence = core.replace_emoji(sentence, replace="")
            
            # 맞춤법
            # try:
            #     sentence = spell_checker.check(sentence).as_dict()['checked']
            # except Exception as e:
            #     pass

            if len(sentence) >= sentence_size:
                new_reviews.append(sentence)
    
        new_reviews = ' '.join(new_reviews)
        if len(new_reviews) > review_length:
            new_reviews = new_reviews[:review_length]
        return new_reviews


    def set_review_size(self, df, args):
        df['review'] = df['review'].apply(ast.literal_eval)
        df['review'] = df['review'].apply(self.set_list_size, args=(args.review_size,))
        df['review'] = df['review'].apply(self.review_preprocessing, args=(args.sentence_size, args.review_length, ))
        return df
        
    def concat_csv(self, csv_files, args):
        # 전체 df
        df = pd.DataFrame()
        for csv_file in csv_files:
            print(csv_file)
            df = pd.concat([df, self.set_review_size(pd.read_csv(csv_file, index_col=0), args)], ignore_index=True)
        df.to_csv(f'{args.result_path}')
        
    def read_all_csv(self, path):
        return glob.glob(f'{path}/*.csv')
        
    def review_data_main(self):
        self.concat_csv(self.read_all_csv(self.args.data_path), self.args)




# --------------------------------------------------
class label__preprocessing:
    def __init__(self):
        parser = argparse.ArgumentParser('label_data preprocessing', add_help=False)
        
        parser.add_argument('--data-path', default='./label_data')
        parser.add_argument('--result-path', default='.')
        parser.add_argument('--threshold', nargs=2, default=[0.3 , 0.08], type=float)

        self.args = parser.parse_args()

        self.summary_dict = {'"커피가 맛있어요"': [0],
                    '"뷰가 좋아요"': [3],
                    '"친절해요"': [2],
                    '"대화하기 좋아요"': [4],
                    '"음료가 맛있어요"': [0],
                    '"매장이 청결해요"': [2],
                    '"좌석이 편해요"': [4, 5],
                    '"빵이 맛있어요"': [1],
                    '"인테리어가 멋져요"': [3],
                    '"주차하기 편해요"': [2],
                    '"디저트가 맛있어요"': [1],
                    '"특별한 메뉴가 있어요"': [0, 1],
                    '"화장실이 깨끗해요"': [2],
                    '"집중하기 좋아요"': [5],
                    '"사진이 잘 나와요"': [3],
                    '"가성비가 좋아요"': [6],
                    '"매장이 넓어요"': [3],
                    '"음악이 좋아요"': [3],
                    '"야외 공간이 멋져요"': [3],
                    '"오래 머무르기 좋아요"': [4],
                    '"차분한 분위기에요"': [3],
                    '"종류가 다양해요"': [0],
                    '"메뉴 구성이 알차요"': [1],
                    '"포장이 깔끔해요"': [1],
                    '"차가 맛있어요"': [0],
                    '"비싼 만큼 가치있어요"': [0, 1],
                    '"반려동물과 가기 좋아요"': [7],
                    '"컨셉이 독특해요"': [3],
                    '"아늑해요"': [3],
                    '"룸이 잘 되어있어요"': [4]
                    }
        
        

    def read_all_csv(self, path):
        return glob.glob(f'{path}/*.csv')
    
    def get_key(self, key):
        # TODO: 알고리즘에 따라 분류하기.
        return key

    def transform_summary(self, x):
        summarys = x['summary']
        summary_sum = np.zeros(8)
        for key, value in summarys.items() :
            if len(value) < 10: continue
            # value를 전처리해서, 
            value = int(value.split('\n')[1])
            #value = int(float(re.sub(r'[^0-9]', '', value)))
            # 존재하는 key의 값에 더하기
            try:
                for sum_key in self.summary_dict[key]:
                    summary_sum[sum_key] += value
            except KeyError:
                continue
        return summary_sum

    def calc_summary(self, x, threshold):
        total = x.sum()
        for idx, n in enumerate(x):
            
            if idx <= 1:
                threshold_v = threshold[0]
            else:
                threshold_v = threshold[1]
            x[idx] = int((n / total) >= threshold_v)
        #x = np.where((x / total) >= threshold , 1, 0)
        return x.astype(np.int64).tolist()

    def set_summary_form(self, df, args):
        df['summary'] = df['summary'].apply(ast.literal_eval)
        df['summary'] = df.apply(self.transform_summary, axis=1)
        df['summary'] = df['summary'].apply(self.calc_summary, args=(args.threshold,))
        return df

    def concat_csv_label(self, csv_files, args):
        # 전체 df
        df = pd.DataFrame()
        for csv_file in csv_files:
            df = pd.concat([df, self.set_summary_form(pd.read_csv(csv_file, index_col=0), args)], ignore_index=True)
            #df = pd.concat([df, pd.read_csv(csv_file, index_col=0)], ignore_index=True)
        df.to_csv(f'{args.result_path}/label_{datetime.datetime.now().strftime("%d%H%M")}.csv')
        


    def label_data_main(self):
        res = self.concat_csv_label(self.read_all_csv(self.args.data_path) , self.args)






# --------------------------------------------------
class duplicate_cafe():
    def __init__(self):
        parser = argparse.ArgumentParser('remove duplicated cafe', add_help=False)
        
        parser.add_argument('--cafedata-path', default='cafe_data_undup.csv')
        parser.add_argument('--cafedata-undup-path', default='cafe_data_undup.csv')
        parser.add_argument('--data-path', default='concat_data.csv')
        parser.add_argument('--data-undup-path', default='concat_data_undup.csv')
        parser.add_argument('--labeldata-path', default='label_data.csv')
        parser.add_argument('--dataset-path', default='dataset.csv')
        parser.add_argument('--train-dataset-path', default='train.csv')
        parser.add_argument('--test-dataset-path', default='test.csv')

        self.args = parser.parse_args()

    def undup_cafedata(self):
        df = pd.read_csv(self.args.cafedata_path)
        df = df.drop_duplicates(subset=['name', 'address'])
        df.to_csv(self.args.cafedata_undup_path)

    def undup_data_cafedata(self):
        df_cafe = pd.read_csv(self.args.cafedata_path)
        df_data = pd.read_csv(self.args.data_path)
        pd.merge(df_cafe, df_data, on = ['dong', 'name'], how = 'left').drop(labels=['Unnamed: 0_x', 'Unnamed: 0_y', 'si_y', 'gu_y'], axis=1).rename(columns={'si_x':'si', 'gu_x':'gu'}).to_csv(self.args.data_undup_path)
        # drop : Unnamed: 0_x, Unnamed: 0_y, si_y, gu_y
        # rename : si_x, gu_x

    def concat_data_label(self):
        df_label = pd.read_csv(self.args.labeldata_path)
        df_data = pd.read_csv(self.args.data_undup_path)
        pd.merge(df_data, df_label, on = ['dong', 'name'], how = 'left').drop(labels=['Unnamed: 0_x', 'Unnamed: 0_y', 'si_y', 'gu_y'], axis=1).rename(columns={'si_x':'si', 'gu_x':'gu', 'summary':'label'}).to_csv(self.args.dataset_path)
        # drop : Unnamed: 0_x, Unnamed: 0_y, si_y, gu_y
        # rename : si_x, gu_x, summary
        
    def split_dataset(self):
        df = pd.read_csv(self.args.dataset_path)
        
        part_90 = df.sample(frac= 0.9)
        rest_part_10 = df.drop(part_90.index)

        part_90.to_csv(self.args.train_dataset_path, index=False)
        rest_part_10.to_csv(self.args.test_dataset_path, index=False)
    






if __name__ == '__main__':
    #review__preprocessing().review_data_main()
    #label__preprocessing().label_data_main()
    duplicate_cafe().split_dataset()

    # review__preprocessing().review_data_main()
    # duplicate_cafe().undup_data_cafedata()
