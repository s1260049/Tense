import tkinter
import nltk
import re

color_dic = {'yellow':'\033[43m', 'red':'\033[31m', 'blue':'\033[34m', 'end':'\033[0m'}


tag=[]
tag.append("a ")
tag.append("")
tag.append("")
space=" "

name=""

def print_hl(text, keyword, color="yellow"):
    for kw in keyword:
        bef = kw
        aft = color_dic[color] + kw + color_dic["end"]
        text = re.sub(bef, aft, text)
    print("plain: "+text.capitalize())
    #Quote -> https://qiita.com/yuto16/items/5618e4147b749177bd15
    
def delete_btn():
    str.delete(0,tkinter.END)
    plain['text']=str.get()

def input_btn():
    word=str.get()
    plain['text']=word
    tense_check(word)
    name=f"{tag[0]}{tag[1]}{tag[2]}"
    print("Grammatical tense: "+"\033[34m{}\033[0m".format(name))
    if name=="":
        tense_lbl['text']="..."
    else:
        tense_lbl['text']=name

def tense_check(word):
    s=word.lower()
    s=s.replace('i ','I ')
    verbs=[]
    i=0
    tense=-1
    
    words=nltk.word_tokenize(s)
    pos=nltk.pos_tag(words)
    print(pos)     #usage: check tags
    for w in pos:
        if w[0]=="will":
            tense=0
            tag[0]="Futute "
            verbs=aspect_check(pos,i,tense)
            break
        elif w[1]=="VBD":
            tense=1
            tag[0]="Past "
            verbs=aspect_check(pos,i,tense)
            break
        elif w[1]=="VB" or w[1]=="VBP" or w[1]=="VBZ":
            tense=2
            tag[0]="Present "
            verbs=aspect_check(pos,i,tense)
            break
        else:
            i+=1
    if tense==-1:
        tag[0]="..."
        tag[1]=""
        tag[2]=""
        v_lbl['text']="..."
    else:
        v_col=print_hl(word.lower(), verbs)
        v_lbl['text']=verbs
        
        
    

def aspect_check(pos,i,tense):
    phrase=[]
    befound=False
    if tense==0:
        phrase.append("will")
        for j in range(i+1,len(pos)):
            #print(pos[j][0])
            if pos[j][1]=="RB" or pos[j][1]=="NN" or pos[j][1]=="NNS" or pos[j][1]=="NNP" or pos[j][1]=="NNPS" or pos[j][1]=="PRP":
                continue
            elif pos[j][0]=="have":
                tag[1]="perfect "
                phrase.append(pos[j][0])
            elif pos[j][1]=="VBN":
                if pos[j][0]=="been" and pos[j+1][1]=="VBG":
                    tag[2]="progressive"
                    phrase.append(pos[j][0])
                    phrase.append(pos[j+1][0])
                else:
                    tag[2]="simple"
                    phrase.append(pos[j][0])
                break
            elif pos[j][0]=="be" and pos[j+1][1]=="VBG":
                tag[2]="progressive"
                phrase.append(pos[j][0])
                phrase.append(pos[j+1][0])
                break
            else:
                tag[1]=""
                tag[2]="simple"
                phrase.append(pos[j][0])
                break
            

    elif tense==1:
        for j in range(i,len(pos)):
           # print(pos[j][0])
            if pos[j][1]=="RB" or pos[j][1]=="NN" or pos[j][1]=="NNS" or pos[j][1]=="NNP" or pos[j][1]=="NNPS" or pos[j][1]=="PRP":
                continue
            elif pos[j][0]=="was" or pos[j][0]=="were":
                tag[1]=""
                tag[2]="progressive"
                phrase.append(pos[j][0])
                befound=True
            elif pos[j][1]=="VBG":
                if befound:
                    phrase.append(pos[j][0])
                break
            
            elif pos[j][0]=="had":
                tag[1]="perfect "
                phrase.append(pos[j][0])
                
            elif pos[j][1]=="VBN":
                if pos[j][0]=="been": 
                    tag[2]="progressive"
                    phrase.append(pos[j][0])
                    befound=True
                else:
                    tag[2]="simple"
                    phrase.append(pos[j][0])
                    break
            
            else:
                tag[1]=""
                tag[2]="simple"
                if befound==False:
                    phrase.append(pos[j][0])
                if j!=0:    
                    break

    elif tense==2:
        for j in range(i,len(pos)):
            #print(pos[j][0]+tag[1])
            if pos[j][1]=="RB" or pos[j][1]=="NN" or pos[j][1]=="NNS" or pos[j][1]=="NNP" or pos[j][1]=="NNPS" or pos[j][1]=="PRP":
                continue
            elif pos[j][0]=="am" or pos[j][0]=="is" or pos[j][0]=="are":
                tag[1]=""
                tag[2]="progressive"
                phrase.append(pos[j][0])
                befound=True
            elif pos[j][1]=="VBG":
                if befound:
                    phrase.append(pos[j][0])
                break

            elif pos[j][0]=="have" or pos[j][0]=="has":
                tag[1]="perfect "
                phrase.append(pos[j][0])

            elif pos[j][1]=="VBN" or pos[j][1]=="VBD":
                if pos[j][0]=="been":
                    tag[2]="progressive"
                    phrase.append(pos[j][0])
                    befound=True
                else:
                    tag[2]="simple"
                    phrase.append(pos[j][0])
                    break

            else:
                tag[1]=""
                tag[2]="simple"
                if befound==False:
                    phrase.append(pos[j][0])
                if j!=0:
                    break
    return phrase
    
    
#---Tkinker GUI Initialization----    
root= tkinter.Tk()
root.geometry('600x400')
root.title('tense checker')
lbl=tkinter.Label(text='Sentence:',bg='#00ffff')
lbl.place(x=20,y=20)
lbl2=tkinter.Label(text='Plain:',bg='#00ffff')
lbl2.place(x=20,y=50)
lbl3=tkinter.Label(text='Verbs:',bg='#00ffff')
lbl3.place(x=20,y=80)

str=tkinter.Entry(width=40)
str.insert(tkinter.END,"I study nltk.")
str.place(x=100,y=20)

btnin = tkinter.Button(root, text='Input', command=input_btn)
btnin.place(x=250,y=300)

btndelete= tkinter.Button(root,text='Delete',command=delete_btn)
btndelete.place(x=300,y=300)

plain=tkinter.Label(text=str.get(),bg='#00ffff')
plain.place(x=100,y=50)

v_lbl=tkinter.Label(text="study",bg='#00ffff')
v_lbl.place(x=100,y=80)


tense=tkinter.Label(text='Gramatical Tense: ',bg='#00ffff')
tense.place(x=20,y=110)

tense_lbl=tkinter.Label(text='Present simple',bg='#00ffff')
tense_lbl.place(x=170,y=110)



root.configure(bg="#00ffff")
root.mainloop()


#This program checks tense of first verb in a sentence. This program has not worked coreectly about auxilary verbs except for "will". We have to download NLTK_data individually to run this program because this program uses NLTK.

#Usage: 1.Type one sentence on GUI;
#       2.Click "Input" button.
#       3.Get grammatical tense and verb phreses on GUI and console screen. On #         console, verb phrases are colored. 
