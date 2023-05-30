#! /usr/bin/python3 python3
import time
import subprocess
import os
import sys

str_ID='securibench'       #'securibench'   #'Example' #'TwoObjHeap'  #'securibench4'
str='out/{mstr_ID}/database'.format(mstr_ID=str_ID)
strB='mainAnalysis.configuration.mFlow.B.csv'
strC='mainAnalysis.configuration.mFlow.C.csv'
strSB='mainAnalysis.configuration.mFlow.SB.csv'
strSC='mainAnalysis.configuration.mFlow.SC.csv'
def cmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",universal_newlines=True)
#    subp.wait(3600)   如果调用了该句,就不会实时打印出调试信息
    while True:
        nextline = subp.stdout.readline()
        if nextline == '' and subp.poll() is not None:  #subp.poll()为None时,表示进程正在运行
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()
    if subp.poll() == 0:
        sizeC = os.path.getsize('{mstr}/{mstrC}'.format(mstr=str,mstrC=strC))
        sizeB = os.path.getsize('{mstr}/{mstrB}'.format(mstr=str,mstrB=strB))
        sizeSC = os.path.getsize('{mstr}/{mstrSC}'.format(mstr=str,mstrSC=strSC))
        sizeSB = os.path.getsize('{mstr}/{mstrSB}'.format(mstr=str,mstrSB=strSB))
        if sizeC == 0:
            print('\n\n\n\n')
            print('--------')
            print('C Fail')
            print('\n\n\n\n')
       
        else:
            strC1='sed \'s/^.*nil, \[\[/"Ctx: /g\' {mstr}/{mstrC}|sed \'s/]], \[\[/" -> "Ctx: /g\'|sed \'s/], </\\nVar: </g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/C.dot'.format(mstr=str,mstrC=strC)
            #strC1='sed \'s/^.*nil, \[\[/"Ctx :/g\' {mstr}/{mstrC}|sed \'s/], </\nVar: </g\'|sed \'s/]], \[\[/" -> "/g\'|sed \'s/]]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/C.dot'.format(mstr=str,mstrC=strC)
            #strC1= 'sed \'s/^.*nil,//g\' {mstr}/{mstrC}|sed \'s/]],/" ->/g\'|sed \'s/\[\[/"[/g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/C.dot'.format(mstr=str,mstrC=strC)
            #strC1='sed \'s/\]//g\' {mstr}/{mstrC}|sed \'s/\[//g\'|sed \'s/nil,//g\'|sed \'s/, </ -> </g\'|sed \'s/^/"/g\'|sed \'s/$/";/g\' |sed \'1i\strict digraph{{ \'|sed \'s/ -> /" -> "/g\' > {mstr}/C.dot'.format(mstr=str,mstrC=strC)
            #strC2='echo \'}}\' >> {mstr}/C.dot'.format(mstr=str)
            strC3='dot -Tsvg {mstr}/C.dot -o {mstr}/C.svg'.format(mstr=str)
            strC4='xdg-open {mstr}/C.svg'.format(mstr=str)

     
            
            os.system(strC1)
            #os.system(strC2)
            os.system(strC3)
            os.system(strC4) 

            print('\n\n\n\n')
            print('--------')
            print('C Success')
            print('\n\n\n\n')

        if sizeB == 0:
            print('\n\n\n\n')
            print('--------')
            print('B Fail')
            print('\n\n\n\n')
        else:
            strB1='sed \'s/^.*nil, \[\[/"Ctx: /g\' {mstr}/{mstrB}|sed \'s/]], \[\[/" -> "Ctx: /g\'|sed \'s/], </\\nVar: </g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/B.dot'.format(mstr=str,mstrB=strB)
            #strB1='sed \'s/^.*nil, \[\[/"Ctx :/g\' {mstr}/{mstrB}|sed \'s/], </\nVar: </g\'|sed \'s/]], \[\[/" -> "/g\'|sed \'s/]]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/B.dot'.format(mstr=str,mstrB=strB)
            #strSB1= 'sed \'s/^.*nil,//g\' {mstr}/{mstrB}|sed \'s/]],/" ->/g\'|sed \'s/\[\[/"[/g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/B.dot'.format(mstr=str,mstrB=strB)
            #strB1='sed \'s/\]//g\' {mstr}/mainAnalysis.configuration.mFlow.B.csv |sed \'s/\[//g\'|sed \'s/nil,//g\'|sed \'s/, </ -> </g\'|sed \'s/^/"/g\'|sed \'s/$/";/g\' |sed \'1i\strict digraph{{ \'|sed \'s/ -> /" -> "/g\' > {mstr}/B.dot'.format(mstr=str)
            #strB2='echo \'}}\' >> {mstr}/B.dot'.format(mstr=str)
            strB3='dot -Tsvg {mstr}/B.dot -o {mstr}/B.svg'.format(mstr=str)
            strB4='xdg-open {mstr}/B.svg'.format(mstr=str)

            os.system(strB1)
            #os.system(strB2)
            os.system(strB3)
            os.system(strB4) 

            print('\n\n\n\n')
            print('--------')
            print('B Success')
            print('\n\n\n\n')
        if sizeSC == 0:
            print('\n\n\n\n')
            print('--------')
            print('SC Fail')
            print('\n\n\n\n')
       
        else:
            strSC1= 'sed \'s/^.*nil, /"/g\' {mstr}/{mstrSC} |sed \'s/], </" -> "</g\'|sed \'s/]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SC.dot'.format(mstr=str,mstrSC=strSC)
            #strSC1=sed 's/^.*nil, </"</g'|sed 's/], </" -> "</g'|sed 's/]$/";/g'|sed '1i strict digraph{'|sed '$a }' >sc.dot
            #strSC1='sed \'s/^.*nil, \[\[/"Ctx: /g\' {mstr}/{mstrSC}|sed \'s/]], \[\[/" -> "Ctx: /g\'|sed \'s/], </\\nVar: </g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SC.dot'.format(mstr=str,mstrSC=strSC)
            #strSC1='sed \'s/^.*nil, \[\[/"Ctx :/g\' {mstr}/{mstrSC}|sed \'s/], </\nVar: </g\'|sed \'s/]], \[\[/" -> "/g\'|sed \'s/]]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SC.dot'.format(mstr=str,mstrSC=strSC)
            #strSC1= 'sed \'s/^.*nil, /"/g\' {mstr}/{mstrSC} |sed \'s/], </" -> "</g\'|sed \'s/]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SC.dot'.format(mstr=str,mstrSC=strSC)
            #strSC1= 'sed \'s/^.*nil,//g\' {mstr}/{mstrSC}|sed \'s/]],/" ->/g\'|sed \'s/\[\[/"[/g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SC.dot'.format(mstr=str,mstrSC=strSC)
            #strC1='sed \'s/\]//g\' {mstr}/{mstrC}|sed \'s/\[//g\'|sed \'s/nil,//g\'|sed \'s/, </ -> </g\'|sed \'s/^/"/g\'|sed \'s/$/";/g\' |sed \'1i\strict digraph{{ \'|sed \'s/ -> /" -> "/g\' > {mstr}/C.dot'.format(mstr=str,mstrC=strC)
            #strC2='echo \'}}\' >> {mstr}/C.dot'.format(mstr=str)
            strSC3='dot -Tsvg {mstr}/SC.dot -o {mstr}/SC.svg'.format(mstr=str)
            strSC4='xdg-open {mstr}/SC.svg'.format(mstr=str)

     
            
            os.system(strSC1)
            #os.system(strC2)
            os.system(strSC3)
            os.system(strSC4) 

            print('\n\n\n\n')
            print('--------')
            print('SC Success')
            print('\n\n\n\n')

        if sizeSB == 0:
            print('\n\n\n\n')
            print('--------')
            print('SB Fail')
            print('\n\n\n\n')
        else:
            strSB1= 'sed \'s/^.*nil, /"/g\' {mstr}/{mstrSB} |sed \'s/], </" -> "</g\'|sed \'s/]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SB.dot'.format(mstr=str,mstrSB=strSB)
            #strSB1='sed \'s/^.*nil, \[\[/"Ctx: /g\' {mstr}/{mstrSB}|sed \'s/]], \[\[/" -> "Ctx: /g\'|sed \'s/], </\\nVar: </g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SB.dot'.format(mstr=str,mstrSB=strSB)
            #strSB1='sed \'s/^.*nil, \[\[/"Ctx :/g\' {mstr}/{mstrSB}|sed \'s/], </\nVar: </g\'|sed \'s/]], \[\[/" -> "/g\'|sed \'s/]]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SB.dot'.format(mstr=str,mstrSB=strSB)
            #strSB1= 'sed \'s/^.*nil, /"/g\' {mstr}/{mstrSB} |sed \'s/], </" -> "</g\'|sed \'s/]$/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/SB.dot'.format(mstr=str,mstrSB=strSB)
            #strSB1= 'sed \'s/^.*nil,//g\' {mstr}/{mstrSB}|sed \'s/]],/" ->/g\'|sed \'s/\[\[/"[/g\'|sed \'s/]]/";/g\'|sed \'1i strict digraph{{\'|sed \'$a }}\' >{mstr}/B.dot'.format(mstr=str,mstrSB=strSB)
            #strB1='sed \'s/\]//g\' {mstr}/mainAnalysis.configuration.mFlow.B.csv |sed \'s/\[//g\'|sed \'s/nil,//g\'|sed \'s/, </ -> </g\'|sed \'s/^/"/g\'|sed \'s/$/";/g\' |sed \'1i\strict digraph{{ \'|sed \'s/ -> /" -> "/g\' > {mstr}/B.dot'.format(mstr=str)
            #strB2='echo \'}}\' >> {mstr}/B.dot'.format(mstr=str)
            strSB3='dot -Tsvg {mstr}/SB.dot -o {mstr}/SB.svg'.format(mstr=str)
            strSB4='xdg-open {mstr}/SB.svg'.format(mstr=str)

            os.system(strSB1)
            #os.system(strB2)
            os.system(strSB3)
            os.system(strSB4) 

            print('\n\n\n\n')
            print('--------')
            print('SB Success')
            print('\n\n\n\n')
    else:
            print('\n\n\n\n')
            print('--------')
            print('All Failed')
            print('\n\n\n\n')

   #过滤生成结果,将所有生成以mainAnalysis.(.*).csv的文件过滤成只有str_ID的行
    #os.system('bash Fliter')
   

str_input='{mstr_ID}.jar'.format(mstr_ID=str_ID)
str_analysis='tfa'  #tfa micro
str_cmd='./doop  -a {mstr_analysis}  --input-file {mstr_input} --platform java_11  --id {mstr_ID} --information-flow webapps --information-flow-high-soundness --generate-jimple'.format(mstr_input=str_input,mstr_ID=str_ID,mstr_analysis=str_analysis)

cmd(str_cmd)
