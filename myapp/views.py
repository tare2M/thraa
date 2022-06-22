from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
import random
import numpy as np
import matplotlib.pyplot as plt
from .utils import get_plot

result_string='hellow'

# Create your views here.
def index(request):
    return render(request,'index2.html')



def insertData(request):
    WV=[]
    if request.method=="POST":
       name=request.POST.get('name')
       capacity=request.POST.get('capacity')
       popN=request.POST.get('popN')
       MRate=request.POST.get('MRate')
       ItemNumber=7
       def Get_Value_Weight(M,index):
        V=0
        W=0
        for x in range(0,Item_Number):
         if(str(M[x])=='1'):
          V=V+Binefit_Weight[x][0]
          W=W+Binefit_Weight[x][1]
        return V,W,index
       def Get_The_Target_Value(CB,Item_Num):
        R=Encoding(CB,Item_Num)
        r=[0]*len(R)
        B=[0]*len(R)
        for x in range(0,len(R)):
            B[x]=[R[x][0],R[x][1],x]
        R=B
        F=[0]*len(R)
        r=[0]*len(R)
        for x in range(0,len(R)):
            r[x]=Get_Value_Weight(R[x][1],R[x][2])
            F[x]=Fit_in_Bag(r[x][2],r[x][1],r[x])
        max_V=r[0][0]
        k=0
        for o in range(0,len(R)):
            if(max_V<r[o][0]):
             k=o
             max_V=r[o][0]
        return max_V,k
       def Fit_in_Bag(x,W,M):
        fit=0
        if(W>Bag_Capacity)or(int(x)==0):
         fit=0
        else:
         fit=1
        return fit
       def Initial_Population_M (P_num,M):
        for i in range(0,P_num):
         n = random.randint(0,Coding_Bits-1)
         Population[i]=[M[n][0],M[n][1],n]
        return Population
       def Probability_Calaculator(Pop):
        totalV=0
        P=[0]*Population_num
        for x in range(0,len(Pop)):
            r=Get_Value_Weight(Pop[x][1],Pop[x][2])
            F=Fit_in_Bag(r[2],r[1], Pop)
            if int(F)==1:
             totalV=totalV+r[0]
        for x in range(0,len(Pop)):
            r=Get_Value_Weight(Pop[x][1],Pop[x][2])
            F=Fit_in_Bag(r[2],r[1], Pop)
            if (int(F)==1)or(Pop[x][2]!=0):
             P[x]=[r[2],r[0]/totalV]
            else:
             P[x]=[r[2],0]
        return P
       def Survived_Gen(M):
        W=0
        for i in range(0,len(M)):
            if M[i][1]!=0:
             W=W+1;
        Choices=[0]*W
        j=0
        for i in range(0,len(M)):
             if M[i][1]!=0:
              Choices[j]=M[i]
              j=j+1
        return Choices
       def Setting_The_Rollet(Gen):
        N=len(Gen)
        step=0
        S=[0]*N
        IndexProb=[0]*N
        NProb=[0]*N
        ProbM=[0]*N
        Angle=[0]*N
        for i in range (0,N):
            IndexProb[i]=C[i][0]
            NProb[i]="C_"+str(Gen[i][0])
            ProbM[i]=Gen[i][1]
            Angle[i]=0
        for i in range(0,len(ProbM)):
            if i==(len(ProbM)-1):
             S[i]=1
             break;
            step= ProbM[i+1]-ProbM[i]
            if step < 0:
             step=step*-1
            S[i]=step
            Angle[i]=step+ProbM[i]
        wholeS=0
        for i in range(0,len(S)):
             if i==(len(ProbM)-1):
              Angle[i]=1
              break;
             wholeS=S[i]+wholeS
             Angle[i]=wholeS+ProbM[1]
        SelectedI=[0]*Population_num
        for x in range(0,Population_num):
            n = random.randint(0,100)/100
            for i in range(0,len(Angle)):
             if n<= Angle[i]:
              SelectedI[x]=IndexProb[i]
              break;
        return SelectedI
       def New_Generation(I):
        Next_G=[]
        NG=[]
        Parent_G=[]
        PG=[]
        for r in range(0,int(len(I)/2)):
            Married=Crossover(I)
            G1=get_first_Parent(Married)
            Parent_G.append(G1)
            PG.append(Bin_to_Dec(G1))
            G2=get_second_Parent(Married)
            Parent_G.append(G2)
            PG.append(Bin_to_Dec(G2))
            C1=get_first_chid(Married)
            C1=mutatuion(C1, mutation_rate)
            Next_G.append(C1)
            NG.append(Bin_to_Dec(C1))
            C2=get_second_chid(Married)
            C2=mutatuion(C2, mutation_rate)
            Next_G.append(C2)
            NG.append(Bin_to_Dec(C2))
            r=r+1
        return Parent_G,Next_G
       def decimalToBinary(n):
         return bin(n).replace("0b", "")
       def Encoding(N,Item_Number):
         Mat=[""]*N #pupulation
         for x in range(0,N):
            a=decimalToBinary(x)
            N=Item_Number-len(a)
            a="0"*N+a
            A=list(a)
            Mat[x]=["C_"+str(x),A]#['C_127', ['1', '1', '1', '1', '1', '1', '1']
         return Mat
       def Crossover(S):
        n1=random.randint(0,len(S)-1)
        n2=random.randint(0,len(S)-1)
        P1=Mat[S[n1]][1]
        P2=Mat[S[n2]][1]
        G1o=P1.copy()
        G2o=P2.copy()
        Crossover_len=random.randint(1, Item_Number-1)
        TG1=[0]*Crossover_len
        TG2=[0]*Crossover_len
        for i in range(0,len(TG1)):
            TG1[i]=P1[len(TG1)-i]
            TG2[i]=P2[len(TG1)-i]
        Cross=TG1.copy()
        TG1=TG2.copy()
        TG2=Cross.copy()
        for i in range(0,len(TG1)):
             G1o[i]=TG1[i]
             G2o[i]=TG2[i]
        return [P1,P2],[G1o,G2o]
       def Bin_to_Dec(M):
        x=0
        for i in range(0,len(M)):
         x=int(M[Item_Number-1-i])*2**(i)+x
        return x
       def Get_Max_Value(R):
            GF=[0]*len(R)
            Gr=[0]*len(R)
            for x in range(0,len(R)):
                Gr[x]=Get_Value_Weight(R[x][1],R[x][2])
                GF[x]=Fit_in_Bag(Gr[x][2],Gr[x][1],Gr[x])
            Gmax_V=Gr[0][0]
            Gk=0
            for o in range(0,len(R)):
                if(Gmax_V<=Gr[o][0]):
                 Gk=Gr[o][2]
                 Gmax_V=Gr[o][0]
            return Gmax_V, Gk
       def mutatuion(G,MR):
            b = np.random.randint(0,len(G))/10
            i=np.random.randint(0,len(G)-1)+1
            if float(b)< MR :
                if str(G[i]) =='0':
                 G[i]='1'
                if str(G[i])=='1':
                 G[i]='0'
            return G
       def get_first_Parent(M):
            P= M[0][0]
            return P
       def get_second_Parent(M):
            P= M[0][1]
            return P
       def get_first_chid(M):
            P= M[1][0]
            return P
       def get_second_chid(M):
            P= M[1][1]
            return P
       def Get_Parents(XG):
            Parent_G=XG[0].copy()
            return Parent_G
       def Get_Childern(XG):
            Next_G=XG[1].copy()
            return Next_G

       V1=request.POST.get('V1')
       W1=request.POST.get('W1')
       V2=request.POST.get('V2')
       W2=request.POST.get('W2')
       V3=request.POST.get('V3')
       W3=request.POST.get('W3')
       V4=request.POST.get('V4')
       W4=request.POST.get('W4')
       V5=request.POST.get('V5')
       W5=request.POST.get('W5')
       V6=request.POST.get('V6')
       W6=request.POST.get('W6')
       V7=request.POST.get('V7')
       W7=request.POST.get('W7')
       #constints
       Max_Generating=int(name)
       Bag_Capacity=int(capacity)
       Item_Number=int(ItemNumber)
       Coding_Bits=2**Item_Number
       Population_num=int(popN)
       if Population_num % 2 !=0:
           Population_num=Population_num+1
       Population=[0]*Population_num
       mutation_rate=float(MRate)
       #object :weight,Value
       Binefit_Weight =[[int(W1),int(V1)], [int(W2),int(V2)], [int(W3),int(V3)], [int(W4),int(V4)], [int(W5),int(V5)],[int(W6),int(V6)],[int(W7),int(V7)]]
       print("name =", name,capacity,popN,MRate,Item_Number,V1,W1,V2,W2,V3,W3,V4,W4,V5,W5,V6,W6,V7,W7,WV,Binefit_Weight)
       problem_entrys=["The Maximum Generating Rounds: "+str(name),"The Bag Capacity: "+str(capacity),"The Population Number: "+str(popN), "The Mutation Rate: "+str(MRate)+"%","There are "+str(Item_Number)+" Items to Pick" ,"The First Item Value is "+str( V1)+" The Weight "+str(W1),"The 2nd Item Value is "+str( V2)+" The Weight "+str(W2),"The 3rd Item Value is "+str( V3)+" The Weight "+str(W3),"The 4th Item Value is "+str( V4)+" The Weight "+str(W4),"The 5th Item Value is "+str( V5)+" The Weight "+str(W5),"The 6th Item Value is "+str( V6)+" The Weight "+str(W6),"The 7th Item Value is "+str( V7)+" The Weight "+str(W7)]
       Steps=["Step 1: Initialization"]
       Result_string="********Knap Sack Problem **********\n \n*******Genetice Algorithm *********\n\n"
       Max_G=[]
       Result_string=Result_string+"We are Encoding!\n"
       Steps.append("We are Encoding the posibilities of the "+str(Item_Number)+" items into (0,1) GENS!")
       Mat=Encoding(Coding_Bits,Item_Number)
       Gens=['The Created Gens']+Mat
       TargetV=Get_The_Target_Value(Coding_Bits, Item_Number)
       Result_string=Result_string+"The Max Value for all Gens is "+str(TargetV[0])+ " it belongs to the C_"+str(TargetV[1])+"\n"
       Steps=Steps+["Step 2: Selection"]
       #print("We are chosing",Population_num,"random Gens!")
       Result_string=Result_string+"We are chosing " +str(Population_num)+" random Gens!\n"
       Steps=Steps+["The Max Value for all Gens is "+str(TargetV[0])+ " it belongs to the C_"+str(TargetV[1])+"\n" ]
       Steps=Steps+["We are chosing " +str(Population_num)+" random Gens from "+str(len(Mat))+" Gens"]
       Population=Initial_Population_M(Population_num, Mat)
       Result_string=Result_string+"Initial Step: Creating the initial population\n"

       Result_string=Result_string+"Starting Fitness Assignemt"
       Steps=Steps+["Step 3: Starting Fitness Assignemt"]
       Steps=Steps+["Step 4: Cross over at a Random Point"]
       Steps=Steps+ ["Step 5 with Mutation Rate "+str(mutation_rate)]
       Steps=Steps+["Step 6: Sevrivior Selection "]
       Steps=Steps+["Creating Generation till We reach the Maximum Number of Generation We Choose to Create!"]
       Round=0
       Genetations=[]
       while(Round!=Max_Generating):
            Genetations.append(["**************The Generation #"+str(Round +1)+"*********"])
            Result_string=Result_string+"\n**************The Generation #"+str(Round +1)+"*********"
            PP=Probability_Calaculator(Population)
            Genetations=Genetations+["Picking The best Gen"]
            Result_string=Result_string+"Picking The best Gen"
            Genetations=Genetations+["Picking The best Gen using the Rollets"]
            C=Survived_Gen(PP)
            Gen=C.copy()
            SelectedI=Setting_The_Rollet(Gen)
            Genetations=Genetations+[SelectedI]
            XG=New_Generation(SelectedI)
            Genetations=Genetations+["Cross over at a Random Point"]
            Genetations=Genetations+ ["Mutation Happens with Rate "+str(mutation_rate)+"% \n"]

            Result_string=Result_string+"\n\nCross over happening and with Mutation Rate "+str(mutation_rate)+"% \n"
            A=Get_Childern(XG)
            PE=[0]*len(A)
            for e in range(0,len(A)):
             a="C_"+str(Bin_to_Dec(A[e]))
             PE[e]=[a,A[e],Bin_to_Dec(A[e])]
            Round=Round+1
            Population=PE
            A=Get_Max_Value(PE)
            Result_string=Result_string+"the max value for this generation is "+str(A[0])+ " it belongs to the C_"+str(A[1])
            Genetations=Genetations+ ["The Max Value for This Generation is "+str(A[0])+ " it belongs to the C_"+str(A[1])]
            Max_G.append(A[0])

       MaxGV=[max(Max_G)]*len(Max_G)
       MinGV=[min(Max_G)]*len(Max_G)
       avgGV=[sum(Max_G)/len(Max_G)]*len(Max_G)
       BestGV=[TargetV[0]]*len(Max_G)
       Result_string=Result_string+"\n----------------- \n\nFinal statiestics are : \n"

       Result_string=Result_string+"\nThe Maximum Value for accpeable Gens is "+str(MaxGV[0])
       Result_string=Result_string+"\nThe Minimum Value for accpeable Gens is "+str(MinGV[0])
       Result_string=Result_string+"\nThe avrage Value for accpeable Gens is "+str(avgGV[0])
       Result_string=Result_string+"\nThe Best Value for accpeable Gens is "+str(BestGV[0])
       axisX=[]
       axisY=[]
       for x in range(0,len(Max_G)):
        axisX.append(x)
        axisY.append(Max_G[x])
       chart=get_plot(axisX,axisY,MaxGV,MinGV,avgGV,BestGV)
       print(Result_string)

       inputs='Thank You!!'
       #the Dynamic Algorithe
       def knapSack(W, wt, val):
            n=len(val)
            table = [[0 for x in range(W + 1)] for x in range(n + 1)]

            for i in range(n + 1):
                for j in range(W + 1):
                    if i == 0 or j == 0:
                        table[i][j] = 0
                    elif wt[i-1] <= j:
                        table[i][j] = max(val[i-1] + table[i-1][j-wt[i-1]],  table[i-1][j])
                    else:
                        table[i][j] = table[i-1][j]

            return table[n][W]

       val=[]
       wt=[]
       for x in range(0,len( Binefit_Weight)):
            val.append(int(Binefit_Weight[x][0]))
            wt.append(int(Binefit_Weight[x][1]))
       Dynamic=['The Dynamic Algorith Result',knapSack(Bag_Capacity,wt,val)]


       values=['The Maximum Value for accpeable Gens is '+str(MaxGV[0]),'The Minimum Value for accpeable Gens is' +str(MinGV[0]),'The avrage Value for accpeable Gens is '+str(avgGV[0]),'The Best Value for accpeable Gens is '+str(BestGV[0])]
       return render(request,'index2.html',{"chart":chart,"C":values,"Steps":Steps,"Gens":Gens,"inputs":Steps,"state_name":inputs,"Genetations":Genetations,"entrys":problem_entrys,'Dyn_R':Dynamic})

















