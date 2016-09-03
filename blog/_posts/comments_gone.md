{"id": 11, "title": "Delete all my blog"}I realized that my blog is so vulnerable to spam comments when I logged in today and saw 1400+ comments waiting for my moderation. These spam comments occupy the space of my server and block me from seeing the legitimate ones.

So I just marked all of the comments spam and delete them at one go. I didn't realize that there are some legitimate comments sitting at the bottom of the long list.

When I refreshed the page, I found that the previous comments were all gone!

<a href="http://blog.zvaya.com/wp-content/uploads/2014/08/freakout.png"><img class="alignnone size-full wp-image-56" src="http://blog.zvaya.com/wp-content/uploads/2014/08/freakout.png" alt="freakout" width="121" height="113" /></a> Ahhhh~~

--preview--

Anyway, this is really a painful lesson. I shouldn't forget that spam is always part of our digital life.

In fact, all these spam messages should be easily caught in a simple text classifier which adopts any nontrivial machine learning techniques. Last year, I even worked on an empirical research study on spam messages detection.

Generally, text classification works effectively in well-written articles, because these articles surely contain certain keywords that suggest what categories they probably belong to. But, spam is a different story. spam messages do not belong to any specific genre. In fact, they are classified as spam because of the act of senders in mass-mailing blindly, not because of its content. But surprisingly, text classification techniques work quite well in identifying spam emails. This may be due to the fact that most spam emails contain words that intend to advertise or promote something; and these words are rarely mentioned in non-spam emails.

In the experiment I did, I took two public spam/ham corpora and tried to classify the mix of messages into two groups -- spam and ham ("ham" is the arcane term used by those machine learning research folks to refer to legitimate messages), by four machine learning algorithms. And an algorithm as simple as Naive Bayes could perform this task fairly well in a short period of time. Support Vector Machine technique is more complex and slower but it can achieve an even higher accuracy in detecting spam messages.

But even the worst algorithm can achieve an accuracy of more than 96%. Note that this is a weighted accuracy; while mis-classifying spam messages as legitimate is a relatively minor issue, the opposite is quite unacceptable.

Anyway, after a lengthy recall on that smart machine learning research, I still resort to a more naive way of deterring spam comments. That is: Captcha!

<a href="http://blog.zvaya.com/wp-content/uploads/2014/08/Capture1.png"><img class="alignnone size-medium wp-image-58" src="http://blog.zvaya.com/wp-content/uploads/2014/08/Capture1.png" alt="Capture" width="300" height="292" /></a>

If the spammer is in anyway slightly smarter, the answer can actually be calculated automatically. But anyway, let me see if this works first!

&nbsp;