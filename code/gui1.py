from __future__ import division
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from DatabaseCommunication import *
from EmailGeneration import *
from send_sms import *
from character_sagmentation import *
from CNN_NP import *
from tkinter import messagebox
import random
import cv2
import numpy as np
import glob
from PIL import Image
import os
from scipy import ndimage, misc
import PIL.Image, PIL.ImageTk
from np_total import *
import pytesseract
import string

COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']

SIZE = 256, 256


class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("FINE GENERATION SYSTEM")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        # initialize global state
        self.number_plate_record={}
        self.imageDir = ''
        self.imageList = []
        self.nbrplateList=[]
        self.egList = []

        self.cur = 0
        self.x=''
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        self.CAPS = []
        self.NUMS = []
        for i in range(0, 10):
            self.NUMS.append(str(i))

        ALPHA = string.ascii_uppercase

        for i in ALPHA:
            self.CAPS.append(i)

        self.label = Label(self.frame, text="Video Dir:",font = "verdana 10 bold")
        self.label.grid(row=0, column=0, sticky=E)
        self.entry = Entry(self.frame,font = "verdana 10 bold",bd=2,relief=SOLID)
        self.entry.grid(row=0, column=1, sticky=W + E)           #for textbox
        self.ldBtn = Button(self.frame, text="Select Video", command=self.loadDir,font = "verdana 10 bold",bd=2,relief=SOLID)
        self.ldBtn.grid(row=0, column=2, sticky=W + E)

        self.videoPanel = Canvas(self.frame,bd=2,relief=SOLID,width=640,height=352)
        self.videoPanel.grid(row=1, column=1, rowspan=4,sticky=W + N)

        self.b1=Button(self.frame,text="Start Analysis",command=self.frame_separate,font = "verdana 10 bold",bd=2,relief=SOLID)
        self.b1.grid(row=5,column=1,sticky=W)

        self.b2 = Button(self.frame, text="Show Report",command=self.report_generation,font = "verdana 10 bold",bd=2,relief=SOLID)
        self.b2.grid(row=5, column=1, sticky=E)

        self.img_numberplate_panal=Canvas(self.frame,bd=2,relief=SOLID,width=200,height=80)
        self.img_numberplate_panal.grid(row=2,column=2,sticky=W+N,padx=20)
        self.lb1 = Label(self.frame,text='Vehicle breaking traffic rule:',font = "verdana 10 bold",bd=2,)
        self.lb1.grid(row=1, column=2, sticky=S)

        self.lb2 = Label(self.frame, text='Extracted Number Plate:',font = "verdana 10 bold",)
        self.lb2.grid(row=3, column=2, sticky=S)
        self.text_label = Label(self.frame, width=20, height=3,fg='red',font = "verdana 12 bold",bd=2,relief=SOLID)
        self.text_label.grid(row=4, column=2, sticky=N)

        self.ctrPanel = Frame(self.frame,bd=2)
        self.ctrPanel.grid(row=5, column=2, columnspan=2, sticky=N)
        self.pre_btn_photo = PhotoImage(file='prev.png')
        self.next_btn_photo=PhotoImage(file='next.png')
        self.prevBtn = Button(self.ctrPanel,image=self.pre_btn_photo,relief=SOLID,width=40,height=40,bd=2,command=self.prevImage)
        self.prevBtn.pack(side=LEFT, padx=10, pady=10)

        self.nextBtn = Button(self.ctrPanel,image=self.next_btn_photo,relief=SOLID,width=40,height=40,bd=2,command=self.nextImage)
        self.nextBtn.pack(side=RIGHT, padx=10, pady=10)
        self.progLabel = Label(self.ctrPanel, text="Prev   Next",font = "verdana 8 bold")
        self.progLabel.pack(side=LEFT, padx=5)


    def report_generation(self):
        window = Toplevel(self.parent)
        window.title("Fine Generation Report")
        l=self.number_plate_record.keys()
        Details = ['Vehicle Number', 'Owner-Name', 'License-Number', 'Address', 'Email-Id','Contact_No']

        for nbrPlt in l:
            for i in range(len(l)+1):
                cols = []
                if i == 0:
                    for j in range(6):
                        e = Entry(window,relief=SOLID,bd="3",fg="red",justify=CENTER,font = "verdana 10 bold")
                        e.grid(row=i, column=j, sticky=NSEW)
                        e.insert(END, Details[j])
                        cols.append(e)
                    continue
                Info = getDetails(self.number_plate_record[nbrPlt])
                Infolist = []
                Infolist.append(str(self.number_plate_record[nbrPlt]))
                Infolist.append(Info['OwnerName'])
                Infolist.append(Info['LicenseNumber'])
                Infolist.append(Info['OwnerAddress'])
                Infolist.append(Info['OwnerEmail'])
                Infolist.append(Info['contactno'])

                for j in range(6):
                    e = Entry(window,relief=SOLID,bd='2',justify=CENTER,font = "verdana 8 bold")
                    e.grid(row=i, column=j, sticky=NSEW)
                    e.insert(END, Infolist[j])
        Button(window,text='Notify All',command=self.onPress,font = "verdana 10 bold",bd=2,relief=SOLID).grid(sticky='E')

    def onPress(self):
        for nbp in self.number_plate_record.keys():
            Info = getDetails(self.number_plate_record[nbp])
            sendEmail(Info['OwnerEmail'])
            send_sms(Info['contactno'])


    def loadDir(self, dbg=False):
        if not dbg:
            self.fname=filedialog.askopenfilename(initialdir="/home/dhruv/PROJECT_NPD", title="Select file",filetypes=(("video files", "*.mp4"), ("all files", "*.*")))
            self.number_plate_record={}
            self.imageList=[]
            self.x=(self.fname)
            self.entry.delete(0,END)
            self.entry.insert(END,self.x)
            # open video source
            self.vid = MyVideoCapture(self.x)
            self.videoPanel.config(width=640,height = 352)
            self.delay = 30
            self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame1 = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
            self.videoPanel.create_image(0, 0, image=self.photo, anchor=NW)
        self.frame.after(self.delay, self.update)

    def start_analysis(self):
        self.frame_separate()

    def plate_detect(self):
        for i in glob.glob("./vfs/*.jpg"):
            img=cv2.imread(i)
            L = i.split(".j")
            L1 = L[0].split("s/")[1]
            img = cv2.resize(img, (500, 400))
            threshold_img = preprocess(img)
            image_countouring(L1,img, threshold_img)
        print("plate_detected")
        self.imageDir = './number_plate/'
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        #remove unnecessary images (not containing number plate)
        for im in self.imageList:
            im1=Image.open(im)
            t=pytesseract.image_to_string(im1)
            if(len(t)!=10):
                self.remove_img(im)
        # default to the 1st image in the collection
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        self.cur = 1
        self.total = len(self.imageList)
        self.loadImage()

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(str(imagepath))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.img_numberplate_panal.config(width=self.tkimg.width(), height=self.tkimg.height())
        self.img_numberplate_panal.create_image(102,2, image=self.tkimg, anchor=N)
        Img = Image.open(imagepath)
        nbr_plate = pytesseract.image_to_string(Img)
        #character_segmentation(imagepath)
        #nbr_plate=extractNumber()
        nbr_plate1=self.verify_text(nbr_plate)
        self.number_plate_record[imagepath] = nbr_plate1
        self.text_label.config(text=nbr_plate1)

    def verify_text(self,npn):
        check_list=['a','a','n','n','a','a','n','n','n','n']
        np_list=list(npn)
        for i in range(np_list.__len__()):
            if check_list[i]=='a':
                if np_list[i] not in self.CAPS:
                    if np_list[i]=='8':
                        np_list[i]='B'
                    elif np_list[i]=='0':
                        np_list[i]='D'
                    elif np_list[i]=='1':
                        np_list[i]='L'
                    elif np_list[i]=='6':
                        np_list[i]='G'
                    elif np_list[i]=='2':
                        np_list[i]='Z'
                    elif np_list[i]=='5':
                        np_list[i]='S'
            else:
                if np_list[i] not in self.NUMS:
                    if np_list[i]=='B':
                        np_list[i]='8'
                    elif np_list[i]=='D':
                        np_list[i]='0'
                    elif np_list[i]=='O':
                        np_list[i]='0'
                    elif np_list[i]=='L':
                        np_list[i]='1'
                    elif np_list[i]=='G':
                        np_list[i]='6'
                    elif np_list[i]=='S':
                        np_list[i]='5'
                    elif np_list[i]=='Z':
                        np_list[i]='2'
        ans=''.join(np_list)
        return ans


    def remove_img(self, path):
        os.remove(path)
        return

    def frame_separate(self):
        vidObj = cv2.VideoCapture(self.x)
        count = 0
        success = 1
        while success:
            success, image = vidObj.read()
            if count%10 == 0:
                cv2.imwrite("vfs/frame%d.jpg" % count, image)
            count += 1

        outPath = "./vfs"
        path = "./vfs"

        """for image_path in os.listdir(path):
            input_path = os.path.join(path, image_path)
            image_to_rotate = ndimage.imread(input_path)
            rotated = ndimage.rotate(image_to_rotate,0)
            fullpath = os.path.join(outPath, '' + image_path)
            misc.imsave(fullpath, rotated)"""
        print("Frame seperated")
        self.plate_detect()

    def nextImage(self):
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            self.cur=1
            self.loadImage()

    def prevImage(self):
        if self.cur < self.total and self.cur!=1:
            self.cur -= 1
            self.loadImage()
        elif self.cur == 0:
            self.cur=self.total
            self.loadImage()

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        #self.frame.mainloop()
if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    #root.resizable(width=True, height=True)
    root.mainloop()
