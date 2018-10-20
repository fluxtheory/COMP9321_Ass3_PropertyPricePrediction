#-*-coding:utf8-*-
__author__ = 'Pengcheng Xie & Hanming Yin'

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# % matplotlib inline
import seaborn as sb
import math
import re
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import os


class PropertyPricePrediction():
    # input property environment
    # env = list([Rooms,Type,Method,SellerG,Sold_Year,Distance,Bathroom,Car,LandSize,CouncilArea])
    # Rooms            int64
    # Type             string
    # Price            float64
    # Method           string
    # SellerG          string
    # Sold_Year        string , e.g. 1984
    # Distance         float64
    # Bathroom         float64
    # Car              float64
    # LandSize         float64
    # CouncilArea      string
    # Regionname       string
    # Propertycount    float64
    def __init__(self):
        self.ds = pd.read_csv('Full.csv')
        if os.path.exists('train.csv'):
            print('Clean data has been found, loading ...')
            self.train = pd.read_csv('train.csv')
        else:
            print('Only find raw data, we are going to processing it.')
            # cleaning data first then return clean data
            self.processing()
            self.train = pd.read_csv('train.csv')

    def setArgs(self, env):
        self.env = env
        if len(env) != 10:
            print('The input information is not accuracy.')
        self.room = env[0]
        self.type = env[1][0].lower()
        self.method = env[2].upper()
        self.sellerG = env[3].title()
        self.soldYear = env[4]
        self.distance = env[5]
        self.bathroom = env[6]
        self.car = env[7]
        self.landSize = env[8]
        self.councilArea = env[9].title()

    def predict(self):
        train = self.train
        # get input data
        # print('self.councilArea',self.councilArea)
        R_n = train.Regionname[train.CouncilArea == self.councilArea]
        # print(R_n.iat[0])
        # print(type(train.Regionname[train.CouncilArea == self.councilArea]))
        self.regionName = R_n.iat[0]
        cnt = train.Propertycount[train.CouncilArea == self.councilArea]
        self.propertyCount = cnt.iat[0]
        self.column = ['Rooms','Type','Method','SellerG','Sold_Year','Distance','Bathroom','Car','Landsize','CouncilArea','Regionname','Propertycount']
        self.inputData = [self.room,self.type,self.method,self.sellerG,self.soldYear,self.distance,self.bathroom,self.car,self.landSize,self.councilArea,self.regionName,self.propertyCount]
        # print('Input data ', self.inputData)
        self.input = pd.DataFrame(data=[self.inputData],columns=self.column)
        # print('Property information:')
        # print(self.input)
        self.dummy_test = self.dummy_data(self.input,train)

        self.dummy_test = self.dummy_test.drop(['Unnamed: 0'], axis=1)

        # print('-----------')
        # print(self.dummy_test)
        # print('-----------')
        # transfer the input to xgb data structure
        dtest = xgb.DMatrix(data=self.dummy_test)

        # save some regarding charts
        if os.path.exists('images'):
            os.chdir('./images')
        else:
            os.mkdir('images')
            os.chdir('./images')

        dictionary = {'h':'House','u':'Unit','t':'Townhouse','dev site':'Development Site','o res':'Other Residential'}
        # chart 1:
        name = f'Average Price Of {dictionary[self.env[1]]} In Different Regions'
        if not os.path.exists(name + '.png'):
            CSV1 = train[['Regionname', 'Landsize', 'Price', 'Type']]
            CSV1 = CSV1[CSV1['Type'] == self.type]
            CSV1 = CSV1.groupby('Regionname').sum()
            CSV1['Avg'] = CSV1.apply(lambda x: x.Price / x.Landsize, axis = 1)
            CSV1 = CSV1['Avg']
            try:
                CSV1.plot.bar()
                plt.tight_layout()
                plt.ylabel('Unit: $/m²')
                plt.title(name)
                plt.savefig(name + '.png')
            except:
                pass

        # chart 2: the average pricein different council area
        name = f'Average Price Of {dictionary[self.type]} In Different Council Area'
        if not os.path.exists(name + '.png'):
            plt.rcdefaults()
            CSV3 = train[['CouncilArea', 'Landsize', 'Price', 'Type']]
            CSV3 = CSV3[CSV3['Type'] == self.type]
            CSV3 = CSV3.groupby('CouncilArea').sum()
            CSV3['Avg'] = CSV3.apply(lambda x: x.Price / x.Landsize, axis = 1)
            CSV3 = CSV3['Avg']
            try:
                CSV3.plot.bar()
                plt.tight_layout()
                plt.ylabel('Unit: $/m²')
                plt.title(name)
                plt.savefig(name + '.png')
            except:
                pass

        # chart 3: the average price of council area in different year
        name = f'Average Price Of {dictionary[self.type]} Over Years'
        if not os.path.exists(name + '.png'):
            plt.rcdefaults()
            CSV3 = train[['Sold_Year', 'Landsize', 'Price', 'Type']]
            CSV3 = CSV3[CSV3['Type'] == self.type]
            CSV3 = CSV3.groupby('Sold_Year').sum()
            CSV3['Avg'] = CSV3.apply(lambda x: x.Price / x.Landsize, axis = 1)
            CSV3 = CSV3['Avg']
            try:
                CSV3.plot.bar()
                plt.tight_layout()
                plt.ylabel('Unit: $/m²')
                plt.title(name)
                plt.savefig(name + '.png')
            except:
                pass

        os.chdir('..')

        # Prediction
        if os.path.exists('ppp.model'):
            print('Pre-trained model found, begin to predict price ...')
            bst2 = xgb.Booster(model_file='ppp.model')
            preds = bst2.predict(dtest)[0]
            print('Property information:')
            print(self.input)
        else:
            print('Not found pre-trained model, we are training model now ...')
            # train first then predict.
            self.training(train=train)
            bst2 = xgb.Booster(model_file='ppp.model')
            preds = bst2.predict(dtest)[0]
            print('Property information:')
            print(self.input)

        new = self.ds[['Address', 'Rooms', 'Landsize', 'Type', 'Price']]
        new1 = new[new['Price'] > (preds - 10000)]
        new2 = new1[new1['Price'] < (preds + 10000)]
        newcsv = new2.reset_index(drop = True)

        info = list()
        length = newcsv.shape[0]
        if length >= 5:
            for i in range(5):
                idx = random.randint(0, length - 1)
                info.append(list(newcsv.loc[idx]))
        elif length > 0:
            for i in range(length):
                idx = random.randint(0, length - 1)
                info.append(list(newcsv.loc[idx]))

        for row in info:
            if row[3] == 'h' or row[3] == 'H':
                row[3] = 'House'
            elif row[3] == 'u' or row[3] == 'U':
                row[3] = 'Unit'
            elif row[3] == 't' or row[3] == 'T':
                row[3] = 'TownHouse'
            else:
                row[3] = 'Other'

        return preds, info

    def processing(self):
        trainf = pd.read_csv('FULL.csv')
        train = trainf
        train = train.drop(['Lattitude', 'Longtitude'], axis=1)
        # drop the samples where Price is NULL
        train1 = train[train.Price > 0]
        # drop the samples in which Regionname is null
        train1['Regionname'] = train1['Regionname'].fillna("None")
        train1 = train1[train1.Regionname != "None"]

        train1 = train1.drop(['Bedroom2'], axis=1)
        # Fill the null Bathroom values with v=round(#Rooms/2)
        train1['Bathroom'] = train1['Bathroom'].fillna(round(train1['Rooms'] / 2))
        train1.loc[train1.Bathroom == 0, 'Bathroom'] = 1

        # Fill the null values with v=round(#Rooms/2)
        train1['Car'] = train1['Car'].fillna(round(train1['Rooms'] / 2))

        # Fill null values with mean values
        train1['Landsize'] = train1['Landsize'].fillna(train1.mean()['Landsize'])

        # Too many null cells, drop this feature at this moment.
        train1 = train1.drop(['YearBuilt'], axis=1)

        # Too many null cells, drop this feature at this moment.
        train1 = train1.drop(['BuildingArea'], axis=1)

        # print(train1)
        # Building model in this step
        train2 = train1.drop(['Postcode', 'Address', 'Suburb'], axis=1)
        # Rewrite sold Date to only remain Year info as Sold_Year

        train2['Date'] = train2['Date'].apply(lambda x: re.search(r'(\d{4})', str(x)).group())
        train2.rename(columns={'Date': 'Sold_Year'}, inplace=True)
        train2['SellerG'] = train2['SellerG'].apply(lambda x: str(x).title())
        train2.to_csv('train.csv')
        # return train2

    def training(self,train):
        # label
        y = train['Price']
        # one-hot coding
        train1 = train.drop(['Price'], axis=1)
        X = pd.get_dummies(train1).reset_index(drop=True)
        # 80% for training and 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        dtrain = xgb.DMatrix(data=X_train, label=y_train)
        dtest = xgb.DMatrix(data=X_test, label=y_test)
        param = {'max_depth': 8,
                 'colsample_bytree': 0.4,
                 'learning_rate': 0.01,
                 'objective': 'reg:linear',
                 'alpha': 10,
                 'n_estimators': 600,
                 'subsample': 0.7,
                 'eval_metric': 'rmse'}
        evallist = [(dtest, 'eval'), (dtrain, 'train')]
        # number of boosting iterations
        num_round = 801
        # print every 100 iterations
        model = xgb.train(param, dtrain, num_round, evallist,verbose_eval=100)
        model.save_model('ppp.model')

    def dummy_data(self,df,train):
        train1 = train.drop(['Price'], axis=1)
        X = pd.get_dummies(train1).reset_index(drop=True)
        column_name = X.columns.values.tolist()
        value = [[0] * len(column_name)]
        newDF = pd.DataFrame(data=value, columns=column_name)
        # get column_name list of input dataFrame
        # print('__________________newDF -_____________')
        # print(newDF)
        # print('__________________newDF -_____________')
        clist = df.columns.values.tolist()
        for i in range(len(clist)):
            if type(df[clist[i]][0]) != str:
                # print(clist[i])
                newDF[clist[i]][0] = float(df[clist[i]][0])
            else:
                column = clist[i] + '_' + df[clist[i]][0]
                # print('c:', column)
                if column in column_name:
                    newDF[column] = 1
        # print('__________________newDF -_____________')
        # print(newDF)
        # print('__________________newDF -_____________')
        return newDF

if __name__ == '__main__':
    # env = list([Rooms,Type,Method,SellerG,Sold_Year,Distance,Bathroom,Car,LandSize,CouncilArea])
    # Rooms            int64
    # Type             string
    # Price            float64
    # Method           string
    # SellerG          string
    # Sold_Year        string , e.g. 1984
    # Distance         float64
    # Bathroom         float64
    # Car              float64
    # LandSize         float64
    # CouncilArea      string

    ppp = PropertyPricePrediction()
    env = [3,'h','None','None','2018',2.5,2.0,0.0,134.0,'Yarra City Council']
    ppp.setArgs(env)
    print("Start to predict")
    price, similar_property = ppp.predict()
    print('The price of this property is: AUD$',round(price))
    print('The property have similar price', similar_property)
    # Yarra City Council ,  Port Phillip City Council
