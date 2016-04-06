#!/usr/bin/python
import os
import sys
import glob
import math
import operator
from random import randint
from collections import Counter

def generateStopWords(tf, df, threshold):
    if threshold < 1: dc = len(tf)
    else: dc = 1
    return set([k for (k,v) in df.items() if float(v)/dc >= threshold])

def getTermFrequencies(fin):
    tf = Counter()
    for line in fin: tf.update(line.split())
    return tf

def getDocumentFrequencies(tf):
    df = Counter()
    for d in tf: df.update(d.keys())
    return df

def getTFIDF(tf, df, dc):
    return tf * math.log(float(dc) / df)

def getTFIDFs(tf, df, sw):
    dc = len(tf)
    tfidf = []

    for d1 in tf:
        d2 = {k:getTFIDF(v,df[k],dc) for (k,v) in d1.items() if k not in sw}
        tfidf.append(d2)

    return tfidf

def getEuclideanDistance(d1, d2):
    sum = 0

    for (k,v) in d1.items():
        if k in d2: sum += (v - d2[k])**2
        else: sum += v**2

    for (k,v) in d2.items():
        if k not in d1: sum += v**2

    return math.sqrt(sum)

def getCosineDistance(d1, d2):
    sum = 0
    product = 0
    i = 0
    j = 0
    for (k, v) in d1.items():
        if k in d2:
            #print k
            sum += (v * d2[k])
            i += v**2
            j += d2[k]**2

        else:
            i += v ** 2

    for (k, v) in d2.items():
        if k not in d1: j += v ** 2


    # if sum == 0 or i == 0 or j == 0:
    #     print d1
    #     print sum
    #     print i
    #     print j

        #return 100000
    # print sum
    # print i
    # print j
    #if sum == 0 or i == 0 or j == 0: return 100000
    return -float(sum)/(float(math.sqrt(i))*float(math.sqrt(j)))

# def initCentroids(docs, k, T):
#     #centroids
#     i, count =0
#     D = docs.size()
#     a = {}
#     centroid =[]
#
#     while(a.size() < k):
#         i = randint(0,D)
#         if(not a.contains(i))
#
# def addtodict(dic, k):
#     dic ={}
#     if(dic.__contains__(k)):
#         dic[k]+=1
#
#     else:
#         dic[k]=0
#
#     return dic
#


Tcorrect = 0

IN_DIR = sys.argv[1]
filenames = glob.glob(os.path.join(IN_DIR,'*'))
tf = [getTermFrequencies(open(filename)) for filename in filenames]



IN_DIR = sys.argv[2]
filenamesdev = glob.glob(os.path.join(IN_DIR,'*'))
tf1 = [getTermFrequencies(open(filename)) for filename in filenamesdev]
df1 = getDocumentFrequencies(tf1)
Tdoc = filenamesdev.__len__()



#
# for term in tf:
#     print term
    #print "\n"
df = getDocumentFrequencies(tf)
#print df
# for docterm in df:
#     print docterm
sw = generateStopWords(tf, df, 200)
sw = generateStopWords(tf, df, .8)
#dev data---------
tfidf1 = getTFIDFs(tf1, df1, sw)
tfidf = getTFIDFs(tf, df, sw)

knn = 3
trainnum = 0

for dev in tfidf1:
    k = { }
    print filenamesdev[trainnum].split("/")[9]
    correct = filenamesdev[trainnum].split("/")[9].split("_")[0]
    print "votes: "
    j = 0
    minv = 10000
    for train in tfidf:
        dist = getEuclideanDistance(train, dev)
        #dist = getCosineDistance(train, dev)

        #print dist

        if k:
            #x = j-2
            if k.__len__() >= knn:
                greatest = max(k.iteritems(), key=operator.itemgetter(1))[0]
                # print "this is greatest: "
                # print greatest
                if dist < minv: minv = dist
                if k.get(greatest) > dist:
                    del k[greatest]
                    k[j]=dist
                    #print dist
            else:   k[j]=dist

        else:
            k = {j:dist}

        #print j
        #print k.get(j)
        #print k

        j+=1
#prints the name of dev train and distance
    for key in k:
        #print filenames[key]
        genre = filenames[key].split("/")[9].split("_")[0]
        print genre
        #print k[key]
        dic = {}
        if (dic.__contains__(genre)):
            dic[genre] += 1

        else:
            dic[genre] = 0

        Mgenre = max(dic.iteritems(), key=operator.itemgetter(1))[0]


    #print minv
    # print "answer:  "
    # print Mgenre
    # print "done"

    if(correct == Mgenre):
        Tcorrect +=1
    #sys.exit(0)
    trainnum += 1
    # if len(k) -1 > 3:
    #     for i in range(len(k) - 3, len(k)):
    #         print k

print "correct matches: " + Tcorrect.__str__()
print Tdoc
perofcorr = (float(Tcorrect) / Tdoc)
print perofcorr

print "percentage: " + perofcorr.__str__()
# for i in range(len(k)-3,len(k)):
#     print k[i]