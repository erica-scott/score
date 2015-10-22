import urllib.request
import urllib.parse
import re
import time
import sys
from datetime import datetime, timedelta

today = time.strftime("%A %B %d, %Y")
time_now = time.strftime("%I:%M %p")

day = time.strftime("\%d")
month = time.strftime("%m")
year = time.strftime("%Y")

cities = {"ANA":"Anaheim", "ARI":"Arizona", "BOS":"Boston", "BUF":"Buffalo", "CGY":"Calgary", "CAR":"Carolina", "CHI":"Chicago", "COL":"Colorado", 
			 "CBJ":"Columbus", "DAL":"Dallas", "DET":"Detroit", "EDM":"Edmonton", "FLA":"Florida", "LAK":"Los Angeles", "MIN":"Minnesota", "MON":"Montreal",
			 "NSH":"Nashville", "NJD":"New Jersey", "NYI":"NY Islanders", "NYR":"NY Rangers", "OTT":"Ottawa", "PHI":"Philadelphia", "PIT":"Pittsburgh",
			 "SJS":"San Jose", "STL":"St. Louis", "TBL":"Tampa Bay", "TOR":"Toronto", "VAN":"Vancouver", "WSH":"Washington", "WPG":"Winnipeg"}

team_apps = {"ANA":"Anaheim Ducks", "ARI":"Arizona Coyotes", "BOS":"Boston Bruins", "BUF":"Buffalo Sabres", "CGY":"Calgary Flames", "CAR":"Carolina Hurricanes", "CHI":"Chicago Blackhawks", "COL":"Colorado Avalanche", 
			 "CBJ":"Columbus Blue Jackets", "DAL":"Dallas Stars", "DET":"Detroit Red Wings", "EDM":"Edmonton Oilers", "FLA":"Florida Panthers", "LAK":"Los Angeles Kings", "MIN":"Minnesota Wild", "MON":"Montreal Canadiens",
			 "NSH":"Nashville Predators", "NJD":"New Jersey Devils", "NYI":"New York Islanders", "NYR":"New York Rangers", "OTT":"Ottawa Senators", "PHI":"Philadelphia Flyers", "PIT":"Pittsburgh Penguins",
			 "SJS":"San Jose Sharks", "STL":"St. Louis Blues", "TBL":"Tampa Bay Lightning", "TOR":"Toronto Maple Leafs", "VAN":"Vancouver Canucks", "WSH":"Washington Capitals", "WPG":"Winnipeg Jets"}
for key, value in team_apps.items():
	print(key + " : " + value)

print("Please enter the abbreviation of the team you are cheering for from the list above:") 
focus_team = sys.stdin.readline()
focus_team = focus_team.strip()

print("")

flag = 0
for key, value in team_apps.items():
	if key == focus_team:
		flag = 1

if flag == 1:
	my_team = team_apps[focus_team]
	
	my_timezone = time.strftime("%Z")
	
	timezone_conversions = {"Pacific Daylight Time":-3, "Mountain Time":-2}
	timezone_change = timezone_conversions[my_timezone]
	
	url = 'http://www.nhl.com/ice/schedulebyday.htm?date=' + month + '\%2F' + day + '\%2F' + year + '&team=' + focus_team
	values = {'s':'basics','submit':'search'}
	data = urllib.parse.urlencode(values)
	data = data.encode('utf-8')
	req = urllib.request.Request(url, data)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	
	date = re.findall(r'<div class="contentBlock"><h3>(.*?)\\n',str(respData))
	
	for eachDate in date:
		eachDate = eachDate.strip()
		if eachDate != "":
			date = eachDate
			
	teams = re.findall(r'teamName(.*?)</div>',str(respData))
	
	for eachT in teams:
		temp = re.findall(r'rel="(.*?)" shape="rect"',str(eachT))
		for eachTeam in temp:
			if eachTeam != focus_team:
				other_team = eachTeam
			
	times = re.findall(r'skedStartTimeEST(.*?)</div>',str(respData))
	
	for eachT in times:
		et_time = re.findall(r'>(.*?)ET', str(eachT))
		for eachTime in et_time:
			if eachTime != "":
				time = eachTime
				if(time[1:2] == "0"):
					hour = time[:2]
					hour = '0' + hour
					int_hour = int(hour) + timezone_change
					int_end_hour = int_hour + 3
					hour = str(int_hour)
					end_hour = str(int_end_hour)
					minute = time[3:5]
					am_pm = time[5:]
					correct_time = hour + ':' + minute + " " + am_pm
					end_time = end_hour + ':' + minute + " " + am_pm
				else:
					hour = time[:1]
					hour = '0' + hour
					int_hour = int(hour) + timezone_change
					int_end_hour = int_hour + 3
					hour = str(int_hour)
					end_hour = str(int_end_hour)
					minute = time[2:4]
					am_pm = time[5:]
					correct_time = hour + ':' + minute + " " + am_pm
					end_time = end_hour + ':' + minute + " " + am_pm
				
	
	url = 'http://www.nhl.com/ice/scores.htm?navid=nav-scr-gc#'
	values = {'s':'basics','submit':'search'}
	data = urllib.parse.urlencode(values)
	data = data.encode('utf-8')
	req = urllib.request.Request(url, data)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	
	scores_1 = re.findall(r'sbGame(.*?)</table>',str(respData))
	
	total_score_list = []
	current_game_teams = []
	
	for eachS in scores_1:
		scores_2 = re.findall(r'team left(.*?)</tr>',str(eachS))
		for eachGame in scores_2:
			details = re.findall(r';">(.*?)</a>',str(eachGame))
			for eachDetail in details:
				if eachDetail != "" and eachDetail == cities[focus_team] or eachDetail == cities[other_team]:
					current_game_teams.append(eachDetail)
					total_score = re.findall(r'total">(.*?)</td>',str(eachGame))
					for eachTotalScore in total_score:
						total_score_list.append(eachTotalScore)
					
	print("Next Game: " + date + " at " + correct_time)
	print(my_team + " vs " + team_apps[other_team])
	
	game_on = 0
	if today == date:
		print("Game Day!")
		hour_now = time_now[:2]
		min_now = time_now[3:5]
		hour_begin = correct_time[:1]
		min_begin = correct_time[2:4]
		hour_end = end_time[:1]
		min_end = end_time[2:4]
		if ( ( ( int(hour_now) >= int(hour_begin) ) and ( int(min_now) >= int(min_begin) ) ) and ( ( int(hour_now) < int(hour_end) ) and ( int(min_now) < int(min_end) ) ) ) :
			game_on = 1
			print("Game has started!")
	
	i = 0
	for test_team in current_game_teams:
		if ((game_on == 1) and (test_team == cities[focus_team] or test_team == cities[other_team])):
			i = i + 1
	
	if i == 2:
		print(current_game_teams[0] + " - " + total_score_list[0])
		print(current_game_teams[1] + " - " + total_score_list[1])
else:
	print("You have entered a team that doesn't exist.")


	
