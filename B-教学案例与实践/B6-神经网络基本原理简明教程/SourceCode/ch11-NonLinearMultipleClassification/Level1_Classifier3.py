# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math

from LossFunction import * 
from Activators import *
from Level0_TwoLayerClassificationNet import *
from DataReader import * 
from WeightsBias import *

x_data_name = "X11.dat"
y_data_name = "Y11.dat"

def ShowAreaResult(net, wb1, wb2, title):
    count = 50
    x1 = np.linspace(0,1,count)
    x2 = np.linspace(0,1,count)
    for i in range(count):
        for j in range(count):
            x = np.array([x1[i],x2[j]]).reshape(2,1)
            dict_cache = net.forward(x, wb1, wb2)
            output = dict_cache["Output"]
            r = np.argmax(output, axis=0)
            if r == 0:
                plt.plot(x[0,0], x[1,0], 's', c='m')
            elif r == 1:
                plt.plot(x[0,0], x[1,0], 's', c='y')
            # end if
        # end for
    # end for
    plt.title(title)
#end def

def ShowData(X, Y):
    for i in range(X.shape[1]):
        if Y[0,i] == 1:
            plt.plot(X[0,i], X[1,i], '^', c='g')
        elif Y[1,i] == 1:
            plt.plot(X[0,i], X[1,i], 'x', c='r')
        elif Y[2,i] == 1:
            plt.plot(X[0,i], X[1,i], '.', c='b')
        # end if
    # end for
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.show()


if __name__ == '__main__':

    dataReader = DataReader(x_data_name, y_data_name)
    dataReader.ReadData()
    X = dataReader.NormalizeX()
    Y = dataReader.ToOneHot()
    
    n_input, n_output = dataReader.num_feature, dataReader.num_category
    n_hidden = 8
    eta, batch_size, max_epoch = 0.1, 10, 1000
    eps = 0.06

    params = CParameters(n_input, n_hidden, n_output, eta, max_epoch, batch_size, eps, LossFunctionName.CrossEntropy3)

    loss_history = CLossHistory()
    net = TwoLayerClassificationNet()

    ShowData(X, Y)

    net.train(dataReader, params, loss_history)

    trace = loss_history.GetMinimalLossData()
    print(trace.toString())
    title = loss_history.ShowLossHistory(params)

    print("wait for 10 seconds...")

    ShowAreaResult(net, trace.wb1, trace.wb2, title)
    ShowData(dataReader.X, dataReader.Y)
    