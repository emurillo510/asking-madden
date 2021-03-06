#!/usr/bin/python
import sys
import glob
import errno
from bs4 import BeautifulSoup

path = 'target/nfl-teams-*.html'
files = glob.glob(path)
for file in files:
	doc  = BeautifulSoup(open(file), "html.parser")

	file_output_name = file + ".csv"
	file_output = open(file_output_name, "w")

	

	#print file
	nfl_header = doc.select("tr.thd1 td")
	nfl_afc_conference = doc.select("tr.thd2 > td")
	nfl_afc_conference_header = doc.select("tr.thd2 td a")
	nfl_teams = doc.select("tr.tbdy1 td a")
	nfl_teams_stats = doc.select("tr.tbdy1 td")
	nfl_teams_links = doc.select("tr.tbdy1 td a")
	nfl_nfc_header = doc.select("tr.thd1.NFCcolors td")

	if nfl_header:


		# print AFC and NFC conference
		'''
		for i in nfl_header:
			print i.string.strip()
		'''

	
		nfl_divisions = []
		# get NFL conferences
		for child in nfl_afc_conference:
			if child.string:
				nfl_divisions.append(str(child.string))
		#print nfl_divisions
		

		stats_header = []
		# get statistics header
		for i in range(0,17):
			stats_header.append(nfl_afc_conference_header[i].string)

		stats_header.insert(0,"Team")
		stats_header.insert(1,"Season")
		stats_header.insert(2,"Division")
		stats_header =  ','.join(stats_header)

		print stats_header
		file_output.write(stats_header)
		file_output.write("\n")

		# get nfl teams
		#for child in nfl_teams:
		#	if child.string:
		#		print child.string.strip()

		team_row = []
		# get nfl teams stats
		'''
		for i in nfl_teams_stats:
			if i.string:
				team_row.append(str(i.string))
			else:
				team_name = i.find('a')
				team_row.append(str(i.string))
		'''
		team_row = []
		for i,j in enumerate(nfl_teams_stats):

			if j.string:
				team_row.append(str(j.string))
			else:
				team_name = j.find('a').string.strip()
				team_row.append(str(team_name))

		team_row_str = ""
		div_counter = 0
		record_row = 288
		for i,j in enumerate(team_row):
			if (i%(18*4) == 0 and i > 0):
				div_counter = div_counter + 1

			if (i%18 == 0 and i > 0):
				team_row_str = team_row_str[:-1]
				if (i < record_row):
					team_row_str += "\n" + j + "," + nfl_header[0].string.strip() +  "," + nfl_divisions[div_counter] + ","
				else:
					team_row_str += "\n" + j + "," +  nfl_header[1].string.strip() + "," + nfl_divisions[div_counter] + ","
			else:
				if(i==0):
					team_row_str += j + "," + nfl_header[0].string.strip() + "," + nfl_divisions[div_counter] + ","
				else:
					team_row_str += j +","
		
			if (i==len(team_row)-1):
				team_row_str = team_row_str[:-1]
		print team_row_str
		file_output.write(team_row_str)
		file_output.write("\n")

		file_output.close()

		#print ",".join(team_row)

		# get nfl team sites
		#base_url="http://www.nfl.com/"

		#for child in nfl_teams_links:
		#	print base_url+child["href"]
	else:
		print "no stats on this file..."
