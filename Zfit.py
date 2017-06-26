VERSIONS = "0.0.1 beta"
DATAFORMAT = {"tab":'\t',
              "space":' ',
              "comma":','
              }
SKIPROWS = 1
POTENTIAL = 0
IMPORT_TYPE = "Zreal_Zimag"


def do_fit(modelName, filename):
    import os
    import numpy as np
    from os import path
    from importlib import import_module, reload
    import Models.modelcore as mc

    filePath = path.split(filename)[0]
    if (os.path.isfile(filename)):
        # 获取到文件名和模块名
        model = import_module("Models." + modelName)
        model = reload(model)

        # 获取data
        #data = np.loadtxt(filename, skiprows=dataFormat['skiprows'], delimiter=dataFormat['delimiter']).T
        # 由于第一列是potential，数据不适用上面函数
 
        data = []
        potential = 0.0

        if POTENTIAL == 0:
            data = np.loadtxt(filename, skiprows=SKIPROWS, delimiter=DATAFORMAT[DELIMITER]).T
        elif POTENTIAL == 1:
            with open(filename) as _f:
                d = _f.read().splitlines()[SKIPROWS:]

            # 现在的数据是带有电位的data
            data = [_d.split(DATAFORMAT[DELIMITER]) for _d in d]
            potential = float(data[0][0])
            # 提取出电位，将剩下的转换为fre，zr，zi的数据格式
            data = np.array([_d[1:] for _d in data],dtype=np.float64).T
            # print(data[0])
        try:
            # potential,
            frequency, Zreal, Zimage = data[0:3]
            # phase = np.ones(len(data[0]))
        except:
            print("Data is not in right columns")
            return
        if IMPORT_TYPE == "Zreal_Zimag":
            # z target 输入的是Z’ 和Z“
            zTarg = np.array([_Zreal - _Zimage * 1j for _Zreal, _Zimage in zip(Zreal, Zimage)],dtype=np.complex128)
            # print(zTarg)
        elif IMPORT_TYPE == "Z_Phase":
            # 如果输入phase 和Z
            p = np.radians(Zimage)
            m = Zreal
            zTarg = m * np.exp(1j*p)


        freq = np.array(frequency,dtype=np.float64)

        # assign modelcore objects to this model
        mc.model = model.model
        mc.PINIT = model.PINIT
        mc.PBOUNDS = model.PBOUNDS
        mc.PARAMS = model.PARAMS
        mc.BOUNDWEIGHT = model.BOUNDWEIGHT

        keys, params = [], []

        fitresult = mc.fit_model(zTarg, np.ones(len(Zreal)).astype(np.float64), freq)
        # with open('d:/test2.txt',mode='w') as f:
        #     print(zTarg,file=f)
        params = fitresult[0]
        keys = model.PARAMS.keys()
        infodict = fitresult[2]
        mesg = fitresult[3]
        ier = fitresult[4]
        # print(params)
        # print(infodict['fjac'])

        storePath = path.join(filePath, "result")
        if not path.exists(storePath):
            os.mkdir(storePath)

        # 写入title，只写入一次，默认如果文件存在就不重复写入
        if not os.path.isfile(path.join(storePath, 'paras.txt')):
            with open(path.join(storePath, 'paras.txt'), mode='a', encoding='utf-8') as f:
                for key in keys:
                    print(str(key), file=f, end='\t')
                    # 在这里加上potential
                print("potential", file=f)
        # 写入parade的值
        with open(path.join(storePath, 'paras.txt'), mode='a', encoding='utf-8') as f:
            for para in params:
                print(str(para), file=f, end='\t')
            print("%.3f"%potential, file=f)

        # 输出模拟值
        zOmega = np.array([2.0 * np.pi * f for f in freq])
        zFited = model.model(zOmega, params)
        phase = np.array([np.rad2deg(np.arctan(z.imag / z.real)) for z in zFited])
        originFilename = path.split(filename)[1]
        fittedPath = path.join(storePath, "fitedData/")
        if not path.exists(fittedPath):
            os.mkdir(fittedPath)
        fittedFile = os.path.join(fittedPath,"fitted_%.2fV_"%potential + originFilename)

        with open(fittedFile, mode='w') as f:
            print('Frequency[Hz] \t Z\'[Omega]\t -Z\"[Omega]\t Z[Omega]\t -Phase[deg]', file=f)

            for _f, _zfitted, _p in zip(frequency, zFited, phase):
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(_f, np.real(_zfitted), -np.imag(_zfitted), np.abs(_zfitted), -_p), file=f)


        # print('\r' + originFilename+ '\t'+mesg + '\n ier=' + str(ier) + '\t fevl=' + str(infodict['nfev']),end='\r')
   
        return
#    elif path.isdir(filename):
#        for file in os.listdir(filename):
#            do_fit(modelName, os.path.join(filename,file))

#def statOnPotential(parafile,xCol,yCol):
#    import numpy as np
#    
#    stat = np.loadtxt(parafile,dtype=np.float,skiprows=SKIPROWS,delimiter=DATAFORMAT[DELIMITER])
#    x = 
#    statPotential = stat[-1]
#    




if __name__ == '__main__':

    import sys,os,getopt
    import configparser
    import pandas as pd
    def usage():
        print('''
        args:
        
        -f finelame
        -v version
        -m model
        
        
        ''')

    basePath = os.path.dirname(os.path.abspath(__file__))

    shortArgs = 'f:m:v'
    longArgs = ['file=', 'mode=', 'version']

    modelName = "ls(cpr)"
    filename = os.path.join(basePath,"Sample.csv")

    opts,args = getopt.getopt(sys.argv[1:],shortArgs,longArgs)


    # 读取配置文件
    confPath = os.path.join(basePath,'config.ini')
    if os.path.isfile(confPath):
        conf = configparser.ConfigParser()
        conf.read(confPath)
        filename = conf.get('Configs','File_Path')
        modelName= conf.get('Configs','Equiv_Circle_Model')
        SKIPROWS =conf.getint('DataFormat','SkipRows')
        POTENTIAL=conf.getint('DataFormat','Potential_Position')
        DELIMITER=str(conf.get('DataFormat','Delimiter')).lower()
        print('read config.ini success!')
        # print(DATAFORMAT[DELIMITER])



    if not len(opts) == 0:
        for opt, val in opts:
            if opt in ('-f', '--filename='):
                filename = val
            elif opt in ('-m', '--model='):
                modelName = val
                modelPath = os.path.join(basePath, 'Models/' + modelName + '.py')
                if not os.path.exists(modelPath):
                    print("model does not exit", file=sys.stdout)
                    sys.exit(2)
            elif opt in ('-v', '--version'):
                    print('VERSION %s'.format(VERSIONS))
                    usage()
                    sys.exit(2)


    if os.path.isfile(filename):
        print("data is file")
        do_fit(modelName, filename)

    elif os.path.isdir(filename):
        print("data is dir")
        sys.stdout.write("#"*int(81)+'|')
        j=0
        for file in os.listdir(filename):
            _filename = os.path.join(filename,file)
            if os.path.isfile(_filename):
                do_fit(modelName,_filename)
                j+=1
                sys.stdout.write('\r'+(j*80//len(os.listdir(filename)))*'-'+'->|'+"\b"*3)
                sys.stdout.flush()

        paraFile = os.path.join(filename,"result/paras.txt")
        stat = pd.read_csv(paraFile,sep='\t',index_col=-1)
        gp = stat.groupby('potential')
        gpStat = gp.describe()
        gpStat.to_csv(os.path.join(filename,"result/statstistic.txt"),sep='\t')
        
        sys.stdout.write("\nFINISHED! at %s\\result \n"%filename)
        
        

    else:
        print("Parameter of programme error")
        sys.exit(2)



