import os
import sys
import csv
import shutil
import datetime

# get today's date
todayDate = datetime.datetime.today().strftime('%Y%m%d')

# variables to replace in the template file
# order matters
findList = ['$cityName', '$stateName', '$channelProvider', '$channelAccountId', '$profileName', '$profileId', '$campaignBudget', '$desktopExactBid', '$desktopBroadBid', '$mobileExactBid', '$mobileBroadBid', '$cityCampaignName', '$landingPage', '$channelUrl']

# choose base file
# TODO: open file selection vs. typing in filename
print 'Type the base csv file name:'
baseFile = raw_input()
baseFile = os.getcwd() + '/base/' + baseFile + '.csv'
print 'Your input file is: ' + baseFile

# choose template file
print 'Type the template file to use:'
tempFile = raw_input()
tempFile = os.getcwd() + '/template/' + tempFile + '.csv'
print 'Your template file is: ' + tempFile

# choose landing page type
print 'What should the LP be? (City, Quiz, Homepage)'
landingPageType = raw_input()

with open(baseFile, 'r') as inputData:
	inputData = csv.reader(inputData, delimiter=',')
	for count, column in enumerate(inputData):
		# skip header row
		if count > 0:

			# remove '.' from cityName and create cityCampaignName and channelUrl fields
			# TODO: trim city / state (prevent spaces)
			column[0] = column[0].replace('.','')
			cityCampaignName = column[0].replace(' ', '_')
			cityUrl = column[0].lower()
			cityUrl = cityUrl.replace(' ', '-')
			channelUrl = column[2].lower()

			# create finalUrl field
			if landingPageType == 'City':
				finalUrl = 'https://www.apartmentlist.com/' + column[1].lower() + '/' + cityUrl
			elif landingPageType == 'Quiz':
				finalUrl = 'https://www.apartmentlist.com/quiz'
			elif landingPageType == 'Homepage':
				finalUrl = 'https://www.apartmentlist.com'
			else:
				print "Landing page error"
				sys.exit()

			# add cityCampaignName and finalUrl to list
			column.append(cityCampaignName)
			column.append(finalUrl)
			column.append(channelUrl)

			# create new directory (by day)
			outputPath = os.getcwd() + '/output/' + todayDate
			if not os.path.exists(outputPath):
				os.makedirs(outputPath)
			# create separate files for each cityName
			newFile = outputPath + '/' + todayDate + '_geoExp_' + cityUrl + '_' + column[1].lower() + '.csv'
			templateFile = open(tempFile, 'r')
			outputFile = open(newFile, 'w')
			changes = templateFile.read()
			print 'Changing the following:'
			for item, replacement in zip(findList, column):
				print 'Item: ' + item
				print 'Replacement: ' + replacement + '\n'
				changes = changes.replace(item, replacement)
			outputFile.write(changes)
			outputFile.close()

print 'Job done - ' + str(count) + ' files created'



# alternative 1 - work with xlsx file instead of csv
# alternative 2 - store all content in file as an array and iterate (allows check for exceeded char / variable that didn't change / etc)
