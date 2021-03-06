
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd


#Define função para calcular o MAPE
def mape(y_pred,y_true):

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


#Carrega os dados

data = pd.read_csv('prime.csv',header=0,index_col=0).sort()

x_data = []
y_data = []

# Formata de maneira que cada linha da matriz X seja composta pelos 6 meses anteriores.
for d in xrange(6,data.shape[0]):
    
    x = data.iloc[d-6:d].values.ravel()
    y = data.iloc[d].values[0]

    x_data.append(x)
    y_data.append(y)


x_data = np.array(x_data)
y_data = np.array(y_data)




#Listas para armazenar as previsões de cada modelo
y_pred = []
y_pred_last = []
y_pred_ma = []
y_true = []



#Itera pela série temporal treinando um novo modelo a cada mês
end = y_data.shape[0]
for i in range(30,end):

    x_train = x_data[:i,:]
    y_train = y_data[:i]
    
    x_test = x_data[i,:]
    y_test = y_data[i]


    model = LinearRegression(normalize=True)
    model.fit(x_train,y_train)

    y_pred.append(model.predict(x_test))
    y_pred_last.append(x_test[-1])
    y_pred_ma.append(x_test.mean())
    y_true.append(y_test)


#Transforma as listas em arrays numpy para facilitar os cálculos
y_pred = np.array(y_pred)
y_pred_last = np.array(y_pred_last)
y_pred_ma = np.array(y_pred_ma)
y_true = np.array(y_true)


#Imprime os erros na tela
print '\nMean Absolute Percentage Error'
print 'MAPE Regressão Linear', mape(y_pred,y_true)
print 'MAPE Último Valor', mape(y_pred_last,y_true)
print 'MAPE Média Móvel', mape(y_pred_ma,y_true)


print '\nMean Absolute Error'
print 'MAE Regressão Linear', mean_absolute_error(y_pred,y_true)
print 'MAE Último Valor', mean_absolute_error(y_pred_last,y_true)
print 'MAE Média Móvel', mean_absolute_error(y_pred_ma,y_true)



# OPCIONAL - REQUER SCIPY
#from scipy.stats import wilcoxon
#error_linreg = abs(y_true - y_pred)
#error_last = abs(y_true - y_pred_last)
#print '\nWilcoxon P-value', wilcoxon(error_linreg,error_last)[1]/2.



# OPCIONAL - REQUER MATPLOTLIB
#from matplotlib import pyplot as plt
#plt.title('Prime Rate Brasil - Mensal - 2005 a 2014')
#plt.ylabel('Prime Rate')
#plt.xlabel(u'Períodos (Meses)')
#reg_val, = plt.plot(y_pred,color='b',label=u'Regressão Linear')
#true_val, = plt.plot(y_true,color='g', label='Valores Reais')
#plt.xlim([0,85])
#plt.legend(handles=[true_val,reg_val])
#plt.show()



