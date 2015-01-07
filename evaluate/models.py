from django.db import models


#class Exp_raw(models.Model):
#  tweet_id = models.BigIntegerField()
#  tag = models.TextField()
#
#  def __str__(self):
#    return self.tag
#

class Exp_lda(models.Model):
  tweet_id = models.BigIntegerField()
  tag = models.TextField()

  def __str__(self):
    return self.tag


#class Chosen_tags(models.Model):
#  tweet_id = models.BigIntegerField()
#  lda_tag = models.TextField()
#  raw_tag = models.TextField()


class Chosen_tweet(models.Model):
  tweet_id = models.BigIntegerField()


#class Results(models.Model):
#  user_id = models.TextField()
#  tweet_id = models.BigIntegerField()
#  lda_tag = models.TextField()
#  raw_tag = models.TextField()
#  lda_score = models.IntegerField()
#  raw_score = models.IntegerField()
#  which = models.IntegerField()


class Results(models.Model):
  user_id = models.TextField()
  tweet_id = models.BigIntegerField()
  tag = models.TextField()
  good = models.IntegerField()
  bad = models.IntegerField()


class User(models.Model):
  user_name = models.TextField()

  def __str__(self):
    return self.user_name
