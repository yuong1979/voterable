from django.shortcuts import render

# Create your views here.
from tags.models import TagPoll, runtagcount
from polls.models import Ptype, PollItem
from django.conf import settings

from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task, task, app

import json
import re
import urllib.request
# from pytube import YouTube
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect






def AnalyseTags(request):
	taglist = TagPoll.objects.filter(active=True)
	polllist = Ptype.objects.filter(active=True).order_by('-date')

	context = {
				'polls': polllist, 
				'tags': taglist, 
				}
				
	return render(request, 'analysetags.html', context)


def AnalysePvote(request):
	# only filtered for the top 50 lowest score so that it will not take a long time to load
	tiplist = PollItem.objects.filter(allowed=True).order_by('score')[:50]
	
	context = {
				'tiplists': tiplist,
				}
				
	return render(request, 'analysepvote.html', context)





            # async_contact_mail.delay(
            #     subject=subject,
            #     contact_message=contact_message,
            #     from_email=from_email,
            #     to_email=to_email
            #     )







def AnalyseVid(request):
	# polllist = Ptype.objects.filter(active=True)

	pitems = PollItem.objects.filter(published=False)

	context = {
				'pitems': pitems,
				}

	print (request.user)

	print (dir(request.user))

	print (request.user.is_staff)

				
	return render(request, 'analysevid.html', context)







def ProcessAnalytics(request):

	if request.user.is_staff == True:
		async_vid_analytics.delay()

	return redirect("Home")



# for detecting dead videos
@task()
def async_vid_analytics():

	#change all the published to postive first
	posiall = PollItem.objects.filter()

	for i in posiall:
		i.published = True
		i.save()


	tiplist = PollItem.objects.filter(allowed=True)

	api_key = settings.YOUTUBE_SECRET
	p_id = []

	for i in tiplist:

		testvid = i.description

		try:
			start = testvid.index("youtube.com/embed")
			end = (testvid[start:].index('"'))
			end = start + end
			youtubefull = testvid[start:end]

			try:
				vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
				#remove the last question mark
				vidid = vidid[:-1]

			except AttributeError:

				vidid = re.findall('(?<=embed/).*$', youtubefull)
				#remove the item from the list
				vidid = vidid[0]

			video_id = vidid

			url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

			json_url = urllib.request.urlopen(url)
			data = json.loads(json_url.read())

			vidactive = data.get('pageInfo')['totalResults']

			if vidactive == 0:
				print (video_id + " video is no longer existing - record result")
				p_id.append(i.id)

		except ValueError:
			pass
			# print ("video does not exist - no issues skip")


		notvalidvid = PollItem.objects.filter(allowed=True, id__in=p_id)


	#change all the published to postive first
	FailVid = PollItem.objects.filter(id__in=p_id)

	for i in FailVid:
		i.published = False
		i.save()




















# # for detecting dead videos
# def AnalyseVid(request):
# 	# polllist = Ptype.objects.filter(active=True)
# 	tiplist = PollItem.objects.filter(allowed=True)

# 	api_key = settings.YOUTUBE_SECRET

# 	p_id = []

# 	for i in tiplist:

# 		testvid = i.description

# 		try:
# 			start = testvid.index("youtube.com/embed")
# 			end = (testvid[start:].index('"'))
# 			end = start + end
# 			youtubefull = testvid[start:end]

# 			try:
# 				vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
# 				#remove the last question mark
# 				vidid = vidid[:-1]

# 			except AttributeError:

# 				vidid = re.findall('(?<=embed/).*$', youtubefull)
# 				#remove the item from the list
# 				vidid = vidid[0]

# 			video_id = vidid

# 			url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

# 			json_url = urllib.request.urlopen(url)
# 			data = json.loads(json_url.read())

# 			vidactive = data.get('pageInfo')['totalResults']

# 			if vidactive == 0:
# 				print (video_id + " video is no longer existing - record result")
# 				p_id.append(i.id)

# 			# try:
# 			# 	print (data.get('pageInfo')['totalResults'])
# 			# 	print (data.get('items')[0]['snippet']['thumbnails']['default']['url'])
# 			# 	print (data.get('items')[0]['snippet']['channelTitle'])
# 			# 	print (data.get('items')[0]['snippet']['title'])

# 			# except IndexError:
# 			# 	print ("video is no longer existing - record result")
# 			# 	p_id.append(i.id)


# 		except ValueError:
# 			pass
# 			# print ("video does not exist - no issues skip")


# 		notvalidvid = PollItem.objects.filter(allowed=True, id__in=p_id)


# 	pitem = PollItem.objects.filter(id__in=p_id)

# 	context = {
# 				'pitems': notvalidvid,
# 				# 'data': data,
# 				# 'vid' : vid,
# 				}
				
# 	return render(request, 'analysevid.html', context)










#analyze vid backup





# def AnalyseVid(request):
# 	polllist = Ptype.objects.filter(active=True)
# 	tiplist = PollItem.objects.filter(allowed=True)

# 	api_key = settings.YOUTUBE_SECRET

# 	# 15 - video is private
# 	# 34 - video is unavailable
# 	# 36 - video does not exist
# 	# 18 - works from the middle
# 	# 21 - works from the start

# 	poll = PollItem.objects.filter(allowed=True, id=18).first()

# 	testvid = poll.description

# 	try:
# 		start = testvid.index("youtube.com/embed")
# 		end = (testvid[start:].index('"'))
# 		end = start + end
# 		youtubefull = testvid[start:end]

# 		try:
# 			vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
# 			#remove the last question mark
# 			vidid = vidid[:-1]

# 		except AttributeError:

# 			vidid = re.findall('(?<=embed/).*$', youtubefull)
# 			#remove the item from the list
# 			vidid = vidid[0]

# 		video_id = vidid

# 		url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

# 		json_url = urllib.request.urlopen(url)
# 		data = json.loads(json_url.read())

# 		try:
# 			print (data.get('pageInfo')['totalResults'])

# 		except IndexError:
# 			print ("video is no longer existing")
# 			print (data.get('items')[0]['snippet']['thumbnails']['default']['url'])
# 			print (data.get('items')[0]['snippet']['channelTitle'])
# 			print (data.get('items')[0]['snippet']['title'])

# 	except ValueError:
# 		print ("video does not exist")



# 	vid = []	
# 	p_id = []

# 	# for detecting dead videos
# 	for i in tiplist:
# 		tipviddes = i.description
# 		y = tipviddes.find("youtube.com/embed")

# 		#if youtube is detected then search for the videos
# 		if y != -1:
# 			vidfound = tipviddes[y:]
# 			x = vidfound.find('"')

# 			x = y + x
# 			# print (tipviddes[y:x])

# 			# if the vid is no longer working - then append
# 			p_id.append(i.id)

# 			# ptype.append(i.polltype)
# 			# tip.append(i)
# 			vid.append(tipviddes[y:x])




# 	pitem = PollItem.objects.filter(id__in=p_id)

# 	context = {
# 				'pitems': pitem,
# 				'data': data,
# 				'vid' : vid,
# 				}
				
# 	return render(request, 'analysevid.html', context)

