# ###  - By TheHighway ### #
# ########################################################## #

import xbmc,xbmcgui,urllib,urllib2,os,sys,logging,array,re,time,datetime,random,string,StringIO,xbmcplugin,xbmcaddon
from config import Config as Config
import common as Common
from common import *
import common
import splash_highway as splash

def DoA(a): xbmc.executebuiltin("Action(%s)" % a)
def SFX(n,e='.wav'):
	if len(n)==0: return
	snd=art(n,e)
	try: xbmc.playSFX(snd,False)
	except: 
		try: xbmc.playSFX(snd)
		except: pass

class MyWindow(xbmcgui.Window):
	visuals={}; button={}; Mistakes=0; NoOfMoves=0; 
	countA=0; countB=0; LineLength=0; 
	MazeFont='font10'; cUser='$'; cEnd='E'; cStart='S'; cWall='#'; cPath=' '; 
	MazeVisL=630; MazeVisT=20; WH=64*2; 
	##
	tWinner='winner'; GridButton={}; GridButtonUD={}; GridButtonUDC={}; GridButtonUDN={}; 
	Hands=[1,2,3];
	PuzzleGridA=''; PuzzleGridB=''; PuzzleWordList=''; PuzzleFileHolder=''; 
	def __init__(self):
		self.MazeVisW=self.WH; self.MazeVisH=self.WH; 
		##
		self.Fanart=(xbmc.translatePath(Config.fanart)); self.b1=artp("black1"); self.current=0; self.content=[]; self.scr={}; self.scr['L']=0; self.scr['T']=0; self.scr['W']=1280; self.scr['H']=720; 
		self.AniTime=' time=2000 '; self.AniEnd=' end=80 '; 
		#note("HUB-HUG Movement Series","Please wait.  Preparing screen.  Load Time may vary from device to device.",delay=10000); 
		self.LoadGridFile(); 
		self.makePageItems(); 
	def LoadGridFile(self):
		self.PuzzlePath=xbmc.translatePath(os.path.join(Config.path,'puzzles')); 
		self.PuzzleFiles=os.listdir(self.PuzzlePath); debob(self.PuzzleFiles); 
		zz=self.PuzzleFiles; 
		for z in zz:
			if '.bak' in z: self.PuzzleFiles.remove(z)
		PuF=self.PuzzleFiles[random.randint(0,len(self.PuzzleFiles)-1)]; 
		self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		if tfalse(SettingG("select-puzzle"))==True:
			dialog=xbmcgui.Dialog()
			fn=str(dialog.browse(1,'Select Puzzle','files','.txt|.puzzle|.puz',False,False,self.PuzzleFile,False))
			try:
				if (fn==False) or (len(fn)==0): self.close; return
				if len(fn) > 1: deb('fn',fn); self.PuzzleFile=fn; 
			except: pass
		#self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		deb('Random File Chosen',self.PuzzleFile); self.PuzzleFileHolder=Common._OpenFile(self.PuzzleFile); deb('Length of Grid File',str(len(self.PuzzleFileHolder))); 
		self.PuzzleFileHolder=self.PuzzleFileHolder.strip().replace('\a','\n').replace('\r','\n').replace('\n\n','\n').strip()
		self.PuzzleFileHolder_Original=''+self.PuzzleFileHolder
		self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cStart,self.cUser,1)
		self.LineLength=len(self.PuzzleFileHolder.split('\n')[0]);
		#self.PrepareMaze(self.PuzzleFileHolder)
		##
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
	def PrepareMaze(self,t):
		t=t.replace(self.cPath,cFL(self.cWall,'black'))
		#t=t.replace(self.cPath,cFL(self.cWall,'black'))
		t=t.replace(self.cUser, cFL(self.cUser,'lightblue'), 1)
		t=t.replace(self.cEnd, cFL(self.cEnd,'red'), 1) 
		t=t.replace(self.cStart, cFL(self.cStart,'green'), 1) 
		t=cFL(t,'mediumpurple')
		self.PuzzleFileHolder_Publish=t
		self.HoroTxt.setText(self.PuzzleFileHolder_Publish)
	def makePageItems(self):
		focus=artp("button-focus_lightblue"); nofocus=artp("button-focus_seagreen"); self.background=self.Fanart; #self.background=artj("backdrop_temp"); 
		## ### ## Background
		self.BG=xbmcgui.ControlImage(self.scr['L'],self.scr['T'],self.scr['W'],self.scr['H'],self.background,aspectRatio=0); self.addControl(self.BG)
		self.BG.setAnimations([('WindowOpen','effect=fade '+self.AniTime+' start=0')])
		## ### ##
		l=95; t=20; #l=195; t=20; 
		l=100; 
		#w=self.scr['W']-l-30; h=self.scr['H']-(t*2)-100-36; 
		w=self.scr['W']-(l*2); h=self.scr['H']-(t*2); 
		w=self.scr['W']-(l+t-10); 
		self.HoroTxtBG=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=self.b1,noFocusTexture=self.b1); 
		self.HoroTxt=xbmcgui.ControlTextBox(l+10,t+2,w-20,h-4,font=self.MazeFont,textColor="0xFFFFFFFF"); 
		zz=[self.HoroTxtBG,self.HoroTxt]
		for z in zz: self.addControl(z); #z.setAnimations([('WindowOpen','effect=fade delay=2000 time=2000 start=0 end=80')]); 
		self.HoroTxtBG.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0 end=90')]); 
		self.HoroTxt.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		#self.HoroTxt.setText("blah..........."); 
		## ### ## Addon Title
		zz=["XBMCHUB","Your","HUB-HUG"]; w=1000; h=50; l=15; t=700; t=560; self.LabTitleText=Config.name; self.LabTitle=xbmcgui.ControlLabel(l,t,w,h,'','font30','0xFFFF0000',angle=90); self.addControl(self.LabTitle)
		for z in zz:
			if z+" " in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace(z+" ","[COLOR deepskyblue][B][I]"+z+"[/I][/B][/COLOR]  [CR]")
		if "Highway" in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace("Highway","[COLOR tan]Highway[/COLOR]")
		self.LabTitle.setAnimations([('WindowOpen','effect=slide delay=1000 time=1000 start=-100')]); self.LabTitle.setLabel(self.LabTitleText); 
		## ### ## Exit
		w=135; h=32; l=20; t=70; t=170; 
		self.button[0]=xbmcgui.ControlButton(l,t,w,h,"Exit",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.button[0])
		zz=[self.button[0]] #,self.button[1],self.button[2]]
		for z in zz: z.setAnimations([('WindowOpen','effect=rotate delay=0 time=1 center='+str(l)+','+str(t)+' end=90')])
		## ### ## Movements
		#self.button[0].controlRight(self.GridButton[0]); self.button[0].controlDown(self.GridButton[0]); 
		#zz=[self.HoroTxtBG,self.HoroTxt]; bZ=self.button[0]; 
		#for z in zz: z.controlUp(bZ); z.controlLeft(bZ); z.controlRight(bZ); z.controlDown(bZ); 
		## ### ## Focus
		#self.setFocus(self.button[0])
		self.setFocus(self.HoroTxtBG); 
		## ### ## 
		self.makeVisualItems(); 
		if (tfalse(SettingG("show-map"))==True): self.PrepareMaze(self.PuzzleFileHolder); 
		self.displayVisualItems(self.PuzzleFileHolder.index(self.cUser)); 
		## ### ## 
	def displayVisualItem(self,iTag,visImg='f_black2'):
		visImg=artp(visImg); 
		#try: 
		self.visuals[iTag].setImage(visImg,True);
		#except: 
		#	try: self.visuals[iTag].setImage(visImg,True);
		#	except: pass
		
	def checkData(self,Pos):
		defaultMissing='ThumbShadow'; 
		if Pos < 0: return defaultMissing
		if Pos > len(self.PuzzleFileHolder): return defaultMissing
		try:
			P=self.PuzzleFileHolder[Pos]; 
			#deb(str(Pos),P); 
			if   P==self.cWall: return 'f_purple'
			elif P==self.cEnd: return 'home-favourites-FO_red'
			elif P==self.cStart: return 'home-power-FO_green'
			elif P==self.cPath: return 'f_black2'
			elif P==self.cUser: return 'f_seagreen'
			else: return defaultMissing
		except: return defaultMissing
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
	def displayVisualItems(self,NewPos):
		self.displayVisualItem('L0C0',self.checkData( NewPos-((self.LineLength+1)*2)-2 )); 
		self.displayVisualItem('L0C1',self.checkData( NewPos-((self.LineLength+1)*2)-1 )); 
		self.displayVisualItem('L0C2',self.checkData( NewPos-((self.LineLength+1)*2)-0 )); 
		self.displayVisualItem('L0C3',self.checkData( NewPos-((self.LineLength+1)*2)+1 )); 
		self.displayVisualItem('L0C4',self.checkData( NewPos-((self.LineLength+1)*2)+2 )); 
		
		self.displayVisualItem('L1C0',self.checkData( NewPos-((self.LineLength+1)*1)-2 )); 
		self.displayVisualItem('L1C1',self.checkData( NewPos-((self.LineLength+1)*1)-1 )); 
		self.displayVisualItem('L1C2',self.checkData( NewPos-((self.LineLength+1)*1)-0 )); 
		self.displayVisualItem('L1C3',self.checkData( NewPos-((self.LineLength+1)*1)+1 )); 
		self.displayVisualItem('L1C4',self.checkData( NewPos-((self.LineLength+1)*1)+2 )); 
		
		self.displayVisualItem('L2C0',self.checkData( NewPos-((self.LineLength+1)*0)-2 )); 
		self.displayVisualItem('L2C1',self.checkData( NewPos-((self.LineLength+1)*0)-1 )); 
		self.displayVisualItem('L2C2',self.checkData( NewPos )); 
		self.displayVisualItem('L2C3',self.checkData( NewPos-((self.LineLength+1)*0)+1 )); 
		self.displayVisualItem('L2C4',self.checkData( NewPos-((self.LineLength+1)*0)+2 )); 
		
		self.displayVisualItem('L3C0',self.checkData( NewPos+((self.LineLength+1)*1)-2 )); 
		self.displayVisualItem('L3C1',self.checkData( NewPos+((self.LineLength+1)*1)-1 )); 
		self.displayVisualItem('L3C2',self.checkData( NewPos+((self.LineLength+1)*1)-0 )); 
		self.displayVisualItem('L3C3',self.checkData( NewPos+((self.LineLength+1)*1)+1 )); 
		self.displayVisualItem('L3C4',self.checkData( NewPos+((self.LineLength+1)*1)+2 )); 
		
		self.displayVisualItem('L4C0',self.checkData( NewPos+((self.LineLength+1)*2)-2 )); 
		self.displayVisualItem('L4C1',self.checkData( NewPos+((self.LineLength+1)*2)-1 )); 
		self.displayVisualItem('L4C2',self.checkData( NewPos+((self.LineLength+1)*2)-0 )); 
		self.displayVisualItem('L4C3',self.checkData( NewPos+((self.LineLength+1)*2)+1 )); 
		self.displayVisualItem('L4C4',self.checkData( NewPos+((self.LineLength+1)*2)+2 )); 
		
		zz=[['L1C2B',( NewPos-((self.LineLength+1)*1)-0 )],['L2C1B',( NewPos-((self.LineLength+1)*0)-1 )],['L2C3B',( NewPos-((self.LineLength+1)*0)+1 )],['L3C2B',( NewPos+((self.LineLength+1)*1)-0 )]]
		for iTag,Pos in zz:
			try:
				P=self.PuzzleFileHolder[Pos]; 
				if   (P==self.cPath): self.visuals[iTag].setVisible(True)
				elif (P==self.cEnd): self.visuals[iTag].setVisible(True)
				elif (P==self.cStart): self.visuals[iTag].setVisible(True)
				elif (P==self.cPath): self.visuals[iTag].setVisible(True)
				elif (P==self.cWall): self.visuals[iTag].setVisible(False)
				else: self.visuals[iTag].setVisible(False)
			except: self.visuals[iTag].setVisible(False)
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.LineLength
		#return
	def makeVisualItem(self,Type,iTag,l,t,w,h,visImg='f_black2'):
		visImg=artp(visImg); visImgB=artp('OverlayWatched_orange'); 
		if Type.upper()=='B':
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); 
			self.addControl(self.visuals[iTag])
			self.visuals[iTag+'B']=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=visImgB,noFocusTexture=visImgB); 
			self.addControl(self.visuals[iTag+'B'])
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
			self.visuals[iTag+'B'].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		elif Type.upper()=='I':
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); 
			self.addControl(self.visuals[iTag])
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		else: return
	def makeVisualItems(self):
		initVis='f_black2'; w=self.MazeVisW; h=self.MazeVisH; l=self.MazeVisL; t=self.MazeVisT; 
		self.makeVisualItem("I","L0C0",l+(w*0),t+(h*0),w,h,visImg=initVis)
		self.makeVisualItem("I","L0C1",l+(w*1),t+(h*0),w,h,visImg=initVis)
		self.makeVisualItem("I","L0C2",l+(w*2),t+(h*0),w,h,visImg=initVis)
		self.makeVisualItem("I","L0C3",l+(w*3),t+(h*0),w,h,visImg=initVis)
		self.makeVisualItem("I","L0C4",l+(w*4),t+(h*0),w,h,visImg=initVis)
		
		self.makeVisualItem("I","L1C0",l+(w*0),t+(h*1),w,h,visImg=initVis)
		self.makeVisualItem("I","L1C1",l+(w*1),t+(h*1),w,h,visImg=initVis)
		self.makeVisualItem("B","L1C2",l+(w*2),t+(h*1),w,h,visImg=initVis)
		self.makeVisualItem("I","L1C3",l+(w*3),t+(h*1),w,h,visImg=initVis)
		self.makeVisualItem("I","L1C4",l+(w*4),t+(h*1),w,h,visImg=initVis)
		
		self.makeVisualItem("I","L2C0",l+(w*0),t+(h*2),w,h,visImg=initVis)
		self.makeVisualItem("B","L2C1",l+(w*1),t+(h*2),w,h,visImg=initVis)
		self.makeVisualItem("I","L2C2",l+(w*2),t+(h*2),w,h,visImg='f_seagreen')
		self.makeVisualItem("B","L2C3",l+(w*3),t+(h*2),w,h,visImg=initVis)
		self.makeVisualItem("I","L2C4",l+(w*4),t+(h*2),w,h,visImg=initVis)
		
		self.makeVisualItem("I","L3C0",l+(w*0),t+(h*3),w,h,visImg=initVis)
		self.makeVisualItem("I","L3C1",l+(w*1),t+(h*3),w,h,visImg=initVis)
		self.makeVisualItem("B","L3C2",l+(w*2),t+(h*3),w,h,visImg=initVis)
		self.makeVisualItem("I","L3C3",l+(w*3),t+(h*3),w,h,visImg=initVis)
		self.makeVisualItem("I","L3C4",l+(w*4),t+(h*3),w,h,visImg=initVis)
		
		self.makeVisualItem("I","L4C0",l+(w*0),t+(h*4),w,h,visImg=initVis)
		self.makeVisualItem("I","L4C1",l+(w*1),t+(h*4),w,h,visImg=initVis)
		self.makeVisualItem("I","L4C2",l+(w*2),t+(h*4),w,h,visImg=initVis)
		self.makeVisualItem("I","L4C3",l+(w*3),t+(h*4),w,h,visImg=initVis)
		self.makeVisualItem("I","L4C4",l+(w*4),t+(h*4),w,h,visImg=initVis)
	def onAction(self,action):
		try: F=self.getFocus()
		except: F=False
		if   action == Config.ACTION_PREVIOUS_MENU: self.CloseWindow1st()
		elif action == Config.ACTION_NAV_BACK: self.CloseWindow1st()
		else:
		#elif (F==self.HoroTxtBG) or (F==self.HoroTxtBG):
			try: self.DoFight(action,F)
			except: pass
	def onControl(self,control):
		if   control==self.button[0]: self.CloseWindow1st()
		#elif (F==self.HoroTxtBG) or (F==self.HoroTxtBG):
		else:
			try:
				if self.visuals['L1C2B']==control: self.onAction(Config.ACTION_MOVE_UP)
				if self.visuals['L2C1B']==control:self.onAction(Config.ACTION_MOVE_LEFT)
				if self.visuals['L2C3B']==control:self.onAction(Config.ACTION_MOVE_RIGHT)
				if self.visuals['L3C2B']==control:self.onAction(Config.ACTION_MOVE_DOWN)
			except: pass
		##
	def DoFight(self,action,F):
		#self.LineLength
		MoveValid=False; 
		try: CurPos=self.PuzzleFileHolder.index(self.cUser); 
		except:
			#deb('unable to grab CurPos',str(action)); 
			return
		if   action==Config.ACTION_MOVE_LEFT:  NewPos=CurPos-1
		elif action==Config.ACTION_MOVE_RIGHT: NewPos=CurPos+1
		elif action==Config.ACTION_MOVE_UP:    NewPos=CurPos-(self.LineLength+1)
		elif action==Config.ACTION_MOVE_DOWN:  NewPos=CurPos+(self.LineLength+1)
		else: 
			#deb('unhandled action',str(action)); 
			return
		#debob('\n'+self.PuzzleFileHolder); 
		if NewPos > len(self.PuzzleFileHolder): MoveValid=False; 
		elif NewPos < 0: MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]==self.cWall: MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]=='\n': 			MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]==self.cPath:  MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cEnd: 	 MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cStart: MoveValid=True; 
		else: MoveValid=False
		#debob('NewPos character "'+self.PuzzleFileHolder[NewPos]+'"'); 
		if MoveValid==True:
			#debob('valid move from '+str(CurPos)+' to '+str(NewPos))
			if self.PuzzleFileHolder_Original[CurPos]==self.cStart: 
				    self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cStart,1)
			if self.PuzzleFileHolder_Original[CurPos]==self.cEnd: 
				    self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cEnd,1)
			else: self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cPath,1)
			#if self.PuzzleFileHolder[NewPos]==self.cPath:  
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cPath,self.cUser,1)
			#elif self.PuzzleFileHolder[NewPos]==self.cEnd: 	 
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cEnd,self.cUser,1)
			#elif self.PuzzleFileHolder[NewPos]==self.cStart: 
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cStart,self.cUser,1)
			#self.PuzzleFileHolder=
			#self.PuzzleFileHolder[NewPos:1]=self.cUser
			#self.PuzzleFileHolder[NewPos]=self.cUser
			if self.PuzzleFileHolder_Original[NewPos]==self.cEnd: 
				self.VictoryDance(); 
			self.PuzzleFileHolder=self.PuzzleFileHolder[0:NewPos]+self.cUser+self.PuzzleFileHolder[NewPos+1:len(self.PuzzleFileHolder)]; 
			if (tfalse(SettingG("show-map"))==True) and (tfalse(SettingG("show-maplocation"))==True): self.PrepareMaze(self.PuzzleFileHolder); 
			self.displayVisualItems(NewPos); 
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
	def VictoryDance(self):
		try:
				debob("game won"); 
				SFX('fanfare_x'); 
				#splash.do_My_Splash(self.iDuckShot3,1); 
				splash.do_My_Splash(artj('corn-maze-exit'),10,True,(self.scr['W']-500)/2,(self.scr['H']-333)/2,500,333); 
				#splash.do_My_Splash(artj('corn-maze-exit'),2,True,10,150,self.scr['W']-200,self.scr['H']-150); 
				self.CloseWindow1st(); #DoA("Back"); 
		except: pass
	def CloseWindow1st(self):
		#try: zz=[self.CtrlList,self.RepoThumbnail,self.RepoFanart2,self.RepoFanart,self.LabCurrentRepo,self.LabTitle,self.button[0],self.TVS,self.TVSBGB,self.BGB]
		#except: zz=[]
		#for z in zz:
		#	try: self.removeControl(z); del z
		#	except: pass
		self.close()
## ################################################## ##
## ################################################## ##
## Start of program
TempWindow=MyWindow(); TempWindow.doModal(); del TempWindow
## ################################################## ##
## ################################################## ##
