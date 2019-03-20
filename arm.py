# -*- coding: utf-8 -*-

#import copy

class Token():
    def __init__(self,token):
        self.tok=token
        self.property=[]



["[","]","\n","\t","{","}","(",")","LDR","STR"," ","!","#",","]




left_sq_bracket="["
right_sq_bracket="]"
class Set():
    def __init__(self,params="",imparity=[],invert=False):
        self.params=""
        self.invert=invert
        if len(params):
            self.params="".join(sorted(params))
        else :
            self.params = ""
        self.imparity=imparity

    def __contains__(self, var):
        for (a,b) in self.imparity :
            if ord(a)<=ord(var) and  ord(var)<=ord(b) :
                return not self.invert
        for i in self.params :
            #print i
            if var==i :
                return not self.invert

        return self.invert
    def __add__(self):
        return None

    def __eq__(self,var):
        if type(var)==type(self):
            if (var.params== self.params) and (var.imparity== self.imparity):
                return True
        if self.params==var :
            return True
        return False

class state():
    def __init__(self,set,childrens=[],index=0):
        self.mark=Set(invert=True)
        self.childrens=list(childrens)
        self.set=set
        self.index_=index
        if index==0:
            self.run=self.run_without_end
        else:
            self.run = self.run_with_end


    def run_without_end(self,var):
        #print self.childrens
        for i in self.childrens :
            if ( var in i.set) :
                #print var
                #print (var in self.mark)
                return i,self.index_*(var in self.mark)

        return None ,0

    def run_with_end(self, var):
        for i in self.childrens :

            if ( var in i.set ) :
                print (var in self.mark)
                return i,self.index_*(var in self.mark)

        return None ,0








#sep=Set(" \t")
#en=Set(imparity=[("a","z"),("A","Z")])


class SM():
    def __init__(self,word,index=0):

        self.start_state = state(set(""))
        state_ = self.start_state
        for i in word :
            if type(i)==str:
                a = state(Set(i))
            else :
                a = state(i)
            state_.childrens = [a]
            state_=a
        state_.index_ = index
        self.end=list([state_])
        #print "end" ,self.endr

    def __or__(self,var):
        index=0
        if type(var) != str:
            var,index=var


        state_=self.start_state
        for i in var :
            b=True
            for j in state_.childrens :
                if j.set==i :
                    state_=j
                    b=False
                    #print i
                    break

            if b :
                a = state(Set(i))
                state_.childrens.append(a)
                state_ = a
        state_.index_=index
        self.end.append(state_)
        #print self.endr
        return self

    def __add__(self,var):

        if type(var)==type(self) :
            for i in self.end :
                #print "Before", i.childrens
                i.childrens+=var.start_state.childrens
                #print i.childrens
                print "i.childrens", i.childrens
            #self.end=list(var.end)

        """
        if type(var)==state :
            for i in self.end :
                i.childrens+=var
            #self.end = list(var.end)
        """
        return self

    def add_end(self,var):
        if type(var)==type(self) :
            for i in self.end :
                #print "Before", i.childrens
                i.childrens+=var.start_state.childrens
                #print i.childrens
                print "i.childrens", i.childrens
            self.end=list(var.end)
        return self

    def create_req(self):
        #print "B",self.end
        for i in self.end :
            #print "Before",[j.set.params for j in i.childrens]
            #print "i.childrens",i.childrens
            #print "Before",ord(i.set.params) ,i.set.params
            if  len(i.childrens):
                i.childrens+=list(self.start_state.childrens)
            else :
                i.childrens = list(self.start_state.childrens)

        return self

    def add_mark(self,mark):
        for i in self.end:
            i.mark=mark
        return self



#sep_state=state(sep)
#dec_state=state(dec)
#alpha_state=state(en)

dec=Set(imparity=[("0","9")])
sep=Set(" \t")
nsep=Set(" \t",invert=True)

ldr=(SM("LDR",4)|("STR",8)|("STRD",12 )).add_mark(sep)
hex_=SM("0x").add_end(SM([dec],16).create_req()).add_mark(sep)
#sep_state=sep_state+sep_state
sep_state=(SM(" ",1)|("\t",2),("\n",3)).create_req().add_mark(nsep)+ldr+hex_
ldr=ldr+sep_state
hex_=hex_+sep_state

sep_state=sep_state.start_state
print [i.set.params for i in sep_state.childrens]
#ldr.add_end([sep_state,alpha_state,dec_state])

#ldr=ldr.start_state.childrens


#sep_state.childrens=[dec_state,sep_state]+ldr+[alpha_state]
#dec_state.childrens=[dec_state,sep_state]
#alpha_state.childrens=[alpha_state,sep_state ]

s="\t\t\t  \t0x123   STR LDR "
word=""
f=sep_state
for i in s:
    f,index=f.run(i)
    #print index,i
    if index!=0:
        if len(word):
            print index ,word
        word=i
    else :
        word+=i




#class srtring():
