from tkinter import *
from DatabaseCommunication import *
from EmailGeneration import *


Details = ['Vehicle Number','Owner-Name','License-Number','Address','Email-Id']
np="GJ23BD7935"
Info = getDetails(np)

Infolist = []

Infolist.append(str(np))
Infolist.append(Info['OwnerName'])
Infolist.append(Info['LicenseNumber'])
Infolist.append(Info['OwnerAddress'])
Infolist.append(Info['OwnerEmail'])

for i in range(2):
    cols = []

    if i==0:

        for j in range(5):
            e = Entry(relief=RIDGE)
            e.grid(row=i, column=j, sticky=NSEW)
            e.insert(END,Details[j])
            cols.append(e)
        continue

    for j in range(5):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END,Infolist[j])
    
    
def onPress():
    sendEmail(Infolist[4])

Button(text='Fetch', command=onPress).grid()
mainloop()



