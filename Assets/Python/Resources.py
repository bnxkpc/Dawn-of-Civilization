# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
#import Popup
from Consts import *
from RFCUtils import utils # edead
from StoredData import data

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

### Constants ###


# initialise bonuses variables

iRoad = 0
#Orka: Silk Road road locations
lSilkRoute = [(101,55), (102,55), (103,56), (104,56), (105,54), (105,55), (106,53), (106,55), (107,53), (107,56), (108,53), (108,56), (109,54), (109,56), (110,54), (110,56), (111,55), (111,57), (112,55), (112,58), (113,56), (113,58), (114,56), (114,57), (115,56), (116,56), (117,55), (118,54)]
lNewfoundlandCapes = [(38, 60), (39, 60), (39, 61), (38, 61), (37, 61), (37, 62), (37, 63), (37, 64), (38, 65), (38, 66), (38, 67)]

class Resources:

	# Leoreth: bonus removal alerts by edead
	def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE"):
		"""Creates a bonus resource and alerts the plot owner"""
		
		if gc.getMap().plot(iX,iY).getBonusType(-1) == -1 or iBonus == -1: # only proceed if the bonus isn't already there or if we're removing the bonus
			if iBonus == -1:
				iBonus = gc.getMap().plot(iX,iY).getBonusType(-1) # for alert
				gc.getMap().plot(iX,iY).setBonusType(-1)
				
				iImprovement = gc.getMap().plot(iX, iY).getImprovementType()
				if iImprovement >= 0:
					if gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(iBonus):
						gc.getMap().plot(iX, iY).setImprovementType(-1)
			else:
				gc.getMap().plot(iX,iY).setBonusType(iBonus)
				
			iOwner = gc.getMap().plot(iX,iY).getOwner()
			if iOwner >= 0 and textKey != -1: # only show alert to the tile owner
				# Leoreth: changed so different area cities are found if water resource is added (because sea is automatically a different area than land)
				bWater = gc.getMap().plot(iX, iY).isWater()
				city = gc.getMap().findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, not bWater, bWater, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				if not city.isNone():
					if gc.getBonusInfo(iBonus).getTechReveal() == -1 or gc.getTeam(city.getTeam()).isHasTech(gc.getBonusInfo(iBonus).getTechReveal()):
						szText = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName()))
						CyInterface().addMessage(iOwner, False, iDuration, szText, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), ColorTypes(iWhite), iX, iY, True, True)


	def removeResource(self, iX, iY, textKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
		"""Removes a bonus resource and alerts the plot owner"""
		if gc.getMap().plot(iX, iY).getBonusType(-1) == -1: return
		self.createResource(iX, iY, -1, textKey)
       	
	def checkTurn(self, iGameTurn):
		
		# Gujarati horses appear later so Harappa cannot benefit too early
		if iGameTurn == getTurnForYear(-1000):
			self.createResource(102, 43, iHorse)
			
		# Assyrian copper appears later to prevent Babylonia from building too strong a defensive military
		if iGameTurn == getTurnForYear(-800):
			self.createResource(89, 51, iCopper)
			
		# Tamils, 300 BC
		elif iGameTurn == getTurnForYear(tBirth[iTamils])-1 and data.isPlayerEnabled(iTamils):
			self.createResource(108, 34, iFish)

		#Orka: Silk Road
		elif iGameTurn == getTurnForYear(-200): 
			for i in range( len(lSilkRoute) ):
				gc.getMap().plot(lSilkRoute[i][0], lSilkRoute[i][1]).setRouteType(iRoad)
		
		#Orka: Silk Road
		elif iGameTurn == getTurnForYear(-100):
			gc.getMap().plot(104, 56).setPlotType(PlotTypes.PLOT_HILLS, True, True)
			gc.getMap().plot(104, 56).setRouteType(iRoad)
			self.createResource(104, 56, iCamel)
			
			self.createResource(103, 55, iSilk)
			self.createResource(101, 53, iSilk)

		#Leoreth: Hanseong's pig appears later so China isn't that eager to found Sanshan
		elif iGameTurn == getTurnForYear(-50):
			self.createResource(130, 55, iPig)

		# Leoreth: remove floodplains in Sudan and ivory in Morocco and Tunisia
		elif iGameTurn == getTurnForYear(550):
			#gc.getMap().plot(79, 37).setFeatureType(-1, 0)
			#gc.getMap().plot(79, 38).setFeatureType(-1, 0)
			
			self.removeResource(58, 44)
			self.removeResource(66, 46)
			
		# Leoreth: prepare Tibet, 630 AD
		elif iGameTurn == getTurnForYear(tBirth[iTibet])-1 and data.isPlayerEnabled(iTibet):
			self.createResource(114, 49, iWheat)
			self.createResource(112, 49, iHorse)
			
		# Leoreth: obstacles for colonization
		elif iGameTurn == getTurnForYear(700):
			gc.getMap().plot(38, 64).setFeatureType(iMud, 0)
			for x, y in lNewfoundlandCapes:
				gc.getMap().plot(x, y).setFeatureType(iCape, 0)
				
			if utils.getHumanID() == iVikings:
				gc.getMap().plot(45, 72).setFeatureType(-1, 0)
		
		# Leoreth: New Guinea can be settled
		# elif iGameTurn == getTurnForYear(1000):
		#	gc.getMap().plot(113, 25).setFeatureType(-1, 0)
		
		# Leoreth: for respawned Egypt
		elif iGameTurn == getTurnForYear(900):
			self.removeResource(81, 42)
			self.createResource(81, 42, iIron)
		    
		elif iGameTurn == getTurnForYear(1100):
			#gc.getMap().plot(71, 30).setBonusType(iSugar) #Egypt
			
			self.createResource(83, 26, iSugar) # East Africa # (84, 28)
			self.createResource(81, 19, iSugar) # Zimbabwe
			self.createResource(77, 13, iSugar) # South Africa
			
			self.createResource(72, 25, iBanana) # Central Africa
			self.createResource(77, 26, iBanana) # Central Africa
			
			if data.isPlayerEnabled(iCongo):
				self.createResource(70, 27, iCotton) # Congo
				self.createResource(71, 23, iIvory) # Congo
				self.createResource(69, 28, iIvory) # Cameroon
			
			self.createResource(66, 56, iWine) # Savoy
			self.createResource(66, 55, iClam) # Savoy
			
			self.createResource(55, 52, iIron) # Portugal
			
			#self.removeResource(87, 49) # Orduqent # Leoreth: to do new map
			#self.removeResource(89, 51) # Orduqent # Leoreth: to do new map
			
		# Leoreth: route to connect Karakorum to Beijing and help the Mongol attackers
		elif iGameTurn == getTurnForYear(tBirth[iMongolia]):
			for tPlot in [(119, 61), (120, 60), (121, 59), (122, 58), (122, 57), (123, 57)]:
				x, y = tPlot
				gc.getMap().plot(x, y).setRouteType(iRoad)
				
			# silk near Astrakhan
			self.createResource(91, 60, iSilk)

		if iGameTurn == getTurnForYear(1250):
			#gc.getMap().plot(57, 52).setBonusType(iWheat) #Amsterdam
			self.createResource(113, 41, iFish) # Calcutta, Dhaka, Pagan
			
			gc.getMap().plot(62, 64).setFeatureType(-1, 0)
			gc.getMap().plot(63, 65).setFeatureType(-1, 0)
			gc.getMap().plot(64, 65).setFeatureType(-1, 0)

		#elif iGameTurn == getTurnForYear(1350):
			#gc.getMap().plot(102, 35).setFeatureType(-1, 0) #remove rainforest in Vietnam

		elif iGameTurn == getTurnForYear(1500):
			gc.getMap().plot(38, 64).setFeatureType(-1, 0) # remove Marsh in case it had been placed
			for x, y in lNewfoundlandCapes:
				gc.getMap().plot(x, y).setFeatureType(-1, 0)
				
			# also remove Marsh on Port Moresby
			gc.getMap().plot(116, 24).setFeatureType(-1, 0)
			
			#self.createResource(56, 54, iFish) # Amsterdam
			#self.createResource(57, 52, iWheat) # Amsterdam
			#self.createResource(58, 52, iCow) # Amsterdam
			
		elif (iGameTurn == getTurnForYear(1600)):
			self.createResource(30, 61, iCow) # Montreal
			self.createResource(15, 62, iCow) # Alberta
			self.createResource(10, 62, iCow) # British Columbia
			self.createResource(29, 53, iCow) # Washington area
			self.createResource(32, 59, iCow) # Boston area
			#self.createResource(25, 49, iCow) # Lakes
			self.createResource(21, 49, iCow) # New Orleans area
			self.createResource(29, 57, iCow) # New York area
			self.createResource(16, 54, iCow) # Colorado
			self.createResource(17, 51, iCow) # Texas
			self.createResource(39, 12, iCow) # Argentina
			self.createResource(36, 9, iCow) # Pampas
			self.createResource(46, 29, iCow) # Brazil
			
			self.createResource(25, 51, iCotton) # near Florida
			self.createResource(23, 50, iCotton) # Louisiana
			self.createResource(21, 52, iCotton) # Louisiana
			self.createResource(10, 51, iCotton) # California
			
			self.createResource(25, 57, iPig) # Lakes
			self.createResource(24, 52, iPig) # Atlanta area
			
			self.createResource(13, 63, iSheep) # Alberta
			self.createResource(17, 58, iSheep) # Midwest
			self.createResource(36, 13, iSheep) # Argentina
			
			#self.createResource(21, 50, iWheat) # Canadian border
			self.createResource(17, 54, iWheat) # Midwest
			self.createResource(19, 63, iWheat) # Manitoba
			
			self.createResource(23, 39, iBanana) # Guatemala
			self.createResource(29, 35, iBanana) # Colombia
			self.createResource(42, 31, iBanana) # Brazil
			self.createResource(49, 29, iBanana) # Brazil
			
			self.createResource(54, 52, iCorn) # Galicia
			self.createResource(60, 56, iCorn) # France
			self.createResource(73, 58, iCorn) # Hungary
			self.createResource(77, 57, iCorn) # Romania
			self.createResource(129, 59, iCorn) # Manchuria
			self.createResource(125, 56, iCorn) # Beijing
			#self.createResource(77, 52, iCorn) # Caricyn
			
			self.createResource(64, 64, iPotato) # Amsterdam
			self.createResource(57, 64, iPotato) # England
			
			self.createResource(108, 39, iSpices) # Deccan
			gc.getMap().plot(108, 39).setFeatureType(iRainforest, 0)
			
			# remove floodplains in Transoxania
			for tuple in [(97, 55), (96, 56)]:
				x, y = tuple
				gc.getMap().plot(x, y).setFeatureType(-1, 0)

		elif iGameTurn == getTurnForYear(1700):
			self.createResource(15, 63, iHorse) # Alberta
			self.createResource(28, 54, iHorse) # Washington area
			self.createResource(17, 59, iHorse) # Midwest
			self.createResource(20, 56, iHorse) # Midwest
			self.createResource(17, 52, iHorse) # Texas
			self.createResource(45, 30, iHorse) # Brazil
			self.createResource(38, 12, iHorse) # Buenos Aires area
			self.createResource(35, 10, iHorse) # Pampas
			self.createResource(30, 30, iHorse) # Venezuela
			
			self.createResource(28, 42, iSugar) # Caribbean
			self.createResource(37, 41, iSugar) # Caribbean
			self.createResource(39, 34, iSugar) # Guayana
			self.createResource(44, 30, iSugar) # Brazil
			self.createResource(42, 23, iSugar) # inner Brazil
			self.createResource(31, 43, iSugar) # Hispaniola
			
			self.createResource(43, 19, iCoffee) # Brazil
			self.createResource(44, 23, iCoffee) # Brazil
			self.createResource(43, 26, iCoffee) # Brazil
			self.createResource(29, 31, iCoffee) # Colombia
			self.createResource(28, 34, iCoffee) # Colombia
			self.createResource(34, 36, iCoffee) # Colombia
			self.createResource(119, 28, iCoffee) # Sumatra
			self.createResource(25, 45, iCoffee) # Cuba
			
			self.createResource(32, 43, iCocoa) # Hispaniola
			self.createResource(124, 25, iCocoa) # Java
			self.createResource(129, 27, iCocoa) # Clebes
			self.createResource(46, 29, iCocoa) # Brazil
			
			self.createResource(79, 56, iTobacco) # Turkey
			
			self.createResource(44, 19, iFish) # Brazil
			self.createResource(31, 14, iFish) # Chile
			self.createResource(129, 51, iFish) # Shanghai
			
			# self.createResource(70, 59, iDeer) # St Petersburg
			
			self.createResource(67, 64, iPotato) # Germany
			self.createResource(70, 63, iPotato) # Germany
			self.createResource(93, 62, iPotato) # Caricyn
			self.createResource(123, 48, iPotato) # China
			self.createResource(127, 51, iPotato) # China
			self.createResource(130, 60, iPotato) # Manchuria
			self.createResource(105, 45, iPotato) # India
			self.createResource(113, 44, iPotato) # Bangladesh
			
			# remove marshes for St. Petersburg
			gc.getMap().plot(81, 70).setFeatureType(-1, 0)
			gc.getMap().plot(80, 69).setFeatureType(-1, 0)
			
		elif iGameTurn == getTurnForYear(1800):
			if gc.getDefineINT("PLAYER_REBIRTH_MEXICO") != 0:
				self.createResource(16, 47, iHorse) # Mexico
				self.createResource(14, 45, iIron) # Mexico
				self.createResource(16, 44, iCow) # Mexico
				
			if gc.getDefineINT("PLAYER_REBIRTH_COLOMBIA") != 0:
				self.createResource(30, 36, iIron) # Colombia
			
			if data.isPlayerEnabled(iArgentina):
				self.createResource(35, 14, iWine) # Mendoza, Argentina
				self.createResource(35, 7, iSheep) # Pampas, Argentina
				self.createResource(35, 15, iIron) # Argentina
			
			if data.isPlayerEnabled(iBrazil):
				self.createResource(43, 19, iCorn) # Sao Paulo
				self.createResource(47, 23, iCow) # Rio de Janeiro
				self.createResource(42, 25, iBanana) # Brasilia

		elif iGameTurn == getTurnForYear(1850):
			self.createResource(8, 52, iWine) # California
			self.createResource(35, 10, iWine) # Andes
			self.createResource(137, 11, iWine) # Barossa Valley, Australia
			
			self.createResource(138, 10, iSheep) # Australia
			self.createResource(140, 14, iSheep) # Australia
			self.createResource(146, 6, iSheep) # New Zealand
			
			# self.createResource(58, 47, iRice) # Vercelli
			self.createResource(8, 56, iRice) # California
			
			self.createResource(9, 50, iFish) # California
			self.createResource(102, 37, iFish) # Bombay
			
			self.createResource(137, 62, iCow) # Hokkaido
			
			self.createResource(0, 43, iSugar) # Hawaii
			self.createResource(2, 42, iBanana) # Hawaii
			
			self.createResource(10, 59, iPotato) # Seattle
			
			self.createResource(58, 32, iCocoa) # West Africa
			self.createResource(61, 31, iCocoa) # West Africa
			self.createResource(67, 31, iCocoa) # West Africa
			
			# flood plains in California
			for tPlot in [(9, 52), (9, 53), (8, 54), (9, 55)]:
				x, y = tPlot
				gc.getMap().plot(x,y).setFeatureType(iFloodPlains, 0)