from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from evaluate.models import User
from evaluate.models import Results
import psycopg2
import random
import time
import datetime
import os, re

def index(request):
  request.session['user_id'] = -1
  request.session['user_name'] = ""
  
  return render(request, 'evaluate/index.html')

def confirm(request):
  tmp_user_name = request.POST['user_name']
  request.session['user_name'] = tmp_user_name

  if tmp_user_name is "":
    error_message = "ユーザ名を入力してください．"
    return render(request, 'evaluate/index.html', {'error_message': error_message})

  if User.objects.filter(user_name=tmp_user_name).exists():
    succeed_user = User.objects.get(user_name=tmp_user_name)
    request.session['user_id'] = succeed_user.id
    
    total_images = len(Results.objects.filter(user_id=succeed_user.id).values())
    marked_images = len(Results.objects.filter(user_id=succeed_user.id).exclude(lda_score=-1).values())
    if marked_images == total_images:
      return render(request, 'evaluate/end.html', {'user_name': tmp_user_name})
    
    finished_rate = "{0}/{1}".format(marked_images, total_images)
    
    return render(request, 'evaluate/confirm.html', {'succeed_user_name': tmp_user_name, 'finished_rate': finished_rate})

  return render(request, 'evaluate/confirm.html', {'new_user_name': tmp_user_name})


def register(request):
  tmp_user_name = request.session['user_name']
  new_user = User(user_name=tmp_user_name)
  new_user.save()

  user_id = new_user.id
  request.session['user_id'] = user_id

  con = psycopg2.connect("dbname=image_tagging host=localhost user=postgres")
  cursor = con.cursor()

  #cursor.execute("select tweet_id, lda_tag, raw_tag from evaluate_chosen_tags")
  #results = cursor.fetchall()
  
  cursor.execute("select tweet_id from evaluate_chosen_tweet")
  results = cursor.fetchall()
  
  for each_res in results:
    chosen_tweet_id = each_res[0]
    
    cursor.execute("""insert into evaluate_results (user_id, tweet_id, 
    bingo, bad) values (%s, %s, %s, %s)""", (user_id, chosen_tweet_id, -1, -1))
    con.commit()

  cursor.close()
  con.close()

  return HttpResponseRedirect(reverse('evaluate:display'))


def display(request):
  user_id = request.session['user_id']
  user_name = request.session['user_name']
  
  random.seed(datetime.datetime.now())
  
  total_images = len(Results.objects.filter(user_id=user_id).values())
  marked_images = len(Results.objects.filter(user_id=user_id).exclude(lda_score=-1).values())
  finished_rate = "{0}/{1}".format(marked_images+1, total_images)
  
  if marked_images == total_images:
    return render(request, 'evaluate/end.html', {'user_name': user_name})
  
  random_choice = random.randint(0,1)
  request.session['random_choice'] = random_choice
  
  #user_info = Results.objects.filter(user_id=user_id, lda_score=-1).order_by('tweet_id').values('tweet_id')[0]
  user_info = Results.objects.filter(user_id=user_id, bingo=-1).order_by('tweet_id').values('tweet_id')[0]
  
  request.session['tweet_id'] = user_info['tweet_id']
  
  con = psycopg2.connect("dbname=image_tagging host=localhost user=postgres")
  concur = con.cursor()

  concur.execute("""select distinct on (b.tweet_id) b.id, b.tweet, b.image 
    from evaluate_results as a, twipple as b
    where a.tweet_id=b.tweet_id and a.tweet_id=%s""", (user_info['tweet_id'],))

  tmp_info = concur.fetchone()

  tmp_image_id = tmp_info[0]
  tmp_tweet = tmp_info[1]
  tmp_image_data = tmp_info[2]

  #target_image_tag = Results.objects.get(user_id=user_id, tweet_id=user_info['tweet_id'])
  #lda_tag = target_image_tag.lda_tag
  #raw_tag = target_image_tag.raw_tag
  
  target_image_tag = Exp_lda.objects.filter(tweet_id=user_info['tweet_id']).values('tag')
  tag_str = ""
  for i in range(len(target_image_tag)):
    tag_str += target_image_tag[i]
    
    if i != len(target_image_tag)-1:
      tag_str += "，"

  file_path = "evaluate/static/evaluate/images/{0}.jpg".format(tmp_image_id)
  if not os.path.isfile(file_path):
    f = open(file_path, 'bw')
    f.write(tmp_image_data)
    f.close()
  
  static_image_path = "{0}.jpg".format(tmp_image_id)
  
  template_dic = {'image_name': static_image_path, 'tweet': tmp_tweet, 'tag_str': tag_str, 'finished_rate': finished_rate, 'user_name': user_name}
  
  return render(request, 'evaluate/display.html', template_dic)


def update(request):
  random_choice = int(request.session['random_choice'])
  
  user_id = request.session['user_id']
  tweet_id = request.session['tweet_id']
  
  #lda_score = 0
  #raw_score = 0
  #if random_choice:
  #  lda_score = int(request.POST['A'])
  #  raw_score = int(request.POST['B'])
  #else:
  #  lda_score = int(request.POST['B'])
  #  raw_score = int(request.POST['A'])
  
  each_result = Results.objects.get(user_id=user_id, tweet_id=tweet_id)
  #each_result.lda_score = lda_score
  #each_result.raw_score = raw_score
  
  #if lda_score == raw_score:
  #  which = request.POST['which']
  #  
  #  if which == 'A':
  #    each_result.which = 1 if random_choice else 0
  #  else:
  #    each_result.which = 0 if random_choice else 1
  
  each_result.bingo = int(request.POST['bingo'])
  each_result.bad = int(request.POST['bad'])
  
  each_result.save()
  
  return HttpResponseRedirect(reverse('evaluate:display'))
  







